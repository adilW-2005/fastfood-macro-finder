import re
from flask import json
import requests
from auth_token import access_token
from fuzzywuzzy import fuzz

def search_restauraunt(brand_name, max_results=10, page_number=1, max_calories= 0, min_protein= 0, sort_by = None):
    API_URL = "https://platform.fatsecret.com/rest/server.api"
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    params = {
        "method": "foods.search",
        "search_expression": brand_name,
        "format": "json"
    }
    
    response = requests.post(API_URL, headers=headers, data=params)
    response = response.json()

    # Initialize the menu_items dictionary
    menu_items = {}

    if 'foods' in response and 'food' in response['foods']:
        foods = response['foods']['food']
        
        for item in foods:
            
            food_id = item.get("food_id", None)
            item_brand_name = item.get("brand_name", "Unknown Brand")  
            food_name = item.get("food_name", "Unknown Food")      
            food_description = item.get("food_description", "")
            
            calories_match = re.search(r'Calories: (\d+)', food_description)
            protein_match = re.search(r'Protein: (\d+\.?\d*)', food_description)
            fat_match = re.search(r'Fat: (\d+\.?\d*)', food_description)
            carbs_match = re.search(r'Carbs: (\d+\.?\d*)', food_description)
            
            
            calories = float(calories_match.group(1)) if calories_match else 0
            protein = float(protein_match.group(1)) if protein_match else 0
            fat = float(fat_match.group(1)) if fat_match else 0
            carbs = float(carbs_match.group(1)) if carbs_match else 0

            split_data_carbs = f"{round((((carbs * 4) / calories) * 100), 2)}%" if calories else "0%"
            split_data_fat = f"{round((((fat * 9) / calories) * 100), 2)}%" if calories else "0%"
            split_data_protein = f"{round((((protein * 4) / calories) * 100), 2)}%" if calories else "0%"

            
            food_info = {
                "food_id": food_id,
                "brand_name": item_brand_name,
                "food_name": food_name,
                "calories": calories,
                "protein": protein,
                "fat": fat,
                "carbs": carbs,
                "Split": {
                    "carbs": split_data_carbs,
                    "fat": split_data_fat,
                    "protein": split_data_protein
                }
            }
            
            if (calories <= max_calories) and (protein >= min_protein):
                menu_items[food_name] = food_info 
        
            

    filtered_menu_items = {}
        
    for key, value in menu_items.items():
        if fuzz.partial_ratio(value.get("brand_name"), brand_name) > 80:
            filtered_menu_items[key] = value
    
        if sort_by == "calories":
            menu_items = dict(sorted(menu_items.items(), key=lambda x: x[1]["calories"]))  # Low to high
        elif sort_by == "protein":
            menu_items = dict(sorted(menu_items.items(), key=lambda x: x[1]["protein"], reverse=True))  # High to low

    return filtered_menu_items
