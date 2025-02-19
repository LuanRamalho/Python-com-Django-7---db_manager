from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('create_database/', views.create_database, name='create_database'),
    path('delete_database/<int:db_id>/', views.delete_database, name='delete_database'),
    path('update_database/<int:db_id>/', views.delete_database, name='update_database'),
]
