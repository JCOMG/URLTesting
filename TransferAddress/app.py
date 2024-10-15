import string
import random
from flask import Flask, redirect, request, jsonify
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://jimmy1999928:jSY6uCyvNr1aayCs@testing.s9jl8.mongodb.net/?retryWrites=true&w=majority&appName=Testing"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

db = client['shortener_db']
collection = db['urls']

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

app = Flask(__name__)


def generate_short_url(length=6):
    characters = string.ascii_letters + string.digits
    short_url = ''

    for _ in range(length):  # we do not care about the variable in for loop, so we use _
        short_url += random.choice(characters)

    return short_url


@app.route('/health', methods=['GET', 'POST'])
def health():
    return "ok"

@app.route('/')
def index():
    return jsonify({"message": "Welcome ~"}), 200

@app.route('/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()

    original_url = data.get('original_url')

    if not original_url:
        return jsonify({"error": "No URL provided"}), 400

    existing_entry = collection.find_one({"original_url": original_url})

    if existing_entry:
        return jsonify({"short_url": request.host_url + existing_entry['short_url']})

    short_url = generate_short_url()

    while collection.find_one({"short_url": short_url}):
        short_url = generate_short_url()

    collection.insert_one({"original_url": original_url, "short_url": short_url})

    return jsonify({"short_url": request.host_url + short_url})


@app.route('/<short_url>')
def redirect_to_original(short_url):
    url_entry = collection.find_one({"short_url": short_url})
    if url_entry:
        return redirect(url_entry['original_url'])
    else:
        return jsonify({"error": "URL not found"}), 404


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
