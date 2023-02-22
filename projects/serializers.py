from rest_framework import serializers
from .models import Project
from tasks.serializers import TasksSerializer



class ProjectsSerializer(serializers.ModelSerializer):
    # tasks = TasksSerializer(many=True,read_only=True)
    class Meta:
        model = Project
        # fields = ['id', 'name', 'description', 'created_at', 'admin_user', 'participants', 'tasks']
        fields = ['id', 'name', 'description', 'created_at', 'admin_user']