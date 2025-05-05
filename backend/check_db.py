from flask import Flask
from config import db
from models import nutrition_info  # Make sure this matches your model name

# Create a Flask app and initialize the database
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///nutrition.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

# Push application context to allow DB queries
with app.app_context():
    entries = nutrition_info.query.all()

    if not entries:
        print("🚫 No entries found in the database.")
    else:
        for entry in entries:
            print(f"✅ ID: {entry.id}, user_ID: {entry.user_id}, Calories: {entry.calories}, Protein: {entry.protein}, Carbs: {entry.carbs}, Fat: {entry.fat}")
