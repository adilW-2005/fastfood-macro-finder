from flask import Blueprint, request, jsonify, session
from config import db, app  # Import `app` to run db.create_all()
from models import nutrition_info , User 

# ✅ Create a blueprint for data routes
data_bp = Blueprint("data", __name__)

# ✅ Ensure database is created when Flask starts
with app.app_context():
    db.create_all()
    print("✅ Database and tables created successfully!")

@data_bp.route("/log_item", methods=["POST"])
def log_item():
    data = request.get_json()

    if "user_id" not in session:
        return jsonify({"error": "User not logged in"}), 401

    data = request.get_json()
    user_id = session["user_id"]

    new_log = nutrition_info(
        user_id=user_id,
        food_id=data["food_id"],
        food_name=data.get("food_name"),
        brand_name=data.get("brand_name"),
        calories=float(data["calories"]),
        protein=float(data["protein"]),
        carbs=float(data["carbs"]),
        fat=float(data["fat"])
    )
    
    db.session.add(new_log)
    db.session.commit()

    # Return the new item's id in the response
    return jsonify({
        "message": "Log item saved successfully!",
        "item_id": new_log.id
    }), 200


@data_bp.route("/user_nutrition/", methods=["GET"])
def get_user_nutrition():
    if "user_id" not in session:
        return jsonify({"error": "User not logged in"}), 401

    user_id = session["user_id"]
    logs = nutrition_info.query.filter_by(user_id=user_id).all()

    if not logs:
        return jsonify({"message": "No nutrition data found for this user."}), 404

    total_calories = sum((log.calories or 0) for log in logs)
    total_protein = sum((log.protein or 0) for log in logs)
    total_carbs = sum((log.carbs or 0) for log in logs)
    total_fat = sum((log.fat or 0) for log in logs)

    user = User.query.get(user_id)
    username = user.username if user else "Unknown"

    return jsonify({
        "username": username,
        "totalCalories": total_calories,
        "totalProtein": total_protein,
        "totalCarbs": total_carbs,
        "totalFat": total_fat,
        "logs": [
            {
                "food_id": log.food_id,
                "food_name": log.food_name,
                "brand_name": log.brand_name,
                "calories": log.calories,
                "protein": log.protein,
                "carbs": log.carbs,
                "fat": log.fat
            }
            for log in logs
        ]
    }), 200



@data_bp.route("/unlog_item/<int:food_id>", methods=["DELETE"])
def unlog_item(food_id):

    if "user_id" not in session:
        return jsonify({"error": "User not logged in"}), 401

    user_id = session["user_id"]
    item = nutrition_info.query.filter_by(food_id=food_id, user_id=user_id).first()

    if not item:
        return jsonify({"error": "Item not found"}), 404

    unlogged_item_info = {
        "food_id": item.food_id,
        "user_id": item.user_id,
        "calories": item.calories,
        "protein": item.protein,
        "carbs": item.carbs,
        "fat": item.fat
    }

    db.session.delete(item)
    db.session.commit()

    return jsonify(
    {"message": "Item unlogged successfully!",
    "unlogged_item": unlogged_item_info
    }), 200
