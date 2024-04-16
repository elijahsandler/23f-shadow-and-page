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

# Get all current stock
@inventory.route('/current-stock', methods=['GET'])
def get_stock():
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
                ON Inventory.CopyID=p.CopyID \
                WHERE Sale IS NULL) as currentI \
        ON Inventory_Curses.CopyID=currentI.CopyID \
        GROUP BY currentI.CopyID')
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

@inventory.route('/inventory/<copyID>/curses', methods=['POST'])
def add_new_curse(copyID):
    
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)

    #extracting the variable
    curse_id = the_data['curse_id']

    # # Constructing the query
    query = f"insert into inventory_curses (CopyID, CurseID) \
        values ('{copyID}', {curse_id})"

    # executing and committing the post statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return 'Success!'


@inventory.route('/inventory/<copyID>/curses', methods=['DELETE'])
def remove_curse(copyID):
    
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)

    #extracting the variable
    curse_id = the_data['curse_id']

    # # Constructing the query
    query = f"delete from inventory_curses \
        where `CopyID`={copyID} AND `CurseID`={curse_id}"

    # executing and committing the delete statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return 'Success!'


@inventory.route('/inventory/<copyID>/price', methods=['GET'])
def get_copy_pricess(copyID):
    cursor = db.get_db().cursor()
    cursor.execute(
        f'SELECT DateSet, Price \
        FROM Inventory \
        NATURAL JOIN BookPrices \
        WHERE CopyID={copyID} \
        ORDER BY DateSet ASC')
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

@inventory.route('/inventory/<copyID>/price', methods=['POST'])
def add_new_price(copyID):
    
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)

    #extracting the variable
    price = the_data['price']

    # # Constructing the query
    query = f"insert into bookprices (CopyID, Price) \
        values ('{copyID}', {price})"

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return 'Success!'

# add a book to the db
@inventory.route('/inventory', methods=['POST'])
def add_new_copy():
    
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)

    #extracting the variable
    book_id = the_data['book_id']

    # # Constructing the query
    query = f"insert into inventory (BookID) \
        values ('{book_id}')"

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return 'Success!'

@inventory.route('/inventory', methods=['PUT'])
def update_copy():
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)

    #extracting the variable
    book_id = the_data['book_id']
    copy_id = the_data['copy_id']

    # Constructing the query
    query = f'update inventory set `BookID` = "{book_id}" where `CopyID` = {copy_id}'
    current_app.logger.info(query)

    # executing and committing the update statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return 'Success!'

# remove a copy from the database
@inventory.route('/inventory', methods=['DELETE'])
def remove_copy():
    the_data = request.json
    current_app.logger.info(the_data)

    copy_id = the_data['copy_id']

    query = f'delete from books where `CopyID`={copy_id}'
    current_app.logger.info(query)

    # executing and committing the update statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return 'Success!'