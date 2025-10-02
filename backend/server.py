# server.py

import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from config.db import init_db

def create_app():
    load_dotenv()
    app = Flask(__name__)
    CORS(app)
    init_db(app)

    # Import routes after db is initialized
    from routes.auth_routes import auth_bp
    from routes.book_routes import book_bp
    from routes.swap_routes import swap_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(book_bp, url_prefix="/api/books")
    app.register_blueprint(swap_bp, url_prefix="/api/swap-requests")

    return app

if __name__ == "__main__":
    app = create_app()
    PORT = int(os.getenv("PORT", 5001))
    app.run(host="localhost", port=PORT, debug=True)
