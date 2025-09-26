from typing import List, Optional
import os, json
import google.generativeai as genai
from google.generativeai.types import GenerationConfig
from .prompts import PROMPT_TEMPLATE, FEW_SHOT_BLOCK

from dotenv import load_dotenv
load_dotenv(override=False)

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
    return resp.text
