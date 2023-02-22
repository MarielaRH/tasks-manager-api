from rest_framework import serializers
from .models import Task

class TasksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

class CreateTasksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['name','description','category','project','user']

class UpdateTasksSerializer(serializers.Serializer):
    name = serializers.CharField()
    description = serializers.CharField()
    status = serializers.CharField()
    category = serializers.IntegerField()
    project = serializers.IntegerField()
    user = serializers.IntegerField()
