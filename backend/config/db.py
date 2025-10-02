# config/db.py
from flask_pymongo import PyMongo
from flask import Flask
import os

app = Flask(__name__)
app.config["MONGO_URI"] = os.getenv("MONGO_URI")

mongo = PyMongo(app)

# Usage example
db = mongo.db  # this is your database
users_collection = db.users
