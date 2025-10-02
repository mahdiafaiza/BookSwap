# controllers/book_controller.py
from flask import jsonify, request
from bson import ObjectId
from models.book import BookModel


# Get all available books (excluding current user's own)
def get_books(user_id=None):
    query = {"available": True}
    if user_id:
        query["ownerId"] = {"$ne": ObjectId(user_id)}

    books = BookModel.find_all(query)
    for book in books:
        book["_id"] = str(book["_id"])
        book["ownerId"] = str(book["ownerId"])
    return jsonify(books), 200


# Get current user's own books
def get_my_books(user_id):
    books = BookModel.find_all({"ownerId": ObjectId(user_id)})
    for book in books:
        book["_id"] = str(book["_id"])
        book["ownerId"] = str(book["ownerId"])
    return jsonify(books), 200


# Add a new book listing
def add_book(user_id):
    data = request.json
    if not data.get("title") or not data.get("author") or not data.get("condition"):
        return jsonify({"message": "Title, author, and condition are required"}), 400

    book = {
        "ownerId": ObjectId(user_id),
        "title": data["title"],
        "author": data["author"],
        "description": data.get("description", ""),
        "condition": data["condition"],
        "available": True,
    }

    # BookModel.create now returns a string ID
    book_id = BookModel.create(book)
    book["_id"] = book_id
    book["ownerId"] = str(book["ownerId"])
    return jsonify(book), 201


# Update book details (only owner can update)
def update_book(user_id, book_id):
    book = BookModel.find_by_id(book_id)
    if not book:
        return jsonify({"message": "Book not found"}), 404
    if str(book["ownerId"]) != str(user_id):
        return jsonify({"message": "Not authorized"}), 403

    data = request.json
    updates = {
        "title": data.get("title", book["title"]),
        "author": data.get("author", book["author"]),
        "description": data.get("description", book["description"]),
        "condition": data.get("condition", book["condition"]),
        "available": data.get("available", book["available"]),
    }
    BookModel.update(book_id, updates)

    updates["_id"] = str(book_id)
    updates["ownerId"] = str(user_id)
    return jsonify(updates), 200


# Delete book listing (only owner can delete)
def delete_book(user_id, book_id):
    book = BookModel.find_by_id(book_id)
    if not book:
        return jsonify({"message": "Book not found"}), 404
    if str(book["ownerId"]) != str(user_id):
        return jsonify({"message": "Not authorized"}), 403

    BookModel.delete(book_id)
    return jsonify({"message": "Book deleted"}), 200
