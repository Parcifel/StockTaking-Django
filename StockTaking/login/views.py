from django.shortcuts import render, redirect

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
        
        if data in temp_users:
            return redirect('home')
        
    return render(request, 'login/login.html', {'message': ''})


def logout(request):
    return render(request, 'login/logout.html')