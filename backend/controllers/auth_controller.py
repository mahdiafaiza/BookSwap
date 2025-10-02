# controllers/auth_controller.py
from flask import request, jsonify
from models.user import UserModel
import jwt, os

JWT_SECRET = os.getenv("JWT_SECRET")

# ---------- Register ----------
def register_user():
    data = request.json
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    university = data.get("university")
    address = data.get("address")

    if not name or not email or not password:
        return jsonify({"message": "All fields are required"}), 400

    existing = UserModel.find_by_email(email)
    if existing:
        return jsonify({"message": "User already exists"}), 400

    user_id = UserModel.create(name, email, password, university, address)
    user = UserModel.find_by_id(user_id)
    token = jwt.encode({"id": str(user["_id"])}, JWT_SECRET, algorithm="HS256")

    return jsonify({
        "id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"],
        "token": token
    }), 201


# ---------- Login ----------
def login_user():
    data = request.json
    email, password = data.get("email"), data.get("password")

    user = UserModel.find_by_email(email)
    if not user:
        return jsonify({"message": "Invalid email or password"}), 401

    if not UserModel.check_password(user, password):
        return jsonify({"message": "Invalid email or password"}), 401

    token = jwt.encode({"id": str(user["_id"])}, JWT_SECRET, algorithm="HS256")

    return jsonify({
        "id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"],
        "token": token
    }), 200


# ---------- Profile ----------
def get_profile(current_user):
    return jsonify({
        "id": str(current_user["_id"]),
        "name": current_user.get("name"),
        "email": current_user.get("email"),
        "university": current_user.get("university", ""),
        "address": current_user.get("address", "")
    }), 200


# ---------- Update Profile ----------
def update_user_profile(current_user):
    data = request.json
    update_fields = {
        "name": data.get("name", current_user.get("name")),
        "email": data.get("email", current_user.get("email")),
        "university": data.get("university", current_user.get("university")),
        "address": data.get("address", current_user.get("address")),
    }

    UserModel.update(current_user["_id"], update_fields)
    updated = UserModel.find_by_id(current_user["_id"])
    token = jwt.encode({"id": str(updated["_id"])}, JWT_SECRET, algorithm="HS256")

    return jsonify({
        "id": str(updated["_id"]),
        "name": updated.get("name"),
        "email": updated.get("email"),
        "university": updated.get("university", ""),
        "address": updated.get("address", ""),
        "token": token
    }), 200
