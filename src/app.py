from flask import Flask, jsonify, request

app = Flask(__name__)

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

    # Update item details
    if new_price is not None:
        book['price'] = new_price
    if new_stock is not None:
        book['stock'] = new_stock

    return jsonify({'message': 'Item updated successfully'}), 200


# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
