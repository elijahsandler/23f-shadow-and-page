from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db

sales = Blueprint('sales', __name__)

# Get all sales from the DB
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
def get_sale_details(saleID):
    cursor = db.get_db().cursor()
    cursor.execute(f"SELECT S.SaleID, I.BookID, I.CopyID, BP.Price, C.CustomerID, C.FirstName, C.LastName, C.Email, \
                    E.EmployeeID, E.Email, E.Position \
                    FROM Sales AS S \
                    JOIN Inventory AS I ON S.SaleID = I.Sale \
                    JOIN Customers C ON S.Customer = C.CustomerID \
                    JOIN Employees AS E ON S.Employee = E.EmployeeID \
                    JOIN ( \
                        SELECT CopyID, MAX(DateSet) AS MaxDate \
                        FROM BookPrices \
                        GROUP BY CopyID \
                    ) AS MaxPrices ON I.CopyID = MaxPrices.CopyID \
                    JOIN BookPrices AS BP ON MaxPrices.CopyID = BP.CopyID AND MaxPrices.MaxDate = BP.DateSet \
                    WHERE S.SaleID = {saleID}")
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
def get_top_sales():
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
    


@sales.route('/top-sales/<EmployeeID>', methods=['GET'])
def employee_sales_info(EmployeeID):
    cursor = db.get_db().cursor()
    cursor.execute(f"SELECT S.SaleID, I.BookID, I.CopyID, BP.Price, C.CustomerID, C.FirstName, C.LastName, C.Email, \
                    E.EmployeeID, E.Email \
                    FROM Sales AS S \
                    JOIN Inventory AS I ON S.SaleID = I.Sale \
                    JOIN Customers AS C ON S.Customer = C.CustomerID \
                    JOIN Employees AS E ON S.Employee = E.EmployeeID \
                    JOIN ( \
                        SELECT CopyID, MAX(DateSet) AS MaxDate \
                        FROM BookPrices \
                        GROUP BY CopyID \
                    ) AS MaxPrices ON I.CopyID = MaxPrices.CopyID \
                    JOIN BookPrices AS BP ON MaxPrices.CopyID = BP.CopyID AND MaxPrices.MaxDate = BP.DateSet \
                    WHERE E.EmployeeID = '{EmployeeID}'")
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

@sales.route('/sales/<saleID>', methods=['POST'])
def add_new_sale(saleID):
    
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)

    # # Constructing the query
    query = f"insert into sales (SaleID) \
        values ('{saleID}')"

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return 'Success!'


@sales.route('/sales', methods=['PUT'])
def update_sale():
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)

    #extracting the variable
    sales_id = the_data['SaleID']
    customer = the_data['Customer']

    # Constructing the query
    query = f'update sales set `Customer` = "{customer}" where `SaleID` = {sales_id}'
    current_app.logger.info(query)

    # executing and committing the update statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return 'Success!'


@sales.route('/sales', methods=['DELETE'])
def remove_sale():
    the_data = request.json
    current_app.logger.info(the_data)

    sale_id = the_data['SaleID']

    query = f'delete from books where `SaleID`={sale_id}'
    current_app.logger.info(query)

    # executing and committing the update statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return 'Success!'