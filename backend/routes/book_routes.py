# routes/book_routes.py
from flask import Blueprint, request
from controllers.book_controller import get_books, get_my_books, add_book, update_book, delete_book
from middleware.auth_middleware import token_required

book_bp = Blueprint("book_bp", __name__)

# Get all available books (excluding current user's own)
@book_bp.route("/all", methods=["GET"])
@token_required
def route_get_books(current_user):
    return get_books(current_user["_id"])

# Get logged-in user's own books
@book_bp.route("/mine", methods=["GET"])
@token_required
def route_get_my_books(current_user):
    return get_my_books(current_user["_id"])

# Add a new book
@book_bp.route("/", methods=["POST"])
@token_required
def route_add_book(current_user):
    return add_book(current_user["_id"])

# Update a book (owner only)
@book_bp.route("/<book_id>", methods=["PUT"])
@token_required
def route_update_book(current_user, book_id):
    return update_book(current_user["_id"], book_id)

# Delete a book (owner only)
@book_bp.route("/<book_id>", methods=["DELETE"])
@token_required
def route_delete_book(current_user, book_id):
    return delete_book(current_user["_id"], book_id)
