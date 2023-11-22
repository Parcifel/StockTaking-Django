from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db import connection

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

def _get_table_response(table_name, start=None, quantity=None):
    with connection.cursor() as cursor:
        query = f"SELECT * FROM {table_name}"
        cursor.execute(query)
        
        headers = _get_table_headers(cursor)
        data = _get_table_data(cursor)
        
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
        
    return JsonResponse({
        'headers': headers,
        'data': data
    }, safe=False)

def get_table(request, table):
    return _get_table_response(table)
    
def get_table_element(request, table, start):
    return _get_table_response(table, start)
    
def get_table_elements(request, table, start, quantity):
    return _get_table_response(table, start, quantity)