# controllers/swap_request_controller.py
from flask import jsonify, request
from bson import ObjectId
from datetime import datetime
from config.db import mongo


# ✅ Create a new swap request
def create_swap_request(user_id):
    data = request.json
    requested_book_id = data.get("requestedBookId")
    offered_book_id = data.get("offeredBookId")
    message = data.get("message", "")

    if not requested_book_id:
        return jsonify({"message": "Requested book ID is required"}), 400

    # Find the requested book
    requested_book = mongo.db.books.find_one({"_id": ObjectId(requested_book_id)})
    if not requested_book:
        return jsonify({"message": "Requested book not found"}), 404
    if not requested_book.get("available", True):
        return jsonify({"message": "Book is not available"}), 400
    if str(requested_book["ownerId"]) == str(user_id):
        return jsonify({"message": "You cannot request your own book"}), 400

    swap_request = {
        "requesterId": ObjectId(user_id),
        "ownerId": requested_book["ownerId"],
        "requestedBookId": ObjectId(requested_book_id),
        "offeredBookId": ObjectId(offered_book_id) if offered_book_id else None,
        "message": message,
        "status": "pending",
        "createdAt": datetime.utcnow(),
        "updatedAt": datetime.utcnow(),
    }

    result = mongo.db.swaprequests.insert_one(swap_request)
    swap_request["_id"] = str(result.inserted_id)
    swap_request["requesterId"] = str(swap_request["requesterId"])
    swap_request["ownerId"] = str(swap_request["ownerId"])
    swap_request["requestedBookId"] = str(swap_request["requestedBookId"])
    if swap_request["offeredBookId"]:
        swap_request["offeredBookId"] = str(swap_request["offeredBookId"])

    return jsonify(swap_request), 201


# ✅ Get all swap requests for books owned by the logged-in user
def get_owner_swap_requests(user_id):
    pipeline = [
        {"$match": {"ownerId": ObjectId(user_id)}},
        {"$lookup": {
            "from": "users",
            "localField": "requesterId",
            "foreignField": "_id",
            "as": "requester"
        }},
        {"$lookup": {
            "from": "books",
            "localField": "requestedBookId",
            "foreignField": "_id",
            "as": "requestedBook"
        }},
        {"$lookup": {
            "from": "books",
            "localField": "offeredBookId",
            "foreignField": "_id",
            "as": "offeredBook"
        }},
        {"$unwind": "$requester"},
        {"$unwind": "$requestedBook"},
        {"$project": {
            "_id": {"$toString": "$_id"},
            "status": 1,
            "message": 1,
            "requester": {"name": "$requester.name", "email": "$requester.email"},
            "requestedBook": {"title": "$requestedBook.title", "author": "$requestedBook.author"},
            "offeredBook": {"title": {"$ifNull": ["$offeredBook.title", None]}, "author": {"$ifNull": ["$offeredBook.author", None]}}
        }},
        {"$sort": {"createdAt": -1}}
    ]
    requests = list(mongo.db.swaprequests.aggregate(pipeline))
    return jsonify(requests), 200


# ✅ Get all swap requests made by the logged-in user
def get_requester_swap_requests(user_id):
    pipeline = [
        {"$match": {"requesterId": ObjectId(user_id)}},
        {"$lookup": {
            "from": "users",
            "localField": "ownerId",
            "foreignField": "_id",
            "as": "owner"
        }},
        {"$lookup": {
            "from": "books",
            "localField": "requestedBookId",
            "foreignField": "_id",
            "as": "requestedBook"
        }},
        {"$unwind": "$owner"},
        {"$unwind": "$requestedBook"},
        {"$project": {
            "_id": {"$toString": "$_id"},
            "status": 1,
            "message": 1,
            "owner": {"name": "$owner.name", "email": "$owner.email"},
            "requestedBook": {"title": "$requestedBook.title", "author": "$requestedBook.author"},
        }},
        {"$sort": {"createdAt": -1}}
    ]
    requests = list(mongo.db.swaprequests.aggregate(pipeline))
    return jsonify(requests), 200


# ✅ Accept or reject a swap request
def respond_to_swap_request(user_id, swap_request_id):
    data = request.json
    status = data.get("status")

    if status not in ["accepted", "rejected"]:
        return jsonify({"message": "Invalid status"}), 400

    swap_request = mongo.db.swaprequests.find_one({"_id": ObjectId(swap_request_id)})
    if not swap_request:
        return jsonify({"message": "Swap request not found"}), 404

    if str(swap_request["ownerId"]) != str(user_id):
        return jsonify({"message": "Not authorized"}), 403

    update_data = {"status": status, "updatedAt": datetime.utcnow()}
    mongo.db.swaprequests.update_one({"_id": ObjectId(swap_request_id)}, {"$set": update_data})

    # If accepted, mark the book unavailable
    if status == "accepted":
        mongo.db.books.update_one(
            {"_id": swap_request["requestedBookId"]},
            {"$set": {"available": False}}
        )

    return jsonify({"message": f"Request {status}"}), 200
