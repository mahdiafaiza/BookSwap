# routes/swap_request_routes.py
from flask import Blueprint
from controllers.swap_request_controller import (
    create_swap_request,
    get_owner_swap_requests,
    get_my_swap_requests,    #updated name
    respond_to_swap_request,
)
from middleware.auth_middleware import token_required

swap_bp = Blueprint("swap_bp", __name__)

# Create a new swap request
@swap_bp.route("", methods=["POST"])
@token_required
def route_create_swap(current_user):
    return create_swap_request(user_id=current_user["_id"])

# Get all swap requests for books owned by logged-in user
@swap_bp.route("/owner", methods=["GET"])
@token_required
def route_get_owner_requests(current_user):
    return get_owner_swap_requests(user_id=current_user["_id"])

# Get all swap requests made by the logged-in user
@swap_bp.route("/requester", methods=["GET"])
@token_required
def route_get_my_requests(current_user):
    return get_my_swap_requests(user_id=current_user["_id"]) 

# Accept or reject a swap request
@swap_bp.route("/<swap_id>/respond", methods=["PUT"])
@token_required
def route_respond_swap(swap_id, current_user):
    return respond_to_swap_request(swap_id=swap_id, user_id=current_user["_id"])
