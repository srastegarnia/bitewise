import json
from bitewise.recipes import enforce_allowed_ingredients

def _ingredients(json_text):
    data = json.loads(json_text)
    return data["recipes"][0]["ingredients"]

def test_non_keto_allows_only_inputs_plus_basic_extras():
    raw = '{"recipes":[{"name":"t","ingredients":["Sausage","Olive oil","Water","Garlic"]}]}'
    out = enforce_allowed_ingredients(raw, ["Sausage"], diets=None)
    assert set(_ingredients(out)) == {"Sausage", "Water"}

def test_keto_allows_keto_extras_and_singular_plural_inputs():
    raw = '{"recipes":[{"name":"t","ingredients":["Sausages","olive oil","butter","Water"]}]}'
    out = enforce_allowed_ingredients(raw, ["Sausage"], diets=["Keto"])
    # compare case-insensitively
    got = {s.lower() for s in _ingredients(out)}
    assert {"sausages", "olive oil", "butter", "water"}.issubset(got)
