# BiteWise 🍽️✨
**From pantry chaos to plated perfection**  
*AI-powered meal planning that reduces waste, respects dietary needs, and saves time*

[![Demo Video](https://img.shields.io/badge/Watch-Demo-red)](https://youtube.com) 
[![Kaggle Notebook](https://img.shields.io/badge/Open-Kaggle-blue)](https://www.kaggle.com/code/shimarastegar/bitewise)
[![Blog Post](https://img.shields.io/badge/Read-Blog-green)](https://medium.com/@brastgrants/blitudes-revolutionizing-meal-planning-with-your-sl-kitchen-assistant-fa7672bb6ce9)

<div align="center">
  <img src="https://via.placeholder.com/800x400?text=BiteWise+App+Screenshot" alt="App Screenshot" width="70%">
</div>

## 🚀 Key Features
| Feature | Benefit |
|---------|---------|
| 📸 **Smart Ingredient Detection** | Upload fridge photos or manually enter ingredients |
| ⚖️ **Calorie-Conscious Recipes** | Set limits from 200-1200 kcal |
| 🌱 **Dietary Customization** | Keto, Vegan, Gluten-Free, and 10+ other diets |
| 🌍 **Global Cuisines** | Italian, Japanese, Mexican, and more |
| ♻️ **Waste Reduction** | Prioritizes using all available ingredients |

## 🧠 AI-Powered Technology
```python
# Sample recipe generation
def generate_recipe(ingredients, calories=500, diet="vegetarian"):
    return gemini.generate_content(f"""
    Suggest 3 {diet} recipes under {calories} calories using: 
    {', '.join(ingredients)}. Output in JSON format.""")
Core AI Components:

Gemini 2.0 Flash for lightning-fast suggestions

Computer Vision for ingredient recognition

Structured JSON Output for easy integration

Few-shot Prompting for precise recommendations

🛠️ How It Works
Input Ingredients → Upload a photo or type them in

Set Preferences → Calories, diet, allergies, cuisine

Get Recipes → 2-3 personalized meal options

Cook Smart → Full instructions & nutrition info

📦 Installation
bash
git clone https://github.com/srastegarnia/BiteWise.git
cd BiteWise
pip install -r requirements.txt
