from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db import connection
import datetime
import math

def response_obj(success=False, message="", data={}):
    """This function returns a generic response object.
    """
    _response = {
        'success': success,
        'message': message,
        'data': data
    }
    
    return _response

# Create your views here.

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]
    
def _table_add_row(table_name, headers, data):
    header_line = ', '.join(headers)
    
    for header in headers:
        if header == 'id':
            continue
        
        if header == 'active':
            if data[header] == '0':
                data[header] = 0
            else:
                data[header] = 1
    
    data_line = ', '.join([f"{data[header]}" if type(data[header])==int else f"'{data[header]}'" for header in headers])
    
    query = f"INSERT INTO {table_name} ({header_line}) VALUES ({data_line})"
    
    with connection.cursor() as cursor:
        cursor.execute(query)
        
    
def _get_table_headers(cursor):
    column_headers = [col[0] for col in cursor.description]
        
    return column_headers
    
def _get_table_data(cursor):
    rows = cursor.fetchall()

    return [*rows]

def _get_table_types(headers, data):
    types = []
    
    """Types:
    id ; int ; bool ; float ; str ; datetime ; N/A 
    """
    for col in range(len(headers)):
        t = type(data[col])
        
        if t == int:
            if headers[col] == 'id':
                types.append('id')
            elif headers[col] == 'active':
                types.append('bool')
            else:
                types.append('int')
        elif t == float:
            types.append('float')
        elif t == str:
            types.append('str')
        elif t == datetime.datetime:
            types.append('datetime')
        else:
            types.append('N/A')
        
    return types

def _get_table_response(table_name=None, start=None, quantity=None, query=None):
    """This function will generate a response for the table specified by table_name.
    
    Args:
        table_name (str): The name of the table to query.
        start (int): The first row to return.
        quantity (int): The number of rows to return.
        query (str): The query to execute.
        
    Returns:
        headers (list): A list of the table headers.
        data (list): A list of lists containing the data.
        data_types (list): A list of the data types for each column.
    """
    response = response_obj()
    
    # There needs to be a table_name or query
    if query is None and table_name is None:
        response['success'] = False
        response['message'] = "Missing table_name or query."
        return response
        
    with connection.cursor() as cursor:
        # Tables -> Columns
        # Users -> id, username, password, active
        # Transaction_Types -> id, description
        # Transactions -> id, user_id, transaction_type_id, stock_id, quatity, date
        # Stock -> id, description, quantity
        if query is None:
            if table_name == 'users':
                query = (
                    "SELECT users.id, username, password, active " +
                    "FROM users"
                )
                headers = ['id', 'username', 'password', 'active']
                
            elif table_name == 'transaction_types':
                query = (
                    "SELECT transaction_types.id, description " +
                    "FROM transaction_types"
                )
                headers = ['id', 'description']
                
            elif table_name == 'transactions':
                query = (
                    "SELECT transactions.id, users.username AS user, transaction_types.description, stock.description, transactions.quantity, date " +
                    "FROM transactions " +
                    "LEFT JOIN users ON transactions.user_id = users.id " +
                    "LEFT JOIN transaction_types ON transactions.transaction_type_id = transaction_types.id " +
                    "LEFT JOIN stock ON transactions.stock_id = stock.id"
                )
                headers = ['id', 'user', 'transaction_type', 'stock', 'quantity', 'date']
                
            elif table_name == 'stock':
                query = ( 
                    "SELECT stock.id, description, quantity " +
                    "FROM stock"
                )
                headers = ['id', 'description', 'quantity']
                
            else:
                response['success'] = False
                response['message'] = f"Table {table_name} does not exist."
                return response
            
            cursor.execute(query)
        else:
            query = query
            cursor.execute(query)
            headers = _get_table_headers(cursor)
            
        data = _get_table_data(cursor)
        number_of_rows = len(data)
        
        # If there is no data, only return headers
        if number_of_rows == 0:
            response['success'] = True
            response['message'] = "No data."
            response['data'] = {
                'headers': headers,
            }
            return response
        
        if start is not None:
            if start < 0:
                start = 0
            
            if start >= len(data):
                response['success'] = False
                response['message'] = "Start is greater than the number of rows."
                return response
            
            if quantity is None:
                data = data[start:]
            else:
                if quantity < 0:
                    quantity = 0
                data = data[start:start+quantity]
        
        types = _get_table_types(headers, data[0])
        
    response['success'] = True
    response['message'] = "Successfully retrieved table data."
    response['data'] = {
        'headers': headers,
        'data': data,
        'types': types,
        'info': {
            'number_of_rows': number_of_rows,
            'start': start,
            'quantity': quantity,
            'total_pages': math.ceil(number_of_rows / quantity) if quantity is not None else None,
            'current_page': math.ceil(start / quantity)+1 if quantity is not None else None,
        }
    }
    return response


# ##############################################################################################################################################################
# def get_table(request, table):
#     return _get_table_response(table_name=table)
    
# def get_table_element(request, table, start):
#     return _get_table_response(table_name=table, start=start)
    
# def get_table_elements(request, table, start, quantity):
#     print(_get_table_response(table_name='transactions'))
    
#     return _get_table_response(table_name=table, start=start, quantity=quantity)


# def update_table_element(request, table, id, column, data_type, new_value):
    
#     try:
#         if data_type == 'int':
#             new_value = int(new_value)
#         elif data_type == 'float':
#             new_value = float(new_value)
#         elif data_type == 'bool':
#             new_value = False if new_value == '0' else True
#         elif data_type == 'str':
#             new_value = str(new_value)
#         elif data_type == 'datetime':
#             new_value = datetime.datetime.strptime(new_value, '%Y-%m-%d %H:%M:%S')
#         else:
#             print("Error: type not recognized.")
#             return JsonResponse({}, safe=False)
#     except:
#         print("Error: could not convert new_value to type.")
#         return JsonResponse({}, safe=False)
    
#     try:
#         query = f"UPDATE {table} SET {column} = %s WHERE id = %s"
#         with connection.cursor() as cursor:
#             cursor.execute(query, [new_value, id])
            
#         if type(new_value) == datetime.datetime:
#             new_value = new_value.strftime('%Y-%m-%d %H:%M:%S')
#         elif type(new_value) == bool:
#             new_value = 1 if new_value else 0
#         else:
#             new_value = str(new_value)
            
#         return JsonResponse({
#             'new_value': new_value    
#         }, safe=False)
#     except Exception as e:
#         print("Error: Could not update table element.")
#         print(e)
#         return JsonResponse({}, safe=False)
    
    
# def get_dash_info(request):
#     query = """
#         SELECT id, description, quantity
#         FROM stock
#     """
    
#     with connection.cursor() as cursor:
#         cursor.execute(query)
        
#         headers = ['id', 'description', 'quantity']
#         data = _get_table_data(cursor)
        
#     return JsonResponse({
#         'headers': headers,
#         'data': data 
#     }, safe=False)   
    
# def get_issue(request, start, quantity):
#     """
#     SELECT transaction.id, users.username, transaction_types.description, stock.description, transaction.quantity, transaction.date
#     FROM transactions
#     LEFT JOIN users ON transactions.user_id = users.id
#     LEFT JOIN transaction_types ON transactions.transaction_type_id = transaction_types.id
#     LEFT JOIN stock ON transactions.stock_id = stock.id
#     WHERE transaction.transaction_type_id = 2
#     """
#     query = "SELECT transactions.id, users.username, transaction_types.description AS transaction_type, stock.description AS stock, transactions.quantity, transactions.date FROM transactions LEFT JOIN users ON transactions.user_id = users.id LEFT JOIN transaction_types ON transactions.transaction_type_id = transaction_types.id LEFT JOIN stock ON transactions.stock_id = stock.id"
#     response = _get_table_response(query=query, start=start, quantity=quantity)
    
#     return response

# def get_log(request):
#     query = "SELECT transactions.id, users.username, transaction_types.description AS transaction_type, stock.description AS stock, transactions.quantity, transactions.date FROM transactions LEFT JOIN users ON transactions.user_id = users.id LEFT JOIN transaction_types ON transactions.transaction_type_id = transaction_types.id LEFT JOIN stock ON transactions.stock_id = stock.id"
#     response = _get_table_response(query=query)
    
#     return response

# def get_form_data(request, form):
#     if form == 'issue':
#         query_users = "SELECT id, username FROM users WHERE active = 1"
#         query_stock = "SELECT id, description FROM stock"
#         query_transaction_types = "SELECT id, description FROM transaction_types"
        
#         with connection.cursor() as cursor:
#             cursor.execute(query_users)
#             users = _get_table_data(cursor)
            
#             cursor.execute(query_stock)
#             stock = _get_table_data(cursor)
            
#             cursor.execute(query_transaction_types)
#             transaction_types = _get_table_data(cursor)
            
#         return JsonResponse({
#             'users': users,
#             'stock': stock,
#             'transaction_types': transaction_types
#         }, safe=False)
        
#     else:
#         return JsonResponse({
#             'alert': f"Unknown form, {form}"    
#         }, safe=False)
        
# def addNewStock(stock_name):
#     query = f"INSERT INTO stock (description, quantity) VALUES ('{stock_name}', 0)"
#     with connection.cursor() as cursor:
#         cursor.execute(query)
        
#     query = f"SELECT id FROM stock WHERE description = '{stock_name}'"
#     with connection.cursor() as cursor:
#         cursor.execute(query)
#         data = _get_table_data(cursor)
    
#     return data[0][0]
        
# def add_transaction(request, user_id, transaction_type, stock_id, quantity):
#     try:
#         user_id = int(user_id)
#         transaction_type = int(transaction_type)
#         quantity = int(quantity)
#     except:
#         return JsonResponse({
#             'alert': "Invalid input data types.",
#         }, safe=False)
        
#     # Stock can only be negative if its a correction
#     if quantity <= 0 and transaction_type != 4:
#         return JsonResponse({
#             'alert': "Quantity must be greater than 0.",
#         }, safe=False)
        
#     # Validation
#     query = f"SELECT id FROM users WHERE id = {user_id}"
#     with connection.cursor() as cursor:
#         cursor.execute(query)
#         data = _get_table_data(cursor)
#         if len(data) == 0:
#             return JsonResponse({
#                 'alert': f"User with id {user_id} does not exist.",
#             }, safe=False)
        
#     query = f"SELECT id FROM transaction_types WHERE id = {transaction_type}"
#     with connection.cursor() as cursor:
#         cursor.execute(query)
#         data = _get_table_data(cursor)
#         if len(data) == 0:
#             return JsonResponse({
#                 'alert': f"Transaction type with id {transaction_type} does not exist.",
#             }, safe=False)
        
#     query = f"SELECT id FROM stock WHERE id = {stock_id}"
#     with connection.cursor() as cursor:
#         cursor.execute(query)
#         data = _get_table_data(cursor)
#         if len(data) == 0:
#             return JsonResponse({
#                 'alert': f"Stock with id {stock_id} does not exist.",
#             }, safe=False)
        
#     # Add transaction
#     return log_transaction(user_id, transaction_type, stock_id, quantity)


# def log_transaction(user_id, transaction_type_id, stock_id, quantity):
#     currect_quantity = None
#     query = f"SELECT quantity FROM stock WHERE id = {stock_id}"
#     with connection.cursor() as cursor:
#         cursor.execute(query)
#         data = _get_table_data(cursor)
#         currect_quantity = data[0][0]
    
#     # Add Stock
#     if transaction_type_id == 1:
#         query = f"UPDATE stock SET quantity = quantity + {quantity} WHERE id = {stock_id}"
#         with connection.cursor() as cursor:
#             cursor.execute(query)
    
#     # Personal Use
#     elif transaction_type_id == 2:
#         if currect_quantity - quantity < 0:
#             return JsonResponse({
#                 'alert': f"Not enough stock to complete transaction.",
#             }, safe=False)
            
#         query = f"UPDATE stock SET quantity = quantity - {quantity} WHERE id = {stock_id}"
#         with connection.cursor() as cursor:
#             cursor.execute(query)
        
#     # Loss
#     elif transaction_type_id == 3:
#         if currect_quantity - quantity < 0:
#             return JsonResponse({
#                 'alert': f"Not enough stock to complete transaction.",
#             }, safe=False)
            
#         query = f"UPDATE stock SET quantity = quantity - {quantity} WHERE id = {stock_id}"
#         with connection.cursor() as cursor:
#             cursor.execute(query)
    
#     # Correction
#     elif transaction_type_id == 4:
#         if currect_quantity + quantity < 0:
#             return JsonResponse({
#                 'alert': f"Not enough stock to complete transaction.",
#             }, safe=False)
        
#         query = f"UPDATE stock SET quantity = quantity + {quantity} WHERE id = {stock_id}"
#         with connection.cursor() as cursor:
#             cursor.execute(query)
    
#     # Sell
#     elif transaction_type_id == 5:
#         if currect_quantity - quantity < 0:
#             return JsonResponse({
#                 'alert': f"Not enough stock to complete transaction.",
#             }, safe=False)
            
#         query = f"UPDATE stock SET quantity = quantity - {quantity} WHERE id = {stock_id}"
#         with connection.cursor() as cursor:
#             cursor.execute(query)
    
#     else:
#         return JsonResponse({
#             'alert': f"Transaction type with id {transaction_type_id} does not exist.",
#         }, safe=False)
    
#     query = f"INSERT INTO transactions (user_id, transaction_type_id, stock_id, quantity, date) VALUES ({user_id}, {transaction_type_id}, {stock_id}, {quantity}, NOW())"
#     with connection.cursor() as cursor:
#         cursor.execute(query)
        
#     return JsonResponse({}, safe=False)

# def add_row(request, table_name):
#     if request.method != 'POST':
#         return JsonResponse({
#             'alert': "Invalid request method."
#         }, safe=False)
        
#     data = request.POST
    
#     with connection.cursor() as cursor:
#         query = f"SELECT * FROM {table_name}"
#         cursor.execute(query)
#         headers = _get_table_headers(cursor)
        
#     headers.remove('id')
        
#     row_data = {}
#     for header in headers:
#         if header == 'id':
#             continue
        
#         if header not in data:
#             return JsonResponse({
#                 'alert': f"Missing data for {header}."
#             }, safe=False)
        
#         row_data[header] = data[header]   
    
#     _table_add_row(table_name, headers, row_data)
   
#     return JsonResponse({}, safe=False)
# ##############################################################################################################################################################



def insert(request, table_name):
    """This function will insert a new row into the table specified by table_name.
    method: POST
    data: {
        <column_name>: <value>,
    }

    Args:
        table_name (str): The table name to insert into.
    """
    response = response_obj()
    
    if request.method != 'POST':
        response['success'] = False
        response['message'] = "Invalid request method."
        
        return JsonResponse(response, safe=False)
    
    post_data = request.POST
    
    # Get table headers (remove id)
    with connection.cursor() as cursor:
        query = f"SELECT * FROM {table_name}"
        cursor.execute(query)
        table_headers = _get_table_headers(cursor)
    table_headers.remove('id')
    
    new_row = {}
    for header in table_headers:
        if header not in post_data:
            response['success'] = False
            response['message'] = f"Missing data for {header}."
            
            return JsonResponse(response, safe=False)
        
        new_row[header] = post_data[header]
        
    _table_add_row(table_name, table_headers, new_row)
    
    response['success'] = True
    response['message'] = "Successfully inserted row."
    
    return JsonResponse(response, safe=False)
    

def newLog(request):
    response = response_obj()
    
    if request.method != "POST":
        response['success'] = False
        response['message'] = "Invalid request method."
        
        return JsonResponse(response, safe=False)
    
    post_data = request.POST
    
    try:
        user_id = int(post_data['user_id'])
        transaction_type_id = int(post_data['transaction_type_id'])
        stock_id = int(post_data['stock_id'])
        quantity = int(post_data['quantity'])
    except Exception as e:
        print(e)
        response['success'] = False
        response['message'] = "Invalid data types."
        return JsonResponse(response, safe=False)
    
    currect_quantity = None
    query = f"SELECT quantity FROM stock WHERE id = {stock_id}"
    with connection.cursor() as cursor:
        cursor.execute(query)
        data = _get_table_data(cursor)
        currect_quantity = data[0][0]
        
    # Add Stock
    if transaction_type_id == 1:
        query = f"UPDATE stock SET quantity = quantity + {quantity} WHERE id = {stock_id}"
        with connection.cursor() as cursor:
            cursor.execute(query)
    
    # Personal Use
    elif transaction_type_id == 2:
        if currect_quantity - quantity < 0:
            response['success'] = False
            response['message'] = "Not enough stock to complete transaction."
            return JsonResponse(response, safe=False)
            
        query = f"UPDATE stock SET quantity = quantity - {quantity} WHERE id = {stock_id}"
        with connection.cursor() as cursor:
            cursor.execute(query)
        
    # Loss
    elif transaction_type_id == 3:
        if currect_quantity - quantity < 0:
            response['success'] = False
            response['message'] = "Not enough stock to complete transaction."
            return JsonResponse(response, safe=False)
            
        query = f"UPDATE stock SET quantity = quantity - {quantity} WHERE id = {stock_id}"
        with connection.cursor() as cursor:
            cursor.execute(query)
    
    # Correction
    elif transaction_type_id == 4:
        if currect_quantity + quantity < 0:
            response['success'] = False
            response['message'] = "Not enough stock to complete transaction."
            return JsonResponse(response, safe=False)
        
        query = f"UPDATE stock SET quantity = quantity + {quantity} WHERE id = {stock_id}"
        with connection.cursor() as cursor:
            cursor.execute(query)
    
    # Sell
    elif transaction_type_id == 5:
        if currect_quantity - quantity < 0:
            response['success'] = False
            response['message'] = "Not enough stock to complete transaction."
            return JsonResponse(response, safe=False)
            
        query = f"UPDATE stock SET quantity = quantity - {quantity} WHERE id = {stock_id}"
        with connection.cursor() as cursor:
            cursor.execute(query)
    
    else:
        response['success'] = False
        response['message'] = f"Transaction type with id {transaction_type_id} does not exist."
        return JsonResponse(response, safe=False)
    
    query = f"INSERT INTO transactions (user_id, transaction_type_id, stock_id, quantity, date) VALUES ({user_id}, {transaction_type_id}, {stock_id}, {quantity}, NOW())"
    with connection.cursor() as cursor:
        cursor.execute(query)
        
    response['success'] = True
    response['message'] = "Successfully logged transaction."
    
    return JsonResponse(response, safe=False)
    

def update(request, table_name):
    """This function will update a table element. This is mainly used by the EditTable component.
    method: POST
    data {
        column: <column_name>,
        id: <row id>,
        data_type: <column data type>,
        new_value: <new value>,
    }

    Args:
        table_name (str): Name of the table to update.
        
    Returns:
        new_value (str): The new value of the table element.
    """
    response = response_obj()
    
    if request.method != 'POST':
        response['success'] = False
        response['message'] = "Invalid request method."
        
        return JsonResponse(response, safe=False)
    
    if (
        'column' not in request.POST 
        or 'id' not in request.POST
        or 'data_type' not in request.POST
        or 'new_value' not in request.POST
        ):
        response['success'] = False
        response['message'] = "Missing data."
        
        return JsonResponse(response, safe=False)
        
    data_type = request.POST['data_type']
    column = request.POST['column']
    id = request.POST['id']
    new_value = request.POST['new_value']
        
    # Convert value to correct type
    try:
        if data_type == 'int':
            new_value = int(new_value)
        elif data_type == 'float':
            new_value = float(new_value)
        elif data_type == 'bool':
            new_value = False if new_value == '0' else True
        elif data_type == 'str':
            new_value = str(new_value)
        elif data_type == 'datetime':
            new_value = datetime.datetime.strptime(new_value, '%Y-%m-%d %H:%M:%S')
        else:
            response['success'] = False
            response['message'] = "Type not recognized."
            return JsonResponse(response, safe=False)
    except Exception as e:
        print(e)
        response['success'] = False
        response['message'] = "Could not convert new_value to type."
        return JsonResponse(response, safe=False)
    
    # Update table
    try:
        with connection.cursor() as cursor:
            query = f"UPDATE {table_name} SET {column} = %s WHERE id = %s"
            cursor.execute(query, [new_value, id])
            
        if type(new_value) == datetime.datetime:
            new_value = new_value.strftime('%Y-%m-%d %H:%M:%S')
        elif type(new_value) == bool:
            new_value = 1 if new_value else 0
        else:
            new_value = str(new_value)
            
        response['success'] = True
        response['message'] = "Successfully updated table element."
        response['data'] = {
            'new_value': new_value
        }
        
        return JsonResponse(response, safe=False)
    except Exception as e:
        print(e)
        
        response['success'] = False
        response['message'] = "Could not update table element."
        return JsonResponse(response, safe=False)


def getDashboard(request):
    """This function will return the data needed to lead the dashboard page.
    method: GET
    
    Returns:
        headers (list): A list of the table headers.
        data (list): A list of lists containing the data.
    """
    response = response_obj()
    
    with connection.cursor() as cursor:
        query = "SELECT id, description, quantity FROM stock"
        cursor.execute(query)
        headers = ['id', 'description', 'quantity']
        data = _get_table_data(cursor)
        
    response['success'] = True
    response['message'] = "Successfully retrieved dashboard data."
    response['data'] = {
        'headers': headers,
        'data': data
    }

    return JsonResponse(response, safe=False)


def getIssue(request, start, quantity):
    """This function will return the data needed to load the issue page table.
    This table is paginated.
    method: GET

    Args:
        request (_type_): _description_
        start (int): The first row to return.
        quantity (int): The number of rows to return.
        
    Returns:
        headers (list): A list of the table headers.
        data (list): A list of lists containing the data.
        data_types (list): A list of the data types for each column.
    """
    response = response_obj()
    
    # SELECT 
    #   transaction.id, users.username, 
    #   transaction_types.description AS transaction_type, 
    #   stock.description AS stock_type, transaction.quantity, transaction.date
    # FROM transactions
    # LEFT JOIN users ON transactions.user_id = users.id
    # LEFT JOIN transaction_types ON transactions.transaction_type_id = transaction_types.id
    # LEFT JOIN stock ON transactions.stock_id = stock.id
    query = (
        "SELECT transactions.id, users.username, " + 
            "transaction_types.description AS transaction_type, " + 
            "stock.description AS stock, transactions.quantity, " +
            "transactions.date " +
        "FROM transactions " +
        "LEFT JOIN users ON transactions.user_id = users.id " +
        "LEFT JOIN transaction_types ON transactions.transaction_type_id = transaction_types.id " +
        "LEFT JOIN stock ON transactions.stock_id = stock.id"
    )
    
    return JsonResponse(_get_table_response(query=query, start=start, quantity=quantity), safe=False)
    
    
def getLogs(request):
    """This function will return the entire log table.
    method: GET

    Returns:
        headers (list): A list of the table headers.
        data (list): A list of lists containing the data.
        data_types (list): A list of the data types for each column.
    """
    query = (
        "SELECT transactions.id, users.username, " + 
            "transaction_types.description AS transaction_type, " + 
            "stock.description AS stock, transactions.quantity, " +
            "transactions.date " +
        "FROM transactions " +
        "LEFT JOIN users ON transactions.user_id = users.id " +
        "LEFT JOIN transaction_types ON transactions.transaction_type_id = transaction_types.id " +
        "LEFT JOIN stock ON transactions.stock_id = stock.id"
    )
    
    return JsonResponse(_get_table_response(query=query), safe=False)


def getForm(request, form):
    """Thisfunction will return all the data needed to load a form.

    Args:
        form (str): Name of the form to load.
    """
    response = response_obj()
    
    if form == 'issue':
        query_users = "SELECT id, username FROM users WHERE active = 1"
        query_stock = "SELECT id, description FROM stock"
        query_transaction_types = "SELECT id, description FROM transaction_types"
        
        with connection.cursor() as cursor:
            cursor.execute(query_users)
            users = _get_table_data(cursor)
            
            cursor.execute(query_stock)
            stock = _get_table_data(cursor)
            
            cursor.execute(query_transaction_types)
            transaction_types = _get_table_data(cursor)
            
        response['success'] = True
        response['message'] = "Successfully retrieved form data."
        response['data'] = {
            'users': users,
            'stock': stock,
            'transaction_types': transaction_types
        }
        
        return JsonResponse(response, safe=False)
        
    else:
        response['success'] = False
        response['message'] = f"Unknown form, {form}"
        
        return JsonResponse(response, safe=False)
    

def getTable(request, table_name, start, quantity):
    response = _get_table_response(table_name=table_name, start=start, quantity=quantity)
    return JsonResponse(response, safe=False)