from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db import connection
import datetime

# Create your views here.

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]
    
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
    with connection.cursor() as cursor:
        """Tables -> Columns
        Users -> id, username, password, active
        Transaction_Types -> id, description
        Transactions -> id, user_id, transaction_type_id, stock_id, quatity, date
        Stock -> id, description, quantity
        """
        if query is None and table_name is None:
            return JsonResponse({}, safe=False)
        elif query is None:
            if table_name == 'users':
                query = """
                    SELECT users.id, username, password, active
                    FROM users
                """
                headers = ['id', 'username', 'password', 'active']
            elif table_name == 'transaction_types':
                query = """
                    SELECT transaction_types.id, description
                    FROM transaction_types
                """
                headers = ['id', 'description']
            elif table_name == 'transactions':
                query = """
                    SELECT transactions.id, users.username AS user, transaction_types.description, stock.description, transactions.quantity, date
                    FROM transactions
                    LEFT JOIN users ON transactions.user_id = users.id
                    LEFT JOIN transaction_types ON transactions.transaction_type_id = transaction_types.id
                    LEFT JOIN stock ON transactions.stock_id = stock.id
                """
                headers = ['id', 'user', 'transaction_type', 'stock', 'quantity', 'date']
            elif table_name == 'stock':
                query = """
                    SELECT stock.id, description, quantity
                    FROM stock
                """
                headers = ['id', 'description', 'quantity']
            else:
                return JsonResponse({}, safe=False)
            cursor.execute(query)
        
        else:
            query = query
            cursor.execute(query)
            headers = _get_table_headers(cursor)
            
        data = _get_table_data(cursor)
        
        if len(data) == 0:
            return JsonResponse({
                'headers': headers
            }, safe=False)
        
        if start is not None:
            if start < 0:
                start = 0
            if start >= len(data):
                return JsonResponse({}, safe=False)
            if quantity is None:
                data = data[start:]
            else:
                if quantity < 0:
                    quantity = 0
                data = data[start:start+quantity]
        
        types = _get_table_types(headers, data[0])
        
    print(f"Headers: \n {headers}")
    print(f"Data: \n {data}")
    print(f"Types: \n {types}")
        
    return JsonResponse({
        'headers': headers,
        'data': data,
        'types': types
    }, safe=False)

def get_table(request, table):
    return _get_table_response(table_name=table)
    
def get_table_element(request, table, start):
    return _get_table_response(table_name=table, start=start)
    
def get_table_elements(request, table, start, quantity):
    print(_get_table_response(table_name='transactions'))
    
    return _get_table_response(table_name=table, start=start, quantity=quantity)


def update_table_element(request, table, id, column, data_type, new_value):
    
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
            print("Error: type not recognized.")
            return JsonResponse({}, safe=False)
    except:
        print("Error: could not convert new_value to type.")
        return JsonResponse({}, safe=False)
    
    try:
        query = f"UPDATE {table} SET {column} = %s WHERE id = %s"
        with connection.cursor() as cursor:
            cursor.execute(query, [new_value, id])
            
        if type(new_value) == datetime.datetime:
            new_value = new_value.strftime('%Y-%m-%d %H:%M:%S')
        elif type(new_value) == bool:
            new_value = 1 if new_value else 0
        else:
            new_value = str(new_value)
            
        return JsonResponse({
            'new_value': new_value    
        }, safe=False)
    except Exception as e:
        print("Error: Could not update table element.")
        print(e)
        return JsonResponse({}, safe=False)
    