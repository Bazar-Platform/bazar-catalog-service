from dis import CACHE

from flask import Flask, jsonify, request
import os
import requests

app = Flask(__name__)

# Environment variables to identify role and peer
ROLE = os.getenv('ROLE', 'primary')  # 'primary' or 'backup'
PEER_URL = os.getenv('PEER_URL')  # URL of the other node (primary or backup)
CACHE_INVALIDATE_URL = os.getenv('CACHE_INVALIDATE_URL')  # URL of the cache invalidation endpoint

# In-memory data store for books
books = [
    {"Book_ID": 1, "name": "How to get a good grade in DOS in 40 minutes a day", "topic": "distributed systems",
     "stock": 10, "price": 29.99},
    {"Book_ID": 2, "name": "RPCs for Noobs", "topic": "distributed systems", "stock": 15, "price": 29.99},
    {"Book_ID": 3, "name": "Xen and the Art of Surviving Undergraduate School", "topic": "undergraduate school",
     "stock": 5, "price": 29.99},
    {"Book_ID": 4, "name": "Cooking for the Impatient Undergrad", "topic": "undergraduate school", "stock": 50,
     "price": 29.99}
]


# Helper function to find a book by its ID
def find_book_by_id(book_id):
    return next((book for book in books if book["Book_ID"] == book_id), None)


# Endpoint to retrieve all books
@app.route('/books', methods=['GET'])
def get_books():
    return jsonify(books), 200


# Endpoint to query books by topic
@app.route('/search/<topic>', methods=['GET'])
def query_by_subject(topic):
    filtered_books = [book for book in books if book["topic"] == topic]
    return jsonify(filtered_books), 200


# Endpoint to query a book by its item number (Book_ID)
@app.route('/info/<int:Book_ID>', methods=['GET'])
def query_by_item(Book_ID):
    book = find_book_by_id(Book_ID)
    if book:
        return jsonify(book), 200
    else:
        return jsonify({'error': 'Item not found'}), 404


# Endpoint to update book details (price or stock)
@app.route('/items/<int:Book_ID>', methods=['PUT'])
def update_item(Book_ID):
    data = request.json
    new_price = data.get('price')
    new_stock = data.get('stock')

    book = find_book_by_id(Book_ID)
    if not book:
        return jsonify({'error': 'Item not found'}), 404

    # If the node is the backup, forward the request to the primary
    if ROLE == 'backup':
        if not PEER_URL:
            return jsonify({'error': 'Primary URL not configured'}), 500

        try:
            response = requests.put(f"{PEER_URL}/items/{Book_ID}", json=data)
            return response.json(), response.status_code
        except Exception as e:
            return jsonify({'error': 'Failed to communicate with primary', 'details': str(e)}), 500

    # If the node is the primary, update the local database and notify the backup
    if new_price is not None:
        book['price'] = new_price
    if new_stock is not None:
        book['stock'] = new_stock

    # Invalidate the cache
    notify_cache_invalidation(f"info:{Book_ID}")

    # Notify the backup
    if PEER_URL:
        try:
            requests.put(f"{PEER_URL}/replica-update/{Book_ID}", json=data)
        except Exception as e:
            print(f"Warning: Failed to notify backup - {e}")

    return jsonify({'message': 'Item updated successfully'}), 200


# Notify gateway to invalidate cache
def notify_cache_invalidation(key):
    if not CACHE_INVALIDATE_URL:
        return
    try:
        response = requests.post(CACHE_INVALIDATE_URL, json={"key": key})
        print(f"Cache invalidation response: {response.status_code}")
    except Exception as e:
        print(f"Failed to notify cache invalidation: {e}")


# Endpoint for the primary to send updates to the backup
@app.route('/replica-update/<int:Book_ID>', methods=['PUT'])
def replica_update(Book_ID):
    if ROLE != 'backup':
        return jsonify({'error': 'Only the backup can accept replica updates'}), 403

    data = request.json
    new_price = data.get('price')
    new_stock = data.get('stock')

    book = find_book_by_id(Book_ID)
    if not book:
        return jsonify({'error': 'Item not found'}), 404

    # Update the database
    if new_price is not None:
        book['price'] = new_price
    if new_stock is not None:
        book['stock'] = new_stock

    return jsonify({'message': 'Replica updated successfully'}), 200


# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
