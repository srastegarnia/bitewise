# CLI for BiteWise
import argparse
import json
import sys
from importlib.metadata import version, PackageNotFoundError

from .recipes import (
    create_client,
    suggest_recipes_from_ingredients,
)

def _split_csv(s: str):
    return [x.strip() for x in s.split(",") if x.strip()]

def main() -> int:
    parser = argparse.ArgumentParser(
        prog="bitewise",
        description="BiteWise: waste- and constraint-aware (calorie, allergy, diet, cuisine) recipe suggester."
    )
    parser.add_argument("--version", action="store_true", help="Show package version and exit")
    parser.add_argument("--run", action="store_true", help="Launch demo UI (requires Jupyter)")

    sub = parser.add_subparsers(dest="command")

    # bitewise suggest --ingredients "a,b,c" --calories 500 [...]
    p_suggest = sub.add_parser("suggest", help="Suggest recipes from ingredients")
    p_suggest.add_argument("--ingredients", required=True, help="Comma-separated list, e.g. 'rice,chicken,soy sauce'")
    p_suggest.add_argument("--calories", type=int, required=True, help="Calorie limit (int)")
    p_suggest.add_argument("--cuisines", default="", help="Comma-separated cuisines (optional)")
    p_suggest.add_argument("--allergies", default="", help="Comma-separated allergens (optional)")
    p_suggest.add_argument("--diets", default="", help="Comma-separated diets (optional)")
    p_suggest.add_argument("--offline", action="store_true", help="Force offline fallback (ignore API key)")

    args = parser.parse_args()

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

    if args.command == "suggest":
        ingredients = _split_csv(args.ingredients)
        cuisines    = _split_csv(args.cuisines) if args.cuisines else None
        allergies   = _split_csv(args.allergies) if args.allergies else None
        diets       = _split_csv(args.diets) if args.diets else None

        client = None if args.offline else create_client()
        result_json = suggest_recipes_from_ingredients(
            client,
            ingredients=ingredients,
            calorie_limit=args.calories,
            cuisines=cuisines,
            allergies=allergies,
            diets=diets,
        )
        # pretty-print if valid JSON, else raw
        try:
            print(json.dumps(json.loads(result_json), ensure_ascii=False, indent=2))
        except Exception:
            print(result_json)
        return 0

    # default: show help
    parser.print_help()
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
