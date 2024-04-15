from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db


books = Blueprint('books', __name__)

# Get all books from the DB
@books.route('/books', methods=['GET'])
def get_books():
    cursor = db.get_db().cursor()
    cursor.execute(
        'SELECT `BookID`, `Title`, `AuthorFirstName`, `AuthorLastName` \
        From Books \
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

# Get book detail for book with particular bookID
@books.route('/books/<bookID>', methods=['GET'])
def get_book(bookID):
    cursor = db.get_db().cursor()
    cursor.execute(
        f"SELECT BookID, Title, Year, AuthorFirstName, AuthorLastName, GenreName, Publisher \
        From Books \
        NATURAL JOIN Genre \
        NATURAL JOIN Publisher \
        WHERE '{bookID}' IN BookID")
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# add a book to the db
@books.route('/books', methods=['POST'])
def add_new_book():
    
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)

    #extracting the variable
    book_id = the_data['book_id']
    title = the_data['book_title']
    year = the_data['book_year']
    firstname = the_data['book_authorfirstname']
    lastname = the_data['book_authorlastname']
    genre_id = the_data['genre_id']
    publisher_id = the_data['publisher_id']

    # # Constructing the query
    query = f"insert into books (bookid, title, year, authorfirstname, authorlastname, \
        genreid, publisherid) values ('{book_id}', '{title}', {year}, '{firstname}', '{lastname}', \
        {genre_id}, {publisher_id})"

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return 'Success!'

@books.route('/books', methods=['PUT'])
def update_book():
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)

    #extracting the variable
    book_id = the_data['book_id']
    title = the_data['book_title']
    year = the_data['book_year']
    firstname = the_data['book_authorfirstname']
    lastname = the_data['book_authorlastname']
    genre_id = the_data['genre_id']
    publisher_id = the_data['publisher_id']

    # Constructing the query
    query = f'update books set `GenreID` = "{genre_id}", `Title` = "{title}",\
          `Year` = {year}, `AuthorFirstName` = "{firstname}", `AuthorLastName` = "{lastname}", \
            `PublisherID` = {publisher_id} where `BookID` = "{book_id}"'
    current_app.logger.info(query)

    # executing and committing the update statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return 'Success!'

# remove a book from the database
@books.route('/books', methods=['DELETE'])
def remove_book():
    the_data = request.json
    current_app.logger.info(the_data)

    book_id = the_data['book_id']

    query = f'delete from books where `BookID`="{book_id}"'
    current_app.logger.info(query)

    # executing and committing the update statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return 'Success!'

# map of titles to bookIDs for sasha :)
@books.route('/map', methods=['GET'])
def get_book_map():
    cursor = db.get_db().cursor()
    cursor.execute(
        'SELECT `BookID`, `Title` \
        From Books \
        ORDER BY Title ASC')
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response