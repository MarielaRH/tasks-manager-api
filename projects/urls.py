from django.urls import path
from projects.views import *

urlpatterns = [
    path('', projects, name="projects"),
    path('<int:project_id>', manage_projects, name="manage_projects"),
    path('<int:project_id>/participants', participants_by_projects, name="participants_by_projects"),
    path('<int:project_id>/users/<int:user_id>', manage_users_project, name="manage_users_project")
]