# middleware/auth_middleware.py
from flask import request, jsonify
import jwt, os
from functools import wraps
from models.user import UserModel
from bson import ObjectId

JWT_SECRET = os.getenv("JWT_SECRET")

def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None

        # Extract Bearer token from headers
        if "Authorization" in request.headers:
            auth_header = request.headers["Authorization"]
            if auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]

        if not token:
            return jsonify({"message": "Not authorized, no token"}), 401

        try:
            decoded = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
            user = UserModel.find_by_id(decoded["id"])  # safe static model
            if not user:
                return jsonify({"message": "User not found"}), 404

            # Flask-style: pass current_user into the route handler
            return f(current_user=user, *args, **kwargs)

        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Invalid token"}), 401
        except Exception as e:
            return jsonify({"message": f"Auth error: {str(e)}"}), 401

    return decorated_function
