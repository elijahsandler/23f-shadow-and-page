from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db


curses = Blueprint('curses', __name__)

# Get all inventory from the DB
@curses.route('/curse-count', methods=['GET'])
def get_curses_count():
    cursor = db.get_db().cursor()
    cursor.execute(
        'SELECT Curses.Name, COUNT(Curses.CurseID) AS NumCurses\
        FROM Curses \
            JOIN Inventory_Curses \
                ON Curses.CurseID = Inventory_Curses.CurseID\
            JOIN Inventory \
                ON Inventory_Curses.CopyID = Inventory.CopyID\
        WHERE Sale IS NULL\
        GROUP BY (Curses.Name)')
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response


@curses.route('/curses', methods=['GET'])
def get_curses():
    cursor = db.get_db().cursor()
    cursor.execute(
        'SELECT * FROM Curses')
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
@curses.route('/curses', methods=['POST'])
def add_new_curse():
    
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)

    #extracting the variable
    name = the_data['Name']
    effect = the_data['Effect']
    dangerlevel = the_data['DangerLevel']
    description = the_data['Description']
    countercurse = the_data['Countercurse']

    # # Constructing the query
    query = f"insert into books (bookid, title, year, authorfirstname, authorlastname, \
        genreid, publisherid) values ('{name}', {effect}, '{dangerlevel}', '{description}', \
        {countercurse})"

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return 'Success!'


@curses.route('/curses', methods=['DELETE'])
def remove_curse():
    the_data = request.json
    current_app.logger.info(the_data)

    curseid = the_data['curseid']

    query = f'delete from curses where `CurseID`={curseid}'
    current_app.logger.info(query)

    # executing and committing the update statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return 'Success!'


# map of names to curseID for sasha :)
@curses.route('/map', methods=['GET'])
def get_curses_map():
    cursor = db.get_db().cursor()
    cursor.execute(
        'SELECT `CurseId`, `Name` \
        From Curses \
        ORDER BY Name ASC')
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

counter_curses = Blueprint('counter_curses', __name__)

# Get all counter curses inventory from the DB
@counter_curses.route('/counter_curses', methods=['GET'])
def get_counter_curses():
    cursor = db.get_db().cursor()
    cursor.execute(
        'SELECT counter_curses.Name, COUNT(counter_curses.CounterID),\
        counter_curses.Instructions \
        FROM counter_curses \
        GROUP BY (counter_curses.Name)')
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response