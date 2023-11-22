from django.shortcuts import render, redirect
from django.db import connection

temp_users = [
    {
        "username": "admin",
        "password": "admin",
    },
    {
        "username": "user",
        "password": "user",
    },
    {
        "username": "test",
        "password": "test",
    },
]

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

# Create your views here.
def login(request):
    if request.method == 'POST':
        # Unknown request
        if 'username' not in request.POST or 'password' not in request.POST:
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
            
            return redirect('home')
            
        
    return render(request, 'login/login.html', {'message': ''})


def logout(request):
    return render(request, 'login/logout.html')