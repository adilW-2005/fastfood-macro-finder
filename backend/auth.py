from flask import Blueprint, request, jsonify, session
from config import db, bcrypt
from models import User

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    print("Received signup data:", data)

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        print("Username already taken:", username)
        return jsonify({"error": "Username already taken"}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
    new_user = User(username=username, password=hashed_password)

    db.session.add(new_user)
    db.session.commit()

    session["user_id"] = new_user.id

    print("User created:", new_user.username, new_user.id)
    return jsonify({
        "message": "User created successfully",
        "user_id": new_user.id,
        "username": new_user.username
    }), 201





@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username).first()
    if not user or not bcrypt.check_password_hash(user.password, password):
        return jsonify({"error": "Invalid credentials"}), 401

    # Store user session
    session["user_id"] = user.id

    return jsonify({"message": "Login successful", "user_id": user.id}), 200





@auth_bp.route("/check_session", methods=["GET"])
def check_session():
    print("\n🔍 Incoming Cookies:", request.cookies)  # ✅ Debugging step
    print("🔍 Current Flask Session Data:", session)  # ✅ Debugging Flask session  # ✅ Debugging step
    if "user_id" in session:
        user = User.query.get(session["user_id"])
        return jsonify({"message": "User is logged in", "user_id": session["user_id"], "username": user.username}), 200
        
    return jsonify({"message": "User is not logged in"}), 401




@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.pop("user_id", None)
    return jsonify({"message": "Logged out successfully"}), 200