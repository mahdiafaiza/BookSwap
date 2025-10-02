# models/user.py
from config.db import mongo
from bson import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash


class UserModel:
    REQUIRED_FIELDS = ["name", "email", "password"]

    @staticmethod
    def _collection():
        from flask import current_app
        print('[DEBUG] current_app.extensions:', current_app.extensions)
        return current_app.extensions['mongo'].db.users

    @staticmethod
    def create(name, email, password, university=None, address=None):
        if not name or not email or not password:
            raise ValueError("Name, email, and password are required.")
        hashed_pw = generate_password_hash(password, method="pbkdf2:sha256")
        user = {
            "name": name,
            "email": email,
            "password": hashed_pw,
            "university": university,
            "address": address,
        }
        result = UserModel._collection().insert_one(user)
        return str(result.inserted_id)

    @staticmethod
    def find_by_email(email):
        return UserModel._collection().find_one({"email": email})

    @staticmethod
    def find_by_id(user_id):
        return UserModel._collection().find_one({"_id": ObjectId(user_id)})

    @staticmethod
    def update(user_id, updates):
        return UserModel._collection().update_one({"_id": ObjectId(user_id)}, {"$set": updates})

    @staticmethod
    def check_password(user, password):
        return check_password_hash(user["password"], password)
