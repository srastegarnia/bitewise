# Minimal CLI for BiteWise
import argparse
import sys
import json
from importlib.metadata import version, PackageNotFoundError

from .recipes import (
    create_client,
    suggest_recipes_from_ingredients,
)

# -----------------------
# Helpers
# -----------------------

def _split_csv(s: str):
    return [x.strip() for x in s.split(",") if x.strip()]

def _print_json(obj):
    print(json.dumps(obj, ensure_ascii=False, indent=2))

def _detect_from_image(client, image_path: str, max_items: int = 20):
    """
    Use Gemini to detect edible grocery items in an image.
    Returns a Python list[str].
    """
    if client is None:
        print("GOOGLE_API_KEY not set; 'detect' needs the online vision model.", file=sys.stderr)
        return []

    try:
        from PIL import Image
    except ImportError:
        print("Missing dependency: Pillow. Install with: pip install pillow", file=sys.stderr)
        return []

    try:
        from google.generativeai.types import GenerationConfig
    except Exception as e:
        print(f"Gemini SDK not available: {e}", file=sys.stderr)
        return []

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

    # Try to parse strict JSON; fall back gently if the model returns list-like text
    try:
        data = json.loads(resp.text)
    except Exception:
        data = resp.text

    # Normalize to list[str]
    if isinstance(data, dict) and "ingredients" in data:
        items = data["ingredients"]
    else:
        items = data
    if not isinstance(items, list):
        items = []

    # Clean, de-dup, clamp
    seen, out = set(), []
    for it in items:
        s = str(it).strip()
        if s and s not in seen:
            seen.add(s)
            out.append(s)
        if len(out) >= max_items:
            break
    return out

# -----------------------
# Entry point
# -----------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        prog="bitewise",
        description="BiteWise: waste- and constraint-aware (calorie, allergy, diet, cuisine) recipe suggester."
    )
    sub = parser.add_subparsers(dest="cmd")

    # top-level flags
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

    # plan (detect ➜ suggest)
    p_plan = sub.add_parser("plan", help="Detect from image then suggest recipes automatically")
    p_plan.add_argument("-i", "--image", required=True, help="Path to fridge/pantry image")
    p_plan.add_argument("--calories", "-c", required=True, type=int, help="Calorie limit")
    p_plan.add_argument("--cuisine", default="", help="Comma-separated cuisines (optional)")
    p_plan.add_argument("--allergy", default="", help="Comma-separated allergens to avoid")
    p_plan.add_argument("--diet", default="", help="Comma-separated diets (Keto, Vegan, etc.)")
    p_plan.add_argument("--max-items", type=int, default=20, help="Max detected ingredients to use")

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

    # subcommands → create client once
    if args.cmd in {"detect", "suggest", "plan"}:
        client = create_client()  # needs GOOGLE_API_KEY for online mode
    else:
        # No subcommand: show help and exit cleanly
        parser.print_help()
        return 0

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
        print(out)  # already JSON string
        return 0

    if args.cmd == "plan":
        if client is None:
            print("GOOGLE_API_KEY not set; 'plan' needs the online vision model.", file=sys.stderr)
            return 1
        detected = _detect_from_image(client, args.image, args.max_items)
        cuisines  = _split_csv(args.cuisine) if args.cuisine else None
        allergies = _split_csv(args.allergy) if args.allergy else None
        diets     = _split_csv(args.diet)    if args.diet    else None
        out = suggest_recipes_from_ingredients(
            client, detected, args.calories, cuisines, allergies, diets
        )
        print(out)
        return 0

    # Shouldn't reach here
    parser.print_help()
    return 0

if __name__ == "__main__":
    raise SystemExit(main())