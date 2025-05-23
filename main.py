from flask import Flask, request, jsonify, render_template
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
    return render_template('index.html')  # Serve the main HTML page

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if collection.find_one({"username": username}):
        return jsonify({"error": "Username already exists!"}), 400

    collection.insert_one({"username": username, "password": password})
    return jsonify({"message": "User registered successfully!"})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = collection.find_one({"username": username})
    if user and user['password'] == password:
        return jsonify({"message": "Login successful!"})
    else:
        return jsonify({"error": "Invalid username or password!"}), 401

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
