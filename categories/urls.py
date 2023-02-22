from django.urls import path
from .views import *

urlpatterns=[
    path('', categories, name='categories'),
    path('<int:category_id>', manage_category, name='manage_category'),
    path('<int:category_id>/tasks', category_tasks, name='category_tasks')
]