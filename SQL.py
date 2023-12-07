from flask import Flask, jsonify, request
from mainn import *

app = Flask(__name__)

@app.route('/get_book/', methods=['GET'])
def get_book():
    book = get_book()
    return jsonify({'data':book}), 200

@app.route('/create_book/', methods=['POST'])
def create_book_rq():
    data = request.get_json()
    if not data or 'title' not in data or 'author' not in data or 'genre' not in data or 'created_at' not in data:
        return jsonify({'error': 'Missing data'}), 400
    book = ItemPydantic(
        title=data.get('title', '1984'),
        author=data.get('author', 'George Orwell'),
        genre=data.get('genre', 'novel'),
        created_at=data.get('created_at', 1984-10-10)
    )
    return jsonify({"message":"created succesfully"})

@app.route("/retrieve_book/<int:book_id>/", methods=['GET'])
def get_one_book(book_id):
    book = retrieve(book_id)
    if not book:
        return jsonify({'message':'not found'}), 404
    return jsonify({'data':book}), 200

@app.route('/update_book/<int:id>', methods=['PUT'])
def update_book(id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Missing data'}), 400
    return jsonify({'message': 'Данные успешно обновлены'}), 200

@app.route('/delete_book/<int:id>', methods=['DELETE'])
def delete_book(id):
    book = retrieve(id)
    if not book:
        return jsonify({'error': 'Book not found'}), 404
        delete(id)
    return jsonify({'message': 'Данные успешно удалены'}), 200