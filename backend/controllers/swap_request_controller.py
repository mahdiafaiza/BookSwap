# controllers/swap_request_controller.py
from flask import request, jsonify
from bson import ObjectId
from models.swap_request import SwapRequestModel
from models.book import BookModel


# Create a new swap request
def create_swap_request(user_id):
    data = request.json
    requested_book_id = data.get("requestedBookId")
    offered_book_id = data.get("offeredBookId")
    message = data.get("message", "")

    if not requested_book_id:
        return jsonify({"message": "Requested book is required"}), 400

    swap_request = {
        "requesterId": ObjectId(user_id),
        "requestedBookId": ObjectId(requested_book_id),
        "offeredBookId": ObjectId(offered_book_id) if offered_book_id else None,
        "message": message,
        "status": "pending",
    }

    swap_id = SwapRequestModel.create(swap_request)
    swap_request["_id"] = str(swap_id)

    return jsonify(swap_request), 201


# ✅ Get all requests created by the logged-in user
def get_my_swap_requests(user_id):
    swaps = SwapRequestModel.find_all({"requesterId": ObjectId(user_id)})
    for s in swaps:
        s["_id"] = str(s["_id"])
        s["requesterId"] = str(s["requesterId"])
        if "requestedBookId" in s:
            s["requestedBookId"] = str(s["requestedBookId"])
        if "offeredBookId" in s and s["offeredBookId"]:
            s["offeredBookId"] = str(s["offeredBookId"])
    return jsonify(swaps), 200


# Get all requests for books owned by the logged-in user
def get_owner_swap_requests(user_id):
    my_books = BookModel.find_all({"ownerId": ObjectId(user_id)})
    my_book_ids = [b["_id"] for b in my_books]

    swaps = SwapRequestModel.find_all({"requestedBookId": {"$in": my_book_ids}})
    for s in swaps:
        s["_id"] = str(s["_id"])
        s["requesterId"] = str(s["requesterId"])
        if "requestedBookId" in s:
            s["requestedBookId"] = str(s["requestedBookId"])
        if "offeredBookId" in s and s["offeredBookId"]:
            s["offeredBookId"] = str(s["offeredBookId"])
    return jsonify(swaps), 200


# Respond to a swap request (accept/reject)
def respond_to_swap_request(user_id, swap_id):
    data = request.json
    status = data.get("status")
    if status not in ["accepted", "rejected"]:
        return jsonify({"message": "Invalid status"}), 400

    swap = SwapRequestModel.find_by_id(swap_id)
    if not swap:
        return jsonify({"message": "Swap request not found"}), 404

    # Ensure logged-in user owns the requested book
    book = BookModel.find_by_id(swap["requestedBookId"])
    if not book or str(book["ownerId"]) != str(user_id):
        return jsonify({"message": "Not authorized"}), 403

    SwapRequestModel.update(swap_id, {"status": status})
    return jsonify({"message": f"Swap request {status}"}), 200
