from flask import Blueprint, request, jsonify, make_response
import json
from src import db


books = Blueprint('books', __name__)

# Get all books from the DB
@books.route('/books', methods=['GET'])
def get_books():
    cursor = db.get_db().cursor()
    cursor.execute(
        'SELECT BookID, Title, Year, AuthorFirstName, AuthorLastName, GenreName, Publisher \
        From Books \
        NATURAL JOIN Genre \
        NATURAL JOIN Publisher \
        ORDER BY BookID')
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Get book detail for book with particular userID
@customers.route('/books/<bookID>', methods=['GET'])
def get_book(bookID):
    cursor = db.get_db().cursor()
    cursor.execute(
        f'SELECT BookID, Title, Year, AuthorFirstName, AuthorLastName, GenreName, Publisher \
        From Books \
        NATURAL JOIN Genre \
        NATURAL JOIN Publisher \
        WHERE bookID={bookID}')
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response