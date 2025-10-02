# config/db.py
from flask_pymongo import PyMongo
from pymongo import MongoClient, errors
import os
from dotenv import load_dotenv

load_dotenv()

mongo = PyMongo()

def init_db(app):
    print("[DEBUG] mongo.db after init:", mongo.db)
    try:
        app.config["MONGO_URI"] = os.getenv("MONGO_URI")
        print("[DEBUG] Initializing PyMongo...")
        mongo.init_app(app)
        # Explicitly register PyMongo instance in extensions as 'mongo'
        app.extensions['mongo'] = mongo
        print(f"[DEBUG] mongo in extensions: {app.extensions.get('mongo')}")

        # Test raw connection (optional safety check)
        client = MongoClient(os.getenv("MONGO_URI"))
        client.admin.command("ping")
        print("✅ MongoDB connected successfully")

    except errors.ConnectionFailure as e:
        print("❌ MongoDB connection failed:", str(e))
    except Exception as e:
        print("❌ Unexpected MongoDB error:", str(e))
