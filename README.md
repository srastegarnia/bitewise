# BiteWise - Meal Planner 🍽️💡  
*From pantry chaos to plated perfection.* 
Smart, waste-aware meal planning that respects **calories**, **diets**, **cuisines**, and **allergies**.

[![Demo Video](https://img.shields.io/badge/Watch-Demo-red)](https://youtu.be/Pxk0hzvAGEQ) 
[![Kaggle Notebook](https://img.shields.io/badge/Open-Kaggle-blue)](https://www.kaggle.com/code/shimarastegar/bitewise)
[![Blog Post](https://img.shields.io/badge/Read-Blog-green)](https://medium.com/@brastgrants/blitudes-revolutionizing-meal-planning-with-your-sl-kitchen-assistant-fa7672bb6ce9)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)

<div align="center">
  <img src="docs/img/01_overview.png" alt="BiteWise overview" width="90%">
</div>

---

## 🚀 What it does
- **Smart Ingredient Detection:** Upload a fridge/pantry photo(s), type ingredients, or select from a pantry list.
- **Calorie-aware:** Suggestions within your selected limit (e.g., 200–1200 kcal).
- **Dietary Customization:** Keto, Vegan, Gluten-Free, Vegetarian, etc.
- **Global Cuisines:** Italian, Japanese, Mexican, Indian, and more.
- **Waste Reduction:** Prioritizes using what you already have.  
- **Developer-friendly:** Returns clean JSON; guardrails enforce allowed ingredients only.
- **Responsible outputs:** JSON-only model output, calorie bounds, explicit allow-lists

---

## 🧠 How it works (tech)
- **Model:** Gemini 2.0 Flash (text + vision). 
- **Vision:** Detects edible items in an image. 
- **Prompting:** Few-shot JSON format; post-filtering ensures only allowed ingredients make it through.
- **Modules:**
  - `src/bitewise/recipes.py` - client, prompting, guardrails, suggest_recipes_from_ingredients
  - `src/bitewise/vision.py` - image → ingredients
  - `src/bitewise/cli.py` - CLI entrypoint (bitewise detect|suggest|plan)
  - `src/bitewise/app.py` - simple Jupyter UI (hybrid flow)
- **Tests:** `tests/test_recipes_guard.py` - verifies the ingredient allow-list behavior

---

## 🖼️ Screens (quick tour)

**1) Start**  
Clean, collapsible sections keep the flow simple.  
![Overview](docs/img/01_overview.png)

**2) Upload + detect**  
Fridge/pantry preview and detected ingredients from image(s). 
![Upload & Detect](docs/img/02_upload_detect.png)

**3) Preferences**  
Pick pantry items, cuisines, allergies, and diets.  
![Preferences](docs/img/03_preferences.png)

**4) Recipe cards**  
2-3 tailored options with ingredients + calories. 
![Recipe cards](docs/img/04_recipe_cards.png)

**5) Recipe detail**  
Full instructions, waste-reduction tips, and nutrition notes. 
![Recipe detail](docs/img/05_recipe_detail.png)

---

## 🔧 Quick start

```bash
git clone https://github.com/srastegarnia/bitewise.git
cd bitewise
python -m venv .venv-bitewise && source .venv-bitewise/bin/activate
pip install -r requirements.txt
```
You can run *either* the comprehensive notebook or the CLI. Both use the same core logic.

### Option 1 - Notebook (all-in-one):
Open: notebooks/BiteWise_Capstone_Workbook.ipynb
- You’ll need your own API key (see below).

Or a minimal launcher: notebooks/BiteWise_App_Demo.ipynb
```bash
import importlib, bitewise.app
importlib.reload(bitewise.app)
from bitewise.app import run
run()
```

### Option 2 - CLI:
Create .env in the project root:
```bash
GOOGLE_API_KEY=YOUR_ACTUAL_KEY
```
Then:
```bash
# detect ingredients (image → list)
bitewise detect -i examples/sample_fridge.jpg

# suggest recipes (ingredients → JSON)
bitewise suggest --ingredients "rice,chicken,soy sauce" --calories 500

# end-to-end: detect then suggest
bitewise plan -i examples/sample_fridge.jpg -c 700
```
---

## 📦 Project layout

```text
Project layout
└─ bitewise/
   ├─ docs/                          # Docs assets (images used in README)
   │  └─ img/
   │
   ├─ examples/                      # Sample inputs for quick CLI demos
   │
   ├─ notebooks/                     # User-facing notebooks
   │  ├─ BiteWise_App_Demo.ipynb     # Minimal launcher notebook (runs the UI via app.run())
   │  └─ BiteWise_Capstone_Workbook.ipynb  # Full exploratory/“giant” notebook
   │
   ├─ src/
   │  └─ bitewise/                   # Installable package code
   │     ├─ __init__.py              
   │     ├─ app.py                   # Jupyter UI: upload → detect → confirm → generate recipes
   │     ├─ cli.py                   # CLI: `bitewise {detect|suggest|plan}`
   │     ├─ prompts.py               # Prompt template + few-shot examples (JSON output)
   │     ├─ recipes.py               # Gemini client, fallback, ingredient guard, suggest()
   │     ├─ vision.py                # Image → ingredients (Gemini Vision; PIL/inline support)
   │     └─ schemas.py               # TypedDicts for structured outputs (Recipe/RecipeList)
   │
   ├─ tests/                         
   │  ├─ test_recipes_guard.py       # Guardrail tests
   │  ├─ test_schemas.py             # Schema import smoke test
   │  └─ test_vision.py              # Vision smoke (skips if no API key)
   │
   ├─ README.md                      
   ├─ requirements.txt              
   ├─ pyproject.toml                 
   ├─ .gitignore                    
   ├─ .env.example                   # Template for GOOGLE_API_KEY
   └─ LICENSE                        
```
---

## 📚 Links
- Demo (2 min): https://youtu.be/Pxk0hzvAGEQ
- Kaggle: https://www.kaggle.com/code/shimarastegar/bitewise
- Medium: https://medium.com/@brastgrants/blitudes-revolutionizing-meal-planning-with-your-sl-kitchen-assistant-fa7672bb6ce9

---

## 🗺️ Roadmap

- Better small-item detection and messy-fridge robustness
- Saved user profiles and persistent preferences
- Grocery list generation from chosen recipes
- Optional nutrition grounding (FDA/USDA)
- Voice and chat refinements

---

## 🪪 License

MIT - see LICENSE