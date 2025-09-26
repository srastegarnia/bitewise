from typing import List, Optional
import os, json
import google.generativeai as genai
from google.generativeai.types import GenerationConfig
from .prompts import PROMPT_TEMPLATE, FEW_SHOT_BLOCK
import re

from dotenv import load_dotenv
load_dotenv(override=False)

# helpers for strict ingredient guard
ALLOWED_EXTRAS_ANY  = {"salt", "pepper", "oil", "vinegar", "water"}
ALLOWED_EXTRAS_KETO = ALLOWED_EXTRAS_ANY | {"butter", "olive oil", "apple cider vinegar"}

def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", s.strip().lower())

def _expand_allowed(inputs: list[str]) -> set[str]:
    allowed = set()
    for x in inputs:
        n = _norm(x)
        allowed.add(n)
        # naive plural/singular equivalence (sausage <-> sausages)
        if n.endswith("s"):
            allowed.add(n[:-1])
        else:
            allowed.add(n + "s")
    return allowed

def enforce_allowed_ingredients(json_text: str, inputs: list[str], diets: Optional[List[str]]) -> str:
    try:
        data = json.loads(json_text)
    except Exception:
        return json_text  # if it's not valid JSON, return as-is

    # build allowed set from inputs (+simple plural/singular)
    allowed_names = _expand_allowed(inputs)

    # choose extras by diet
    keto = any(_norm(d) == "keto" for d in (diets or []))
    extras = ALLOWED_EXTRAS_KETO if keto else ALLOWED_EXTRAS_ANY

    cleaned = []
    for r in data.get("recipes", []):
        ing = []
        for item in r.get("ingredients", []):
            n = _norm(item)
            if n in allowed_names or n in extras:
                ing.append(item)
        if ing:
            r["ingredients"] = ing
            cleaned.append(r)

    return json.dumps({"recipes": cleaned}, ensure_ascii=False, indent=2)

# end of strict ingredient helpers

def create_client(api_key: Optional[str] = None):
    """Return a Gemini client, or None if no key (offline demo mode)."""
    key = api_key or os.getenv("GOOGLE_API_KEY")
    if not key:
        return None
    genai.configure(api_key=key)
    return genai.GenerativeModel("gemini-2.0-flash")

def _fallback_recipes(ingredients: List[str], calorie_limit: int) -> str:
    name = ", ".join(ingredients[:3]) or "Pantry"
    data = {
        "recipes": [
            {"name": f"{name} Bowl", "ingredients": ingredients, "estimated_calories": max(150, min(calorie_limit, calorie_limit - 50))},
            {"name": f"{name} Stir-Fry", "ingredients": ingredients, "estimated_calories": calorie_limit}
        ]
    }
    return json.dumps(data, ensure_ascii=False)

def suggest_recipes_from_ingredients(
    client,
    ingredients: List[str],
    calorie_limit: int,
    cuisines: Optional[List[str]] = None,
    allergies: Optional[List[str]] = None,
    diets: Optional[List[str]] = None,
) -> str:
    if not ingredients:
        return json.dumps({"recipes": []})
    if client is None:
        return _fallback_recipes(ingredients, calorie_limit)

    ingredients_str = ", ".join(ingredients)
    cuisines_str    = ", ".join(cuisines)  if cuisines  else "any cuisine"
    allergies_str   = ", ".join(allergies) if allergies else "none"
    diets_str       = ", ".join(diets)     if diets     else "none"

    prompt = PROMPT_TEMPLATE.format(
        ingredients_str=ingredients_str,
        calorie_limit=calorie_limit,
        cuisines_str=cuisines_str,
        allergies_str=allergies_str,
        diets_str=diets_str,
        few_shots=FEW_SHOT_BLOCK,
    )

    resp = client.generate_content(
        contents=[{"parts": [{"text": prompt}]}],
        generation_config=GenerationConfig(
            response_mime_type="application/json",
            temperature=0.4,
            top_p=0.9,
        ),
    )
    raw = resp.text or "{}"
    return enforce_allowed_ingredients(raw, ingredients, diets)

