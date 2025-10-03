from flask import request, jsonify
from bson import ObjectId
from models.swap_request import SwapRequestModel
from models.book import BookModel
from models.user import UserModel


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


# ✅ Get all requests created by the logged-in user (Requester view)
def get_my_swap_requests(user_id):
    swaps = SwapRequestModel.find_all({"requesterId": ObjectId(user_id)})
    enriched_swaps = []

    for s in swaps:
        s["_id"] = str(s["_id"])
        s["requesterId"] = str(s["requesterId"])

        # Requested book info
        book = BookModel.find_by_id(s["requestedBookId"])
        if book:
            s["requestedBookId"] = str(book["_id"])
            s["requestedBook"] = {
                "title": book.get("title"),
                "author": book.get("author"),
            }

            # Owner info (only if accepted)
            owner = UserModel.find_by_id(book["ownerId"])
            if owner and s["status"] == "accepted":
                s["ownerId"] = {
                    "name": owner.get("name"),
                    "email": owner.get("email"),
                }
            else:
                s["ownerId"] = {"name": None, "email": None}

        # Offered book info
        if s.get("offeredBookId"):
            offered_book = BookModel.find_by_id(s["offeredBookId"])
            if offered_book:
                s["offeredBookId"] = str(offered_book["_id"])
                s["offeredBook"] = {
                    "title": offered_book.get("title"),
                    "author": offered_book.get("author"),
                }

        enriched_swaps.append(s)

    return jsonify(enriched_swaps), 200


# ✅ Get all requests for books owned by the logged-in user (Owner view)
def get_owner_swap_requests(user_id):
    my_books = BookModel.find_all({"ownerId": ObjectId(user_id)})
    my_book_ids = [b["_id"] for b in my_books]

    swaps = SwapRequestModel.find_all({"requestedBookId": {"$in": my_book_ids}})
    enriched_swaps = []

    for s in swaps:
        s["_id"] = str(s["_id"])
        s["requesterId"] = str(s["requesterId"])

        # Requester details
        requester = UserModel.find_by_id(s["requesterId"])
        if requester:
            s["requester"] = {
                "name": requester.get("name"),
                "email": requester.get("email"),
            }

        # Requested book details
        book = BookModel.find_by_id(s["requestedBookId"])
        if book:
            s["requestedBookId"] = str(book["_id"])
            s["requestedBook"] = {
                "title": book.get("title"),
                "author": book.get("author"),
            }

        # Offered book details
        if s.get("offeredBookId"):
            offered_book = BookModel.find_by_id(s["offeredBookId"])
            if offered_book:
                s["offeredBookId"] = str(offered_book["_id"])
                s["offeredBook"] = {
                    "title": offered_book.get("title"),
                    "author": offered_book.get("author"),
                }

        enriched_swaps.append(s)

    return jsonify(enriched_swaps), 200


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

    # ✅ Update both swap request and book availability if accepted
    SwapRequestModel.update(swap_id, {"status": status})
    if status == "accepted":
        BookModel.update(swap["requestedBookId"], {"available": False})
        if swap.get("offeredBookId"):
            BookModel.update(swap["offeredBookId"], {"available": False})
    elif status == "rejected":
        # Rejection means the book should stay available
        BookModel.update(swap["requestedBookId"], {"available": True})

    return jsonify({"message": f"Swap request {status}"}), 200
