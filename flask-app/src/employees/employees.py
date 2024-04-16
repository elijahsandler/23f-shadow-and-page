from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db


employees = Blueprint('employees', __name__)

# Get all employees from the DB
@employees.route('/employees', methods=['GET'])
def get_employees():
    cursor = db.get_db().cursor()
    cursor.execute(
        'SELECT `employeeID`, `AuthorFirstName`, `AuthorLastName` \
        From Employees \
        ORDER BY employeeID')
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Get employees detail for employees with particular employeesID
@employees.route('/employees/<employeesID>', methods=['GET'])
def get_employees(employeesID):
    cursor = db.get_db().cursor()
    cursor.execute(
        f"SELECT employeesID, Title, Year, AuthorFirstName, AuthorLastName, GenreName, Publisher \
        FROM Employees \
        NATURAL JOIN Genre \
        NATURAL JOIN Publisher \
        WHERE employeesID = '{employeesID}'")
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
@employees.route('/employees', methods=['POST'])
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
    query = f"insert into employees (bookid, title, year, authorfirstname, authorlastname, \
        genreid, publisherid) values ('{book_id}', '{title}', {year}, '{firstname}', '{lastname}', \
        {genre_id}, {publisher_id})"

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return 'Success!'
