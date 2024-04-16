from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db


curses = Blueprint('curses', __name__)

# Get all inventory from the DB
# ELI
@curses.route('/curses', methods=['GET'])
def get_curses():
    cursor = db.get_db().cursor()
    cursor.execute(
        'SELECT Curses.Name, COUNT(Curses.CurseID)\
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


# add a book to the db
@curses.route('/curses', methods=['POST'])
def add_new_curse():
    
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)

    #extracting the variable
    curseid = the_data['curseid']
    name = the_data['name']
    effect = the_data['effect']
    dangerlevel = the_data['dangerlevel']
    description = the_data['description']
    countercurse = the_data['countercurse']

    # # Constructing the query
    query = f"insert into books (bookid, title, year, authorfirstname, authorlastname, \
        genreid, publisherid) values ('{curseid}', '{name}', {effect}, '{dangerlevel}', '{description}', \
        {countercurse})"

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return 'Success!'