from django.urls import path
from .views import *

urlpatterns = [
    path('projects/<int:project_id>/tasks', tasks, name='tasks'),
    path('projects/<int:project_id>/tasks/<int:task_id>', manage_tasks, name='managa_tasks')
]