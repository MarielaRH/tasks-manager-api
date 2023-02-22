from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status
from projects.models import Project
from users.models import User
from users.serializers import *
from .serializers import *


@api_view(['GET','POST'])
@permission_classes([permissions.IsAuthenticated])
def projects(request):
    paginator = PageNumberPagination()
    response = None
    if request.method == 'GET':
        projects = Project.objects.all()
        page = paginator.paginate_queryset(projects, request)
        projects_serialized = ProjectsSerializer(page, many=True)
        response = {
            "status_code": status.HTTP_200_OK,
            "message":"OK",
            "data": projects_serialized.data
        }
        return paginator.get_paginated_response(response)
    elif request.method == 'POST':
        project = ProjectsSerializer(data=request.data)
        if project.is_valid():
            project = Project.objects.create(
                name = request.data['name'],
                admin_user_id = request.data['admin_user'],
                description = request.data['description'],
            )
            created_project = Project.objects.get(id=project.id)
            projects_serialized = ProjectsSerializer(created_project)
            response = {
                "status_code": status.HTTP_201_CREATED,
                "message":"OK",
                "data": projects_serialized.data
            }
        else:
            response = {
                "status_code": status.HTTP_400_BAD_REQUEST,
                "message":"Bad request",
                "error": project.errors
            }
        return Response(response)


@api_view(['GET','PUT', 'DELETE'])
@permission_classes([permissions.IsAuthenticated])
def manage_projects(request, project_id):
    response = None

    try:
        project = Project.objects.get(id=project_id)
    except:
        return Response({
            "status_code": status.HTTP_404_NOT_FOUND,
            "message": "Not found",
            "error": "project you’re trying to access doesn’t exist",
        })

    if request.method == 'GET':
        project_serialized = ProjectsSerializer(project)
        response = {
            "status_code": status.HTTP_200_OK,
            "message":"OK",
            "data": project_serialized.data
        }
    elif request.method == 'PUT':
        project_serialized = ProjectsSerializer(data=request.data)
        if project_serialized.is_valid():
            project.name = request.data['name']
            project.admin_user_id = request.data['admin_user']
            project.description = request.data['description']
            project.save()

            project_serialized = ProjectsSerializer(project)
            response = {
                "status_code": status.HTTP_200_OK,
                "message":"OK",
                "data": project_serialized.data
            }
        else:
            response = {
                "status_code": status.HTTP_400_BAD_REQUEST,
                "message":"Bad request",
                "error": project.errors
            }
    elif request.method == 'DELETE':
        response = {
            "status_code": status.HTTP_200_OK,
            "message": "OK",
            "data": "project {} has been successfully removed".format(project.name)
        }
        project.participants.clear()
        project.delete()

    return Response(response)


@api_view(['POST','DELETE'])
@permission_classes([permissions.IsAuthenticated])
def manage_users_project(request, project_id, user_id):
    response = None
    project = None
    user = None

    try:
        project = Project.objects.get(id=project_id)
        user = User.objects.get(id=user_id)
    except:
        response = {
            "status_code": status.HTTP_404_NOT_FOUND,
            "message":"Not found",
            "error": ""
        }
        if not project:
            response["error"]="project you’re trying to access doesn’t exist"
            return Response(response)
        elif not user:
            response["error"]="user you’re trying to access doesn’t exist"
            return Response(response)

    if request.method == 'POST':

        if  project.participants.contains(user):
            response ={
                "status_code": status.HTTP_409_CONFLICT,
                "message": "Conflict",
                "error":"this user has already been added to this project",
            }
        else:
            project.participants.add(user)

            response = {
                "status_code": status.HTTP_200_OK,
                "message": "OK",
                "data": "user has been successfully added into {}".format(project.name)
            }
    elif request.method == 'DELETE':
        if  project.participants.contains(user):
            project.participants.remove(user)

            response = {
                "status_code": status.HTTP_200_OK,
                "message": "OK",
                "data": "user has been successfully removed from {}".format(project.name)
            }
        else:
            response = {
                "status_code": status.HTTP_404_NOT_FOUND,
                "message": "Not found",
                "data": "user you’re trying to access doesn’t exist in {}".format(project.name)
            }


    return Response(response)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def participants_by_projects(request, project_id):
    paginator = PageNumberPagination()
    response = None
    page = None

    try:
        project = Project.objects.get(id=project_id)
    except:
        return Response({
            "status_code": status.HTTP_404_NOT_FOUND,
            "message": "Not found",
            "error": "project you’re trying to access doesn’t exist",
        })

    if request.method == 'GET':
        project_participants = project.participants.all()
        page = paginator.paginate_queryset(project_participants, request)
        project_participants_serialized = GetUserSerializer(page, many=True)
        response = {
            "status_code": status.HTTP_200_OK,
            "message":"OK",
            "data": project_participants_serialized.data
        }

    return paginator.get_paginated_response(response)