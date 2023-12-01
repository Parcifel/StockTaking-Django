from django.shortcuts import render, redirect
from django.db import connection

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

# Create your views here.
def login(request):
    request.session.flush()
    
    if request.method == 'POST':
        # Unknown request
        if 'username' not in request.POST or 'password' not in request.POST:
            print(request.POST)
            return render(request, 'login/login.html', {'message': 'Unknown POST request sent to server. Please try again.'})
        
        data = {
            "username": request.POST['username'],
            "password": request.POST['password'],
        }
        
        if data['username'] == "":
            return render(request, 'login/login.html', {'message': 'Please enter a username.'})
        elif data['password'] == "":
            return render(request, 'login/login.html', {'message': 'Please enter a password.'})
        
        with connection.cursor() as cursor:
            query = """
                SELECT password FROM users WHERE username = %s
            """
            cursor.execute(query, [data['username']])
            
            response = dictfetchall(cursor)
            
            if len(response) == 0:
                return render(request, 'login/login.html', {'message': 'Username or password is incorrect.'})
            
            if response[0]['password'] != data['password']:
                return render(request, 'login/login.html', {'message': 'Username or password is incorrect.'})
            
            request.session['username'] = data['username']
            request.session['password'] = data['password']
            request.session['logged_in'] = True
            
            return redirect('home')
            
        
    return render(request, 'login/login.html', {'message': ''})


def logout(request):
    return redirect('login')
    
    return render(request, 'login/logout.html')