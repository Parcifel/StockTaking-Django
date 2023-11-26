from django.urls import path, include
from . import views

urlpatterns = [
    path('get-table/<str:table>/', views.get_table, name='get-table'),
    path('get-table/<str:table>/<int:start>/', views.get_table_element, name='get-table-element'),
    path('get-table/<str:table>/<int:start>/<int:quantity>/', views.get_table_elements, name='get-table-elements'),

    path('update/<str:table>/<int:id>/<str:column>/<str:data_type>/<str:new_value>/', views.update_table_element, name='update-table-element'),

    path('getDashboard/', views.get_dash_info, name='get-dashboard'),
    path('getIssue/<int:start>/<int:quantity>/', views.get_issue, name='get-issue'),
    path('getLog/', views.get_log, name='get-log'),

    path('get-form-data/<str:form>/', views.get_form_data, name='get-form-data'),
    
    path('add-transaction/<int:user_id>/<int:transaction_type>/<int:stock_id>/<str:quantity>/', views.add_transaction, name='add-transaction'),
]
