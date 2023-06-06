from django.urls import path
  
# importing views from views..py
from . import views

urlpatterns = [
    
    
    path('create_department/', views.create_department, name="create_department"),
    path('create_employee/', views.create_employee, name="create_employee"),
    path('create_leave/', views.create_leave, name="create_leave"),
    path('accept_leave/<int:pk>/', views.accept_leave, name='accept_leave'),
    path('pending_leave/', views.pending_leave, name='pending_leave'),
 
   
]