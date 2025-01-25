import string
import random
from flask import Flask, redirect, request, jsonify, render_template
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from flask import g
from dotenv import load_dotenv
import os
import unittest
import pymongo


load_dotenv()
# Mongo DB is a NoSQL database
mongodb_uri = os.getenv('MONGODB_URI')
print(f"MongoDB URI: {mongodb_uri}")


def get_db():
    if 'db' not in g:
        g.client = MongoClient(mongodb_uri)
        g.db = g.client['shortener_db']
        g.collection = g.db['urls']  # Similar to the Table in SQL

    return g.collection


# Send a ping to confirm a successful connection
try:
    g.client.admin.command('ping')
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
    return render_template('index.html')


@app.route('/connect')
def connect():
    return jsonify({"message": "CONNECT SUCCESSFULLY"}), 200


@app.route('/shorten', methods=['POST'])
def shorten_url():
    collection = get_db()

    data = request.get_json()

    original_url = data.get('original_url')

    if not original_url:
        return jsonify({"error": "No URL provided"}), 400

    existing_entry = collection.find_one({"original_url": original_url})

    if len(original_url) > 2000:
        return jsonify({"message": "URL too long"}), 400

    if existing_entry:
        return jsonify({"short_url": request.host_url + existing_entry['short_url']})

    short_url = generate_short_url()

    while collection.find_one({"short_url": short_url}):
        short_url = generate_short_url()

    collection.insert_one({"original_url": original_url, "short_url": short_url})

    return jsonify({"short_url": request.host_url + short_url})


@app.route('/<short_url>')
def redirect_to_original(short_url):
    collection = get_db()
    url_entry = collection.find_one({"short_url": short_url})
    if url_entry:
        return redirect(url_entry['original_url'])
    else:
        return jsonify({"error": "URL not found"}), 404


@app.route('/original', methods=['POST'])
def get_original():
    collection = get_db()
    request_original = request.form.get('original')
    custom_short = request.form.get('custom_short_url')

    if not request_original:
        return "Original URL is required", 400

    if request_original:
        if custom_short:
            collection.insert_one({
                'short_url': custom_short,
                'original_url': request_original
            })
            short_url = custom_short  # as long as we press the url i y will auto go to the redirect_to_original function
            return render_template('index.html', short_url=request.host_url + short_url)
        else:
            short_url = generate_short_url()
            collection.insert_one({
                'short_url': short_url,
                'original_url': request_original
            })
        return render_template('index.html', short_url=request.host_url + short_url)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
