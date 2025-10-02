# server.py
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Import route modules
from routes.auth_routes import auth_bp
from routes.task_routes import task_bp
from routes.book_routes import book_bp
from routes.swap_routes import swap_bp
from config.db import mongo  # your MongoDB connection

# Load .env variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# MongoDB connection (from config/db.py)
MONGO_URI = os.getenv("MONGO_URI")
JWT_SECRET = os.getenv("JWT_SECRET")
PORT = int(os.getenv("PORT", 5000))

# Register routes (like app.use() in Express)
app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(task_bp, url_prefix="/api/tasks")
app.register_blueprint(book_bp, url_prefix="/api/books")
app.register_blueprint(swap_bp, url_prefix="/api/swap-requests")

if __name__ == "__main__":
    PORT = int(os.getenv("PORT", 5000))
    app.run(port=PORT, debug=True)
