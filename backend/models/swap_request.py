# models/swap_request.py
from config.db import mongo
from bson import ObjectId


class SwapRequestModel:
    @staticmethod
    def _collection():
        from flask import current_app
        return current_app.extensions['mongo'].db.swap_requests

    @staticmethod
    def create(swap_request):
        """Insert a new swap request and return the new ID as a string."""
        result = SwapRequestModel._collection().insert_one(swap_request)
        return str(result.inserted_id)

    @staticmethod
    def find_all(query={}):
        """Return all swap requests matching a query as a list of dicts."""
        return list(SwapRequestModel._collection().find(query))

    @staticmethod
    def find_by_id(swap_request_id):
        """Return a single swap request by its ID."""
        return SwapRequestModel._collection().find_one({"_id": ObjectId(swap_request_id)})

    @staticmethod
    def update(swap_request_id, updates):
        """Update a swap request by its ID."""
        return SwapRequestModel._collection().update_one(
            {"_id": ObjectId(swap_request_id)},
            {"$set": updates}
        )

    @staticmethod
    def delete(swap_request_id):
        """Delete a swap request by its ID."""
        return SwapRequestModel._collection().delete_one({"_id": ObjectId(swap_request_id)})
