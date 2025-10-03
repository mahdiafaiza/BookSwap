# routes/auth_routes.py
from flask import Blueprint, request
from controllers.auth_controller import register_user, login_user, get_profile, update_user_profile
from middleware.auth_middleware import token_required

auth_bp = Blueprint("auth_bp", __name__)

# Register new user
@auth_bp.route("/register", methods=["POST"])
def route_register():
    return register_user()

# Login
@auth_bp.route("/login", methods=["POST"])
def route_login():
    return login_user()

# Get profile (protected)
@auth_bp.route("/profile", methods=["GET"])
@token_required
def route_get_profile(current_user):
 return get_profile(current_user) 

# Update profile (protected)
@auth_bp.route("/profile", methods=["PUT"])
@token_required
def route_update_profile(current_user):
    return update_user_profile(current_user)
