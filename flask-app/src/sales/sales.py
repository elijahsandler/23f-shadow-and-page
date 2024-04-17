from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db

sales = Blueprint('sales', __name__)

# Get all sales from the DB
# Andy
@sales.route('/sales', methods=['GET'])
def get_sales():
    cursor = db.get_db().cursor()
    cursor.execute(
        'SELECT * \
        From Sales Order By SaleID;')
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response


@sales.route('/sales/<saleID>', methods=['GET'])
def get_sale(saleID):
    cursor = db.get_db().cursor()
    cursor.execute(f"select * from Sales where SaleID = {saleID}")
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response



@sales.route('/top-sales', methods=['GET'])
def get_top_x_sales():
    cursor = db.get_db().cursor()
    cursor.execute(f"SELECT E.FirstName, E.LastName, E.Position, E.EmployeeID, COUNT(*) AS total_sales From Sales as S \
                   JOIN Employees as E ON E.EmployeeID = S.Employee GROUP BY E.employeeID \
                   ORDER BY COUNT(*) DESC")
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response
    



