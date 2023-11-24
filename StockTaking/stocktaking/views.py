from django.shortcuts import render, redirect
from django.db import connection

import math

# Create your views here.
def home(request):
    return render(request, 'stocktaking/dash.html', {})

def issue(request):
    transactions_per_page = 10
    
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM transactions")
        
        pages = math.ceil(cursor.rowcount / transactions_per_page)
            
    return render(request, 'stocktaking/issue.html', {'pages': pages, 'transactions_per_page': transactions_per_page})

def log(request):
    return render(request, 'stocktaking/log.html', {})

def admin(request):
    return render(request, 'stocktaking/admin.html', {})

def logout(request):
    return redirect('/logout')