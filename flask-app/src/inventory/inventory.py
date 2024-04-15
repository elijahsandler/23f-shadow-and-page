from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db


inventory = Blueprint('inventory', __name__)

# Get all inventory from the DB
@inventory.route('/inventory', methods=['GET'])
def get_inventory():
    cursor = db.get_db().cursor()
    cursor.execute(
        'SELECT CopyID, BookID, Sale \
        From Inventory \
        ORDER BY CopyID')
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
@inventory.route('/inventory/<copyID>', methods=['GET'])
def get_copy(copyID):
    cursor = db.get_db().cursor()
    cursor.execute(
        f'SELECT BookID, Title, currentI.CopyID, Price, COUNT(Inventory_Curses.CurseID) as NumCurses \
        FROM Inventory_Curses \
        RIGHT OUTER JOIN (SELECT BookID, Title, Inventory.CopyID, Price \
            FROM Books \
            NATURAL JOIN Inventory \
            JOIN (SELECT CopyID, Price \
                FROM BookPrices \
                JOIN (SELECT CopyID as cID, MAX(BookPrices.DateSet) as ds \
                FROM BookPrices \
                GROUP BY CopyID) as c \
                ON CopyID=cID AND ds=DateSet) as p \
            ON Inventory.CopyID=p.CopyID) as currentI \
        ON Inventory_Curses.CopyID=currentI.CopyID \
        GROUP BY currentI.CopyID \
        HAVING CopyID = {copyID}')
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

@inventory.route('/inventory/<copyID>/curses', methods=['GET'])
def get_copy_curses(copyID):
    cursor = db.get_db().cursor()
    cursor.execute(
        f'SELECT CurseID, Name, DangerLevel, Description \
        FROM Inventory_Curses \
        NATURAL JOIN Inventory \
        NATURAL JOIN Curses \
        WHERE CopyID = {copyID} \
        ORDER BY DangerLevel DESC')
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

############################################################

# # add a book to the db
# @books.route('/books', methods=['POST'])
# def add_new_book():
    
#     # collecting data from the request object 
#     the_data = request.json
#     current_app.logger.info(the_data)

#     #extracting the variable
#     book_id = the_data['book_id']
#     title = the_data['book_title']
#     year = the_data['book_year']
#     firstname = the_data['book_authorfirstname']
#     lastname = the_data['book_authorlastname']
#     genre_id = the_data['genre_id']
#     publisher_id = the_data['publisher_id']

#     # # Constructing the query
#     query = f"insert into books (bookid, title, year, authorfirstname, authorlastname, \
#         genreid, publisherid) values ('{book_id}', '{title}', '{year}', '{firstname}', '{lastname}', \
#         '{genre_id}', '{publisher_id}')"

#     # executing and committing the insert statement 
#     cursor = db.get_db().cursor()
#     cursor.execute(query)
#     db.get_db().commit()
    
#     return 'Success!'

# @books.route('/books', methods=['PUT'])
# def update_book():
#     # collecting data from the request object 
#     the_data = request.json
#     current_app.logger.info(the_data)

#     #extracting the variable
#     book_id = the_data['book_id']
#     title = the_data['book_title']
#     year = the_data['book_year']
#     firstname = the_data['book_authorfirstname']
#     lastname = the_data['book_authorlastname']
#     genre_id = the_data['genre_id']
#     publisher_id = the_data['publisher_id']

#     # Constructing the query
#     query = f'update books set `GenreID` = "{genre_id}", `Title` = "{title}",\
#           `Year` = {year}, `AuthorFirstName` = "{firstname}", `AuthorLastName` = "{lastname}", \
#             `PublisherID` = "{publisher_id}" where `BookID` = {book_id}'
#     current_app.logger.info(query)

#     # executing and committing the update statement 
#     cursor = db.get_db().cursor()
#     cursor.execute(query)
#     db.get_db().commit()
    
#     return 'Success!'

# # remove a book from the database
# @books.route('/books', methods=['DELETE'])
# def remove_book():
#     the_data = request.json
#     current_app.logger.info(the_data)

#     book_id = the_data['book_id']

#     query = f'delete from books where `BookID`={book_id}'
#     current_app.logger.info(query)

#     # executing and committing the update statement 
#     cursor = db.get_db().cursor()
#     cursor.execute(query)
#     db.get_db().commit()
    
#     return 'Success!'