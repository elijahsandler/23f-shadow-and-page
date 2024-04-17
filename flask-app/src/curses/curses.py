from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db


curses = Blueprint('curses', __name__)

# Get all inventory from the DB
@curses.route('/curse-count', methods=['GET'])
def get_curses_count():
    cursor = db.get_db().cursor()
    cursor.execute(
        'SELECT Curses.CurseId, Curses.Name, COUNT(Curses.CurseID) AS NumUses\
        FROM Curses \
            JOIN Inventory_Curses \
                ON Curses.CurseID = Inventory_Curses.CurseID\
            JOIN Inventory \
                ON Inventory_Curses.CopyID = Inventory.CopyID\
        WHERE Sale IS NULL\
        GROUP BY Curses.CurseId, Curses.Name')
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response


@curses.route('/curses/<curseID>', methods=['GET'])
def get_curse_inventory_info(curseID):
    cursor = db.get_db().cursor()
    cursor.execute(
        f"SELECT c.CurseID, c.Name, c.DangerLevel, i.BookID, i.CopyID, i.Sale, b.Title \
            FROM Curses c \
                JOIN Inventory_Curses ic ON c.CurseID = ic.CurseID \
                JOIN shadow.Inventory i on ic.CopyID = i.CopyID \
                JOIN Books b ON i.BookID = b.BookID \
            WHERE c.CurseID = {curseID}")
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
    curseid = the_data['CurseID']
    name = the_data['Name']
    effect = the_data['Effect']
    dangerlevel = the_data['DangerLevel']
    description = the_data['Description']
    countercurse = the_data['Countercurse']

    # # Constructing the query
    query = f"insert into Curses (CurseID, Name, Effect, DangerLevel, Description, \
        CounterCurse) values ('{curseid}', '{name}', '{effect}', '{dangerlevel}', '{description}', \
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


# Get all counter curses inventory from the DB
@curses.route('/counter-curses', methods=['GET'])
def get_counter_curses():
    cursor = db.get_db().cursor()
    cursor.execute(
        'SELECT * FROM CounterCurses')
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response


@curses.route('/counter-curses-count', methods=['GET'])
def get_counter_curses_count():
    cursor = db.get_db().cursor()
    cursor.execute(
        'SELECT counter_curses.Name, COUNT(counter_curses.CounterID),\
        counter_curses.Instructions \
        FROM countercurses \
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


@curses.route('/projects', methods=['GET'])
def get_projects():
    cursor = db.get_db().cursor()
    cursor.execute(
        'SELECT * FROM Projects')
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response


@curses.route('/projects/<projectID>', methods=['GET'])
def get_project_info(projectID):
    cursor = db.get_db().cursor()
    cursor.execute(
        f'SELECT p.ProjectID, p.ProjectName, c.CurseID, Name, DangerLevel, EmployeeID, DateJoined, DateLeft \
        FROM Projects p \
        JOIN ResearchCurseIDs rci ON p.ProjectID = rci.ProjectID \
        JOIN Curses c ON rci.ResearchCurseID = c.CurseID \
        JOIN Employees_Projects ep on p.ProjectID = ep.ProjectID \
        WHERE p.ProjectID = {projectID}')
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

@curses.route('/employee-projects', methods=['GET'])
def emp_projects():
    cursor = db.get_db().cursor()
    cursor.execute(
        'SELECT COUNT(DISTINCT p.ProjectID) AS NumProjects,EmployeeID \
        FROM Projects p \
            JOIN ResearchCurseIDs rci ON p.ProjectID = rci.ProjectID \
            JOIN Curses c ON rci.ResearchCurseID = c.CurseID \
            JOIN Employees_Projects ep on p.ProjectID = ep.ProjectID \
         GROUP BY EmployeeID')
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response


@curses.route('/employee-projects/<employeeID>', methods=['GET'])
def get_employee_project_info(employeeID):
    cursor = db.get_db().cursor()
    cursor.execute(
        f"SELECT p.ProjectID, p.ProjectName, c.CurseID, Name, DangerLevel, EmployeeID, DateJoined, DateLeft \
        FROM Projects p \
        JOIN ResearchCurseIDs rci ON p.ProjectID = rci.ProjectID \
        JOIN Curses c ON rci.ResearchCurseID = c.CurseID \
        JOIN Employees_Projects ep on p.ProjectID = ep.ProjectID \
        WHERE ep.EmployeeID = '{employeeID}'")
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response