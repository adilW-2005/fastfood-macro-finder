from config import db  # Ensure config is imported
from flask import Flask


# ✅ User Model for Authentication
class User(db.Model):
    __tablename__ = "users"  # ✅ Explicit table name to match ForeignKey reference

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)  # Store hashed passwords

    logs = db.relationship("nutrition_info", backref="user", lazy=True)



class nutrition_info(db.Model):
    __tablename__ = "nutrition_info"  # ✅ Explicit table name  

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)  # ✅ Connect to User Model    
    food_id = db.Column(db.String, nullable=False)

    food_name = db.Column(db.String(100))
    brand_name = db.Column(db.String(100))
    
    calories = db.Column(db.Float)
    protein = db.Column(db.Integer)  # Store as "city, state" or lat/lon
    fat = db.Column(db.Float)
    carbs = db.Column(db.Float)
