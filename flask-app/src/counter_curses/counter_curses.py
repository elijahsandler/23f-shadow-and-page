from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db


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

