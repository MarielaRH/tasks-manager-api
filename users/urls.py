from django.urls import path
from .views import *

urlpatterns = [
    path('signup', user_signup , name='signup'),
    path('login', user_login, name='signup'),
    path('users', users, name="users"),
    path('users/<int:user_id>', manage_users, name="manage_users"),
    path('users/<int:user_id>/projects', user_projects, name="user_projects"),
]