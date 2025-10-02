# models/swap_request.py
from config.db import mongo
from bson import ObjectId

class SwapRequestModel:
    @staticmethod
    def collection():
        return mongo.db.swap_requests

    @staticmethod
    def create(request_data):
        return SwapRequestModel.collection().insert_one(request_data)

    @staticmethod
    def find_all(query=None):
        return list(SwapRequestModel.collection().find(query or {}))

    @staticmethod
    def find_by_id(request_id):
        return SwapRequestModel.collection().find_one({"_id": ObjectId(request_id)})

    @staticmethod
    def update(request_id, updates):
        return SwapRequestModel.collection().update_one({"_id": ObjectId(request_id)}, {"$set": updates})

    @staticmethod
    def delete(request_id):
        return SwapRequestModel.collection().delete_one({"_id": ObjectId(request_id)})
