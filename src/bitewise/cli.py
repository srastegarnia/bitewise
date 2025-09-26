# Minimal CLI for BiteWise
import argparse
import sys
import json
from importlib.metadata import version, PackageNotFoundError

from .recipes import (
    create_client,
    suggest_recipes_from_ingredients,
)

# -------- helpers --------
def _split_csv(s: str):
    return [x.strip() for x in s.split(",") if x.strip()]

def _print_json(obj):
    print(json.dumps(obj, ensure_ascii=False, indent=2))

def _detect_from_image(client, image_path: str, max_items: int = 20):
    """
    Use Gemini to detect edible grocery items in an image.
    Returns a Python list[str].
    """
    import json as _json
    from PIL import Image
    from google.generativeai.types import GenerationConfig

    prompt = (
        "Identify edible grocery/food items visible in this photo. "
        "Return ONLY a JSON array of strings (unique, capitalized common names). "
        "No commentary."
    )
    img = Image.open(image_path)
    resp = client.generate_content(
        [img, {"text": prompt}],
        generation_config=GenerationConfig(
            response_mime_type="application/json",
            temperature=0.2,
        ),
    )
    try:
        data = _json.loads(resp.text)
    except Exception:
        data = resp.text

    if isinstance(data, dict) and "ingredients" in data:
        items = data["ingredients"]
    else:
        items = data
    if not isinstance(items, list):
        items = []

    # normalize + unique + clamp
    items = [str(x).strip() for x in items if str(x).strip()]
    seen, out = set(), []
    for it in items:
        if it not in seen:
            seen.add(it)
            out.append(it)
        if len(out) >= max_items:
            break
    return out

def _pick_from_list(items: list[str]) -> list[str]:
    """
    Simple terminal picker: show numbered items, ask for comma-separated numbers.
    Empty input = keep all.
    """
    if not items:
        return items
    print("\nDetected items:")
    for i, it in enumerate(items, 1):
        print(f"  {i:2d}. {it}")
    raw = input(
        "\nPick items by number (comma-separated, e.g. 1,3,5). "
        "Press Enter to keep ALL: "
    ).strip()
    if not raw:
        return items
    try:
        idxs = [int(x) for x in raw.split(",") if x.strip()]
    except ValueError:
        print("Invalid input; keeping ALL detected items.", file=sys.stderr)
        return items
    chosen = []
    for k in idxs:
        if 1 <= k <= len(items):
            chosen.append(items[k - 1])
    return chosen or items

# -------- main --------
def main() -> int:
    parser = argparse.ArgumentParser(
        prog="bitewise",
        description="BiteWise: waste- and constraint-aware (calorie, allergy, diet, cuisine) recipe suggester."
    )
    sub = parser.add_subparsers(dest="cmd")

    # version / run
    parser.add_argument("--version", action="store_true", help="Show package version and exit")
    parser.add_argument("--run", action="store_true", help="Launch demo UI (requires Jupyter)")

    # detect
    p_detect = sub.add_parser("detect", help="Detect ingredients from an image")
    p_detect.add_argument("-i", "--image", required=True, help="Path to fridge/pantry image")
    p_detect.add_argument("--max-items", type=int, default=20, help="Max ingredients to return")

    # suggest
    p_suggest = sub.add_parser("suggest", help="Suggest recipes from ingredients")
    p_suggest.add_argument("--ingredients", required=True, help="Comma-separated list")
    p_suggest.add_argument("--calories", "-c", required=True, type=int, help="Calorie limit")
    p_suggest.add_argument("--cuisine", default="", help="Comma-separated cuisines (optional)")
    p_suggest.add_argument("--allergy", default="", help="Comma-separated allergens to avoid")
    p_suggest.add_argument("--diet", default="", help="Comma-separated diets (Keto, Vegan, etc.)")

    # plan (detect ➜ optionally pick ➜ suggest)
    p_plan = sub.add_parser("plan", help="Detect from image then (optionally) pick items before suggesting")
    p_plan.add_argument("-i", "--image", required=True, help="Path to fridge/pantry image")
    p_plan.add_argument("--calories", "-c", required=True, type=int, help="Calorie limit")
    p_plan.add_argument("--cuisine", default="", help="Comma-separated cuisines (optional)")
    p_plan.add_argument("--allergy", default="", help="Comma-separated allergens to avoid")
    p_plan.add_argument("--diet", default="", help="Comma-separated diets (Keto, Vegan, etc.)")
    p_plan.add_argument("--max-items", type=int, default=20, help="Max detected ingredients to use")
    p_plan.add_argument("--pick", action="store_true", help="Interactively pick from detected items")

    args = parser.parse_args()

    # top-level flags
    if args.version:
        try:
            print(version("bitewise"))
        except PackageNotFoundError:
            print("0.0.0")
        return 0

    if args.run:
        try:
            from .app import run
            return run()
        except Exception as e:
            print(f"BiteWise failed to start: {e}", file=sys.stderr)
            return 1

    # subcommands
    if args.cmd in {"detect", "suggest", "plan"}:
        client = create_client()  # needs GOOGLE_API_KEY in env for online mode

    if args.cmd == "detect":
        items = _detect_from_image(client, args.image, args.max_items)
        _print_json(items)
        return 0

    if args.cmd == "suggest":
        ingredients = _split_csv(args.ingredients)
        cuisines  = _split_csv(args.cuisine) if args.cuisine else None
        allergies = _split_csv(args.allergy) if args.allergy else None
        diets     = _split_csv(args.diet)    if args.diet    else None
        out = suggest_recipes_from_ingredients(
            client, ingredients, args.calories, cuisines, allergies, diets
        )
        print(out)
        return 0

    if args.cmd == "plan":
        detected = _detect_from_image(client, args.image, args.max_items)
        if args.pick:
            detected = _pick_from_list(detected)

        cuisines  = _split_csv(args.cuisine) if args.cuisine else None
        allergies = _split_csv(args.allergy) if args.allergy else None
        diets     = _split_csv(args.diet)    if args.diet    else None
        out = suggest_recipes_from_ingredients(
            client, detected, args.calories, cuisines, allergies, diets
        )
        print(out)
        return 0

    # default: show help
    parser.print_help()
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
