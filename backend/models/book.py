# models/book.py
from config.db import mongo
from bson import ObjectId


class BookModel:
    REQUIRED_FIELDS = ["title", "author", "owner_id"]

    @staticmethod
    def _collection():
        from flask import current_app
        return current_app.extensions['mongo'].db.books

    @staticmethod
    def create(title, author, owner_id, description=None, condition="Good", available=True, requested_by=None):
        if not title or not author or not owner_id:
            raise ValueError("Title, author, and owner_id are required.")
        book = {
            "title": title,
            "author": author,
            "owner_id": ObjectId(owner_id),
            "description": description,
            "condition": condition,
            "available": available,
            "requested_by": requested_by,
        }
        result = BookModel._collection().insert_one(book)
        return str(result.inserted_id)

    @staticmethod
    def find_all(query=None):
        return list(BookModel._collection().find(query or {}))

    @staticmethod
    def find_by_id(book_id):
        return BookModel._collection().find_one({"_id": ObjectId(book_id)})

    @staticmethod
    def update(book_id, updates):
        return BookModel._collection().update_one({"_id": ObjectId(book_id)}, {"$set": updates})

    @staticmethod
    def delete(book_id):
        return BookModel._collection().delete_one({"_id": ObjectId(book_id)})
