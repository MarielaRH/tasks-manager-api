from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status
from projects.models import Project
from .models import Task
from .serializers import *
# Create your views here.

@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticated])
def tasks(request,project_id):
    paginator = PageNumberPagination()
    response = None
    try:
        Project.objects.get(id=project_id)
    except:
        return Response({
            "status_code": status.HTTP_404_NOT_FOUND,
            "message":"Not found",
            "error": "project you’re trying to access doesn’t exist"
        }, status=status.HTTP_404_NOT_FOUND)


    if request.method == 'GET':
        tasks = Task.objects.filter(project_id=project_id)
        page = paginator.paginate_queryset(tasks, request)
        tasks_serialized = TasksSerializer(page, many=True)
        response = {
            "status_code": status.HTTP_200_OK,
            "message":"OK",
            "data": tasks_serialized.data
        }
        return paginator.get_paginated_response(response)
    elif request.method == 'POST':
        task_serialized = CreateTasksSerializer(data=request.data)
        if task_serialized.is_valid():
            task = Task.objects.create(
                name = request.data['name'],
                description = request.data['description'],
                project_id = request.data['project'],
                category_id = request.data['category'],
                user_id = request.data['user'],
            )

            created_task = Task.objects.get(id=task.id)
            task_serialized = TasksSerializer(created_task)
            response = {
                "status_code": status.HTTP_201_CREATED,
                "message":"OK",
                "data": task_serialized.data
            }
        else:
            response = {
                "status_code": status.HTTP_400_BAD_REQUEST,
                "message":"Bad request",
                "error": task_serialized.errors
            }

        return Response(response, status=response.status_code)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([permissions.IsAuthenticated])
def manage_tasks(request, project_id, task_id):

    response = None
    project = None
    task = None
    try:
        project = Project.objects.get(id=project_id)
        task = Task.objects.get(id=task_id,project=project_id)
    except:
        response = {
            "status_code": status.HTTP_404_NOT_FOUND,
            "message":"Not found",
            "error": ""
        }
        if not project:
            response["error"]="project you’re trying to access doesn’t exist"
            return Response(response, status=response.status_code)
        elif not task:
            response["error"]="task you’re trying to access doesn’t exist"
            return Response(response, status=response.status_code)


    if request.method == 'GET':

        task_serialized = TasksSerializer(task)
        response = {
            "status_code": status.HTTP_200_OK,
            "message":"OK",
            "data": task_serialized.data
        }
    elif request.method == 'PUT':
        task_serialized = UpdateTasksSerializer(data=request.data)
        if task_serialized.is_valid():
            task.name = request.data['name']
            task.description = request.data['description']
            task.category_id = request.data['category']
            task.project_id = request.data['project']
            task.user_id = request.data['user']

            if 'status' in request.data:
                task.status = request.data['status']

            task.save()
            task_serialized = TasksSerializer(task)
            response = {
                "status_code": status.HTTP_200_OK,
                "message":"OK",
                "error": task_serialized.data
            }
        else:
            response = {
                "status_code": status.HTTP_400_BAD_REQUEST,
                "message":"Bad request",
                "error": task_serialized.errors
            }
    elif request.method == 'DELETE':
        response = {
            "status_code": status.HTTP_200_OK,
            "message":"OK",
            "data": "Tasks {} has been successfully removed from project {}".format(task.name, project.name)
        }
        task.delete()

    return Response(response, status=status.response.status_code)
