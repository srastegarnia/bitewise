from typing import List
from typing_extensions import TypedDict

class Recipe(TypedDict):
    name: str
    ingredients: List[str]
    estimated_calories: int

class RecipeList(TypedDict):
    recipes: List[Recipe]