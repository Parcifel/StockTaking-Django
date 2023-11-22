from django.shortcuts import render, redirect

# Create your views here.
def home(request):
    return render(request, 'stocktaking/dash.html', {})


def admin(request):
    return render(request, 'stocktaking/admin.html', {})