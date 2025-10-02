# routes/swap_routes.py
from flask import Blueprint, request
from controllers.swap_request_controller import (
    create_swap_request,
    get_owner_swap_requests,
    get_requester_swap_requests,
    respond_to_swap_request,
)
from middleware.auth_middleware import token_required

swap_bp = Blueprint("swap_bp", __name__)

# Create a new swap request
@swap_bp.route("/", methods=["POST"])
@token_required
def route_create_swap_request(current_user):
    return create_swap_request(current_user["_id"])


# Get all swap requests for books owned by logged-in user
@swap_bp.route("/owner", methods=["GET"])
@token_required
def route_owner_swap_requests(current_user):
    return get_owner_swap_requests(current_user["_id"])


# Get all swap requests made by the logged-in user
@swap_bp.route("/requester", methods=["GET"])
@token_required
def route_requester_swap_requests(current_user):
    return get_requester_swap_requests(current_user["_id"])


# Accept or reject a swap request
@swap_bp.route("/<swap_request_id>/respond", methods=["PUT"])
@token_required
def route_respond_swap_request(current_user, swap_request_id):
    return respond_to_swap_request(current_user["_id"], swap_request_id)
