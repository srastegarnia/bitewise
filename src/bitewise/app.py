# src/bitewise/app.py
from __future__ import annotations
import json, os, tempfile
from pathlib import Path
from typing import Iterable

try:
    import ipywidgets as widgets
    from IPython.display import display
except Exception:
    def run() -> int:
        print(
            "BiteWise demo requires Jupyter + ipywidgets.\n"
            "Install and run:\n  pip install jupyterlab ipywidgets\n  jupyter lab"
        )
        return 1
else:
    from .recipes import create_client, suggest_recipes_from_ingredients
    from .vision  import detect_ingredients

    # ---------- helpers ----------
    def _split_csv(s: str) -> list[str]:
        return [x.strip() for x in (s or "").split(",") if x.strip()]

    def _parse_text_ingredients(text: str) -> list[str]:
        text = (text or "").replace("\r", "")
        if "\n" in text:
            return [p.strip() for p in text.split("\n") if p.strip()]
        return _split_csv(text)

    def _dedup(seq: Iterable[str]) -> list[str]:
        seen, out = set(), []
        for x in seq:
            if x and x not in seen:
                seen.add(x); out.append(x)
        return out

    def _iter_uploads(value):
        """Support ipywidgets v7 (dict) + v8 (list/tuple)."""
        if not value: 
            return
        if isinstance(value, dict):
            for name, meta in value.items():
                yield name, meta.get("content") or meta.get("data")
        elif isinstance(value, (list, tuple)):
            for meta in value:
                yield meta.get("name"), meta.get("content") or meta.get("data")

    # ---------- constants (match your screenshots) ----------
    PANTRY_CHOICES = [
        "lentils","chickpeas","rice","potatoes","pasta","quinoa",
        "flour","sugar","beans","oats","cornmeal","butter",
        "oil","onion","garlic"
    ]
    CUISINES = ["Italian","Chinese","Mexican","Indian","Japanese","American","Mediterranean"]
    ALLERGIES = ["Lactose","Nuts","Shellfish","Eggs","Soy","Fish"]
    DIETS = ["Vegetarian","Vegan","Pescatarian","Keto","Gluten-Free"]

    # ---------- UI ----------
    def run() -> int:
        client = create_client()

        # Top description (styled like your shots)
        desc = widgets.HTML(
            "<div style='color:#18794e;font-family:ui-sans-serif,system-ui;"
            "font-weight:600;margin:6px 0 10px 0;'>"
            "Upload an image of your fridge (or manually enter everything), "
            "select pantry items, choose cuisines, specify allergies and diets, "
            "and get tailored recipe suggestions."
            "</div>"
        )
        spacer = widgets.Text(layout=widgets.Layout(width="100%"))

        # Section 1: Image + Calories
        up = widgets.FileUpload(accept="image/*", multiple=True, description="Upload Fridge Image (0)")
        cal = widgets.BoundedIntText(value=500, min=150, max=2000, description="Calorie Limit (kcal)")
        note = widgets.HTML(
            "<i>Note: If you don’t have an image, you can manually enter your ingredients after the process.</i>"
        )
        s1 = widgets.VBox([up, cal, note])

        def _upd_upload_label(_=None):
            n = 0
            v = up.value
            if isinstance(v, dict): n = len(v)
            elif isinstance(v, (list, tuple)): n = len(v)
            up.description = f"Upload Fridge Image ({n})"
        up.observe(_upd_upload_label, names="value")

        # Section 2: Pantry
        pantry_checks = [widgets.Checkbox(description=label, value=False) for label in PANTRY_CHOICES]
        pantry_grid = widgets.GridBox(
            children=pantry_checks,
            layout=widgets.Layout(grid_template_columns="repeat(3, minmax(140px, 1fr))", grid_gap="8px")
        )
        pantry_custom = widgets.Text(placeholder="e.g., canned tomatoes, soy sauce", description="Custom Pantry Items:")
        s2 = widgets.VBox([widgets.HTML("<b>Select Pantry Items</b>"), pantry_grid, pantry_custom])

        # Section 3: Cuisine (multi)
        cuisine_checks = [widgets.Checkbox(description=c, value=False) for c in CUISINES]
        cuisine_grid = widgets.GridBox(
            children=cuisine_checks,
            layout=widgets.Layout(grid_template_columns="repeat(3, minmax(140px, 1fr))", grid_gap="8px")
        )
        s3 = widgets.VBox([widgets.HTML("<b>Select Preferred Cuisines</b>"), cuisine_grid])

        # Section 4: Allergies + other
        allergy_checks = [widgets.Checkbox(description=a, value=False) for a in ALLERGIES]
        allergy_grid = widgets.GridBox(
            children=allergy_checks,
            layout=widgets.Layout(grid_template_columns="repeat(3, minmax(140px, 1fr))", grid_gap="8px")
        )
        allergy_other = widgets.Text(placeholder="e.g., sesame, celery", description="Other Allergies:")
        s4 = widgets.VBox([widgets.HTML("<b>Select Allergies</b>"), allergy_grid, allergy_other])

        # Section 5: Dietary prefs + other
        diet_checks = [widgets.Checkbox(description=d, value=False) for d in DIETS]
        diet_grid = widgets.GridBox(
            children=diet_checks,
            layout=widgets.Layout(grid_template_columns="repeat(3, minmax(140px, 1fr))", grid_gap="8px")
        )
        diet_other = widgets.Text(placeholder="e.g., Low-Carb, Paleo", description="Other Dietary :")
        s5 = widgets.VBox([widgets.HTML("<b>Select Dietary Preferences</b>"), diet_grid, diet_other])

        # Accordion to match your collapsible look
        acc = widgets.Accordion(children=[s1, s2, s3, s4, s5])
        acc.set_title(0, "Image Upload & Calorie Limit")
        acc.set_title(1, "Pantry Items")
        acc.set_title(2, "Cuisine Preferences")
        acc.set_title(3, "Allergies")
        acc.set_title(4, "Dietary Preferences")
        acc.selected_index = None  # start collapsed, like your screenshots

        # Process button (green)
        btn = widgets.Button(
            description="Process",
            layout=widgets.Layout(width="100%", height="52px", margin="12px 0"),
            button_style="success",
        )

        out = widgets.Output()

        # ---------- collect+run ----------
        def _selected_labels(checks: list[widgets.Checkbox]) -> list[str]:
            return [c.description for c in checks if c.value]

        def _detect_from_uploads() -> list[str]:
            items: list[str] = []
            if client is None:
                # Silent: user may be offline; they can still submit manual pantry/custom items
                return items
            temp_paths: list[Path] = []
            try:
                for name, data in _iter_uploads(up.value) or []:
                    if not data:
                        continue
                    tmp = Path(tempfile.mkstemp(prefix="bw_", suffix=Path(name or "img.jpg").suffix or ".jpg")[1])
                    temp_paths.append(tmp)
                    with open(tmp, "wb") as f:
                        f.write(data)
                    try:
                        items.extend(detect_ingredients(str(tmp), client, max_items=20))
                    except Exception:
                        pass
            finally:
                for p in temp_paths:
                    try: p.unlink(missing_ok=True)
                    except Exception: pass
            return _dedup(items)

        def _pretty_json(s: str) -> str:
            try:
                return json.dumps(json.loads(s), ensure_ascii=False, indent=2)
            except Exception:
                return s

        def _tag_list(values: list[str]) -> str:
            if not values: 
                return "<i>None</i>"
            tags = "".join(f"<span style='display:inline-block;padding:2px 8px;margin:2px 6px 2px 0;"
                           f"border-radius:999px;background:#e7f5ff;border:1px solid #d0ebff'>{v}</span>"
                           for v in values)
            return tags

        @out.capture(clear_output=True)
        def _on_process(_):
            # Gather ingredients from (uploads ➜ detection) + pantry + custom
            detected = _detect_from_uploads()
            pantry_sel = _selected_labels(pantry_checks)
            pantry_extra = _parse_text_ingredients(pantry_custom.value)

            ingredients = _dedup(detected + pantry_sel + pantry_extra)

            # Cuisines, allergies, diets
            cuisines = _selected_labels(cuisine_checks) or None
            allergies = _dedup(_selected_labels(allergy_checks) + _split_csv(allergy_other.value)) or None
            diets     = _dedup(_selected_labels(diet_checks) + _split_csv(diet_other.value)) or None

            # Call suggester (online if key present, else offline fallback)
            result = suggest_recipes_from_ingredients(
                client, ingredients, cal.value, cuisines, allergies, diets
            )

            # Summary card (exactly one block above JSON)
            summary = widgets.HTML(
                "<div style='font-family:ui-sans-serif,system-ui;"
                "border:1px solid #e9ecef;border-radius:10px;padding:12px;background:#f8f9fa;'>"
                f"<div><b>Ingredients ({len(ingredients)}):</b> {_tag_list(ingredients)}</div>"
                f"<div style='margin-top:6px'><b>Cuisines:</b> {_tag_list(cuisines or [])}</div>"
                f"<div style='margin-top:6px'><b>Allergies:</b> {_tag_list(allergies or [])}</div>"
                f"<div style='margin-top:6px'><b>Diets:</b> {_tag_list(diets or [])}</div>"
                f"<div style='margin-top:6px'><b>Calories:</b> {cal.value}</div>"
                "</div>"
            )
            print(_pretty_json(result))
            display(summary)

        btn.on_click(_on_process)

        # Layout (matches your clean, single-column flow)
        ui = widgets.VBox([desc, spacer, acc, btn, out])
        display(ui)
        return 0
