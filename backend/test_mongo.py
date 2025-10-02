from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# 🔑 Replace <db_password> with your actual password
uri = "mongodb+srv://mideverything:euBt9SYbXxWJeaan@cluster0.8iq8597.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("✅ Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print("❌ Connection failed:", e)
