FEW_SHOT_BLOCK = r"""
    Example Input:
    Ingredients: rice, chicken, soy sauce
    Calorie Limit: 500 kcal
    Cuisines: Chinese
    Allergies: none
    Dietary Preferences: none
    Example Output:
    {{
    "recipes": [
    {{"name": "Soy Chicken Fried Rice",
    "ingredients": ["rice", "chicken", "soy sauce"],
    "estimated_calories": 450}},
    {{"name": "Chicken Rice Stir-Fry",
    "ingredients": ["rice", "chicken", "soy sauce"],
    "estimated_calories": 480}}
    ]
    }}

    Example Input:
    Ingredients: spinach, canned tuna, lemon
    Calorie Limit: 300 kcal
    Cuisines: Italian
    Allergies: none
    Dietary Preferences: none
    Example Output:
    {{
    "recipes": [
    {{"name": "Lemon Tuna Spinach Salad",
    "ingredients": ["spinach", "canned tuna", "lemon"],
    "estimated_calories": 250}},
    {{"name": "Spinach Tuna Citrus Mix",
    "ingredients": ["spinach", "canned tuna", "lemon"],
    "estimated_calories": 260}}
    ]
    }}

    Example Input:
    Ingredients: tomatoes, black beans, corn, avocado, chicken
    Calorie Limit: 400 kcal
    Cuisines: Mexican
    Allergies: Nuts, Lactose
    Dietary Preferences: Vegetarian
    Example Output:
    {{
    "recipes": [
    {{"name": "Black Bean and Corn Salsa",
    "ingredients": ["tomatoes", "black beans", "corn"],
    "estimated_calories": 300}},
    {{"name": "Avocado Tomato Salad",
    "ingredients": ["tomatoes", "avocado"],
    "estimated_calories": 350}}
    ]
    }}

    Example Input:
    Ingredients: rice, chicken, soy sauce, pasta, beans
    Calorie Limit: 600 kcal
    Cuisines: Chinese
    Allergies: Beans
    Dietary Preferences: Gluten-free
    Example Output:
    {{
    "recipes": [
    {{"name": "Gluten-Free Soy Chicken Fried Rice",
    "ingredients": ["rice", "chicken", "gluten-free soy sauce"],
    "estimated_calories": 450}},
    {{"name": "Chicken Rice Stir-Fry",
    "ingredients": ["rice", "chicken", "gluten-free soy sauce"],
    "estimated_calories": 450}}
    ]
    }}

    Example Input:
    Ingredients: sweet potatoes, kale, chickpeas, tahini, spinach, onion, garlic, ginger, mustard seeds
    Calorie Limit: 400 kcal
    Cuisines: Indian
    Allergies: Gluten
    Dietary Preferences: Vegan
    Example Output:
    {{
    "recipes": [
    {{"name": "Sweet Potato and Chickpea Curry (Gluten-Free)",
    "ingredients": ["sweet potatoes", "spinach", "chickpeas", "tahini", "onion", "garlic"],
    "estimated_calories": 390}},
    {{"name": "Spiced Chickpea and Sweet Potato Stir-Fry",
    "ingredients": ["sweet potatoes", "chickpeas", "kale", "onion", "ginger","mustard seeds"],
    "estimated_calories": 360}}
    ]
    }}

    Example Input:
    Ingredients: salmon, asparagus, quinoa, lemon, garlic
    Calorie Limit: 500 kcal
    Cuisines: American
    Allergies: Dairy
    Dietary Preferences: Pescatarian
    Example Output:
    {{
    "recipes": [
    {{"name": "Lemon Garlic Salmon with Quinoa and Asparagus",
    "ingredients": ["salmon", "asparagus", "quinoa", "lemon", "garlic"],
    "estimated_calories": 480}},
    {{"name": "Quinoa Asparagus Salad with Lemon Salmon",
    "ingredients": ["salmon", "asparagus", "quinoa", "lemon"],
    "estimated_calories": 450}}
    ]
    }}

    Example Input:
    Ingredients: rice, Canned tuna in water, light mayo, Soy sauce, Nori seaweed, Sesame seeds, Pickled ginger,Cucumber 
    Calorie Limit: 400 kcal
    Cuisines: Japanese
    Allergies: none
    Dietary Preferences: none
    Example Output:
    {{
    "recipes": [
    {{"name": "Tuna Onigiri(Rice Ball)",
    "ingredients": ["rice", "Canned tuna in water", "light mayo", "Soy sauce", "Nori seaweed", "Sesame seeds", "Pickled ginger"],
    "estimated_calories": 380}},
    {{"name": "Tuna cucmber Temaki",
    "ingredients": ["rice", "Canned tuna in water", "Soy sauce", "Nori seaweed", "Cucumber", "Sesame seeds", "Pickled ginger"],
    "estimated_calories": 370}}
    ]
    }}

    Example Input:
    Ingredients: zucchini, ground turkey, tomatoes, onions
    Calorie Limit: 350 kcal
    Cuisines: Italian
    Allergies: none
    Dietary Preferences: Keto
    Example Output:
    {{
    "recipes": [
    {{"name": "Keto Turkey Zucchini Skillet",
    "ingredients": ["zucchini", "ground turkey", "tomatoes", "onions"],
    "estimated_calories": 320}},
    {{"name": "Italian Turkey Zucchini Boats",
    "ingredients": ["zucchini", "ground turkey", "tomatoes"],
    "estimated_calories": 300}}
    ]
    }}

    Example Input:
    Ingredients: chicken thighs, rice, coconut milk, curry paste, onions
    Calorie Limit: 800 kcal
    Cuisines: Indian
    Allergies: none
    Dietary Preferences: none
    Example Output:
    {{
    "recipes": [
    {{"name": "Coconut Chicken Curry with Rice",
    "ingredients": ["chicken thighs", "rice", "coconut milk", "curry paste", "onions"],
      "estimated_calories": 750}},
    {{"name": "Spicy Chicken Curry Rice Bowl",
    "ingredients": ["chicken thighs", "rice", "coconut milk", "curry paste"],
    "estimated_calories": 720}}
    ]
    }}

    Example Input:
    Ingredients: ground beef, pasta, tomatoes, cheese, cream
    Calorie Limit: 900 kcal
    Cuisines: Italian
    Allergies: none
    Dietary Preferences: none
    Example Output:
    {{
    "recipes": [
    {{"name": "Creamy Beef Pasta Bake",
    "ingredients": ["ground beef", "pasta", "tomatoes", "cheese", "cream"],
    "estimated_calories": 850}},
    {{"name": "Beef and Cheese Pasta Skillet",
    "ingredients": ["ground beef", "pasta", "tomatoes", "cheese"],
    "estimated_calories": 820
    }}
    ]
    }}

    Example Input:
    Ingredients: tomato, cucumber, red onion, black olives, feta, chicken, meat, onion, rice, bread
    Calorie Limit: 200 kcal
    Cuisines: none
    Allergies: Eggplant
    Dietary Preferences: none
    Example Output:
    {{
    "recipes": [
    {{"name": "Classic Greek Salad",
    "ingredients”: ["tomato", "cucumber", "red onion", "black olives", "feta"],
    "estimated_calories": 180}},
    {{"name": "Chicken‑and‑Rice Stuffed Tomato",
    "ingredients": ["tomato", "Cooked rice", "chicken", "Onion", "black olives", "feta"],
    "estimated_calories":195}}
    ]
    }}

    Example Input:
    Ingredients: canned fish, coconut milk, rice, pasta, oats, honey, egg, butter, onion, cheese, chicken breast, lettuce, eggplant
    Calorie Limit: 400 kcal
    Cuisines: Chinese
    Allergies: non
    Dietary Preferences: Keto
    Example Output: 
    {{
    "recipes": [
    {{"name": "Eggplant and Chicken Stir-Fry",
    "ingredients": ["chicken breast", "eggplant", "onion", "butter"],
    "estimated_calories": 350}},
    {{"name": "Cheesy Egg Lettuce Wraps",
    "ingredients": "egg", "cheese", "lettuce leaves", "butter"],
    "estimated_calories":220}}
    ]
    }}

    Example Input:
    Ingredients: chicken breast, bell peppers, onions, brown rice, avocado, cheddar, salsa, tortilla, beans, cheese, sour cream, eggs, lean ground beef, lettuce, tomato
    Calorie Limit: 700 kcal
    Cuisines: Mexican
    Allergies: Egg
    Dietary Preferences: none
    Example Output:
    {{
    "recipes": [
    {{"name": "Chicken Fajita Bowl",
    "ingredients": [chicken breast”, “bell peppers”, “onions”,” brown rice”, “avocado”, “cheddar”, “salsa”],
    "estimated_calories": 700}},
    {{"name": "Chicken & Bean Burrito",
    "ingredients": ["tortilla", "beans", "chicken breast", "beans", "brown rice", "cheese", "salsa",  "sour cream"],
    "estimated_calories":700}},
    {{"name": "Huevos Rancheros with Beans & Avocado",
    "ingredients": ["tortilla","avocado","salsa","cheese", "eggs", "beans"],
    "estimated_calories":650}},
    {{"name": "Taco Salad with Beef",
    "ingredients": ["lean ground beef", "lettuce", "tomato", "onions", "avocado", "cheese", "sour cream", "tortilla", "salsa"],
    "estimated_calories":700}}
    ]
    }}

    Example Input:
    Ingredients: pork belly, potatoes, butter, garlic, green beans
    Calorie Limit: 1000 kcal
    Cuisines: American
    Allergies: Dairy
    Dietary Preferences: none
    Example Output:
    {{
    "recipes": [
    {{"name": "Garlic Pork Belly with Roasted Potatoes",
    "ingredients": ["pork belly", "potatoes", "garlic", "green beans"],
    "estimated_calories": 900}},
    {{"name": "Pork Belly and Potato Hash",
    "ingredients": ["pork belly", "potatoes", "garlic"],
    "estimated_calories": 870}}
    ]
    }}
        
    Example Input:
    Ingredients: chicken, rice, barberries, peanuts, saffron, onion, eggplant, kashk, garlic, mint, rice, lentils, onions, butter, eggs
    Calorie Limit: 500 kcal
    Cuisines: Iranian
    Allergies: Eggs, Peanuts
    Dietary Preferences: Gluten-free
    Example Output: 
    {{
    "recipes": [
    {{"name": "Zereshk Polo ba Morgh",
    "ingredients": ["chicken", "rice", "barberries", "saffron", "onion", "butter"],
    "estimated_calories": 500 }},
    {{"name": "Kashk-e Bademjan",
    "ingredients": ["eggplant", "onion", "kashk", "garlic", "mint"],
    "estimated_calories":480}},
    {{"name": "Adas Polo (Lentil Rice with Raisins)",
    "ingredients": ["rice", "lentils", "onions", "butter"],
    "estimated_calories":500}}
    ]
    }}


    Example Input:
    Ingredients:  chickpeas, tomato, garlic, ginger, potato, Cauliflower florets, onion, semolina, carrot, peas, beans, green chilli
    Calorie Limit: 370 kcal
    Cuisines: Indian
    Allergies: none
    Dietary Preferences: Vegan
    Example Output:
    {{
    "recipes": [
    {{
    "name": "Chana Masala with Brown Rice",
    "ingredients": ["chickpeas", garlic", "ginger", "tomato", "onion"],
    "estimated_calories": 370}},
    {{"name": "Aloo Gobi with Roti",
    "ingredients": ["potato", "Cauliflower florets", "tomato", "onion"],
    "estimated_calories": 370}},
    {{"name": "Aloo Gobi with Roti",
    "ingredients": ["semolina", "carrot", "beans","onion","green chilli"],
    "estimated_calories": 360}}
    ]
    }}

    Example Input:
    Ingredients: tofu, ginger, broccoli florets, red bell pepper, sesame seeds, cauliflower rice, bell peppers, shirataki noodles, tahini, coconut aminos, apple cider vinegar, garlic, chilli flakes, almond milk
    Calorie Limit: 700 kcal
    Cuisines: Japanese
    Allergies: Beans and Lactose
    Dietary Preferences: Keto
    Example Output:
    {{
    "recipes": [
    {{"name": "Keto Baked Tofu with Sesame-Ginger Veggies",
    "ingredients": ["tofu", "ginger", "broccoli florets", "red bell pepper", "sesame seeds", "apple cider vinegar", "olive oil"],
    "estimated_calories": 600}},
    {{"name": "Keto Sesame-Ginger Cauliflower Rice Bowl",
    "ingredients": ["cauliflower rice", "bell Peppers", "shirataki noodles", "tahini", "coconut aminos", "apple cider vinegar", "garlic", "chilli flakes", "unsweetened almond milk", "butter"],
    "estimated_calories": 650}},
    {{"name": "Spicy Shirataki Noodle Stir-Fry",
    "ingredients": ["shirataki noodles", "tofu", "red bell pepper", "broccoli florets", "garlic", "chilli flakes", "tahini", "coconut aminos", "apple cider vinegar", "olive oil", "sesame seeds"],
    "estimated_calories": 630}}
    ]
    }}


    Example Input: 
    Ingredients: zucchini, eggplant, olive oil, garlic, cherry tomatoes, basil, cauliflower, walnuts, nutritional yeast, lemon, spinach, mushrooms  
    Calorie Limit: 700 kcal  
    Cuisines: Italian 
    Allergies: Beans and Lactose 
    Dietary Preferences: Keto  
    Example Output:
    {{
    "recipes": [
    {{"name": "Keto Eggplant Parmesan (Dairy-Free)",
    "ingredients": ["eggplant", "nutritional yeast", "garlic", "basil", "olive oil", "walnuts (crushed)", "cherry tomatoes"],
    "estimated_calories": 650}},
    {{"name": "Creamy Garlic Mushroom & Zucchini Noodles",
    "ingredients": ["zucchini (spiralized)", "mushrooms", "garlic", "olive oil", "unsweetened almond milk", "nutritional yeast", "spinach", "lemon juice"],
    "estimated_calories": 600}},
   {{"name": "Walnut-Pesto Stuffed Mushrooms",
    "ingredients": ["mushrooms", "walnuts", "basil", "garlic", "olive oil", "nutritional yeast", "spinach", "lemon juice"],
    "estimated_calories": 580}}
    ]
    }}    

    Example Input:
    Ingredients: tortilla chips, beef, sausage, corn, green chilli, mushroom, cheese, milk, salami, potato, bread, chicken, butter
    Calorie Limit: 1200 kcal
    Cuisines: none
    Allergies: none
    Dietary Preferences: none
    Example Output:
    {{
    "recipes": [
    {{"name": "Loaded Nacho Mountain",
    "ingredients": ["Tortilla chips", "green chilli", "cheese", "milk", "mushroom", "corn","sausage", "beef","salami"],
    "estimated_calories": 1200}},
    {{"name": "Cheesy Meat-Stuffed Potatoes",
    "ingredients": ["Potato", "beef", "sausage", "mushroom", "milk", "cheese", "green chilli", "salami"],
    "estimated_calories": 1050}},
   {{"name": "Melty Meat Madness Sandwich",
    "ingredients": ["bread", "milk", "butter", "salami", "chicken", "sausage", "cheese", "mushroom", "green chilli"],
    "estimated_calories": 1200}}
    ]
    }}
""".strip()


PROMPT_TEMPLATE = r"""
You are a Waste and Calorie Wise Food Crafter.

Suggest recipes based on available ingredients, following these rules:
- Use ONLY the user's provided ingredients: {ingredients_str}.
- Allowed extras:
  - For Keto: butter, olive oil, apple cider vinegar, salt, pepper, water.
  - For other diets: salt, pepper, oil, vinegar, water.
- Prioritize low waste (use as many inputs as possible).
- Stay strictly at or under the calorie limit ({calorie_limit} kcal).
- Match preferred cuisines when possible ({cuisines_str}).
- Respect dietary preferences: {diets_str}.
- Avoid allergens: {allergies_str}.
- Return STRICT JSON with key "recipes": list of objects
  having fields name (str), ingredients (subset of input), estimated_calories (int).

### Keto-specific rules
1. Prioritize: Meat/Fish/Eggs > low-carb veggies (zucchini, spinach, broccoli).
2. Macros: high fat, moderate protein, minimal carbs (<5% of calories).
3. Banned: grains, starchy vegetables, legumes, sugar.

{few_shots}

Example Input:
Ingredients: {ingredients_str}
Calorie Limit: {calorie_limit} kcal
Cuisines: {cuisines_str}
Allergies: {allergies_str}
Dietary Preferences: {diets_str}
Example Output:
""".strip()