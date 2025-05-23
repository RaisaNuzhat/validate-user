from flask import Flask, request, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["user_db"]
collection = db["users"]

@app.route('/')
def home():
    return 'Login API is running!'

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    password = data['password']
    collection.insert_one({"username": username, "password": password})
    return jsonify({"message": "User registered successfully!"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # <-- required for Render
    app.run(host='0.0.0.0', port=port)        # <-- required for Render
