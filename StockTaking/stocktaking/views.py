from django.shortcuts import render, redirect
from django.db import connection

import math

def auth_required(func):
    def wrapper(request, *args, **kwargs):
        if 'logged_in' not in request.session or request.session['logged_in'] == False:
            return redirect('login')
        
        return func(request, *args, **kwargs)
    
    return wrapper

# Create your views here.
@auth_required
def home(request):
    return render(request, 'stocktaking/dash.html', {})

@auth_required
def issue(request):
    transactions_per_page = 10
    
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM transactions")
        
        pages = math.ceil(cursor.rowcount / transactions_per_page)
            
    return render(request, 'stocktaking/issue.html', {'pages': pages, 'transactions_per_page': transactions_per_page})

@auth_required
def log(request):
    return render(request, 'stocktaking/log.html', {})

@auth_required
def admin(request):
    return render(request, 'stocktaking/admin.html', {})

@auth_required
def logout(request):
    return redirect('/logout')