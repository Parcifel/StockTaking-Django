from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('issue/', views.issue, name='issue'),
    path('log/', views.log, name='log'),
    path('admin/', views.admin, name='admin'),
    path('logout/', views.logout, name='logout'),
]