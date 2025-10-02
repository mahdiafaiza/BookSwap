# models/book.py
from bson import ObjectId
from flask import current_app
from config.db import mongo


class BookModel:
    REQUIRED_FIELDS = ["title", "author", "condition"]

    @staticmethod
    def _collection():
        return current_app.extensions["mongo"].db.books

    @staticmethod
    def create(book):
        """
        book should be a dict with:
        {
          "ownerId": ObjectId,
          "title": str,
          "author": str,
          "description": str,
          "condition": str,
          "available": bool
        }
        """
        result = BookModel._collection().insert_one(book)
        return str(result.inserted_id)

    @staticmethod
    def find_all(query=None):
        if query is None:
            query = {}
        return list(BookModel._collection().find(query))

    @staticmethod
    def find_by_id(book_id):
        return BookModel._collection().find_one({"_id": ObjectId(book_id)})

    @staticmethod
    def update(book_id, updates):
        return BookModel._collection().update_one(
            {"_id": ObjectId(book_id)},
            {"$set": updates}
        )

    @staticmethod
    def delete(book_id):
        return BookModel._collection().delete_one({"_id": ObjectId(book_id)})
