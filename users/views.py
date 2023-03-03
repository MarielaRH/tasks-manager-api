
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import permissions
from rest_framework import status
from .models import User
from projects.serializers import *
from .serializers import *

# Create your views here.

@api_view(['GET','POST'])
@permission_classes([permissions.AllowAny])
def user_signup(request):

    response = None

    if request.method == 'POST':
        data = UserSerializer(data=request.data)
        if data.is_valid():
            user = User.objects.create_user(
                email=request.data['email'],
                password=request.data['password'],
                first_name=request.data['first_name'],
                last_name=request.data['last_name']
            )
            created_user = GetUserSerializer(user)

            response = {
                "status_code": status.HTTP_201_CREATED,
                "message": "User has been successfully created",
                "data": created_user.data
            }
        else:
            response = {
                "status_code": status.HTTP_400_BAD_REQUEST,
                "message": 'Bad request',
                "error":  data.errors
            }

        return Response(response, status=response['status_code'])


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def user_login(request):
 if request.method == 'POST':
    serializer = LoginUserSerializer(data=request.data)
    if serializer.is_valid():
        user = authenticate(
            username=request.data['email'],
            password=request.data['password']
        )
        if not user:
            user_exist = User.objects.filter(email=request.data['email'])
            error_message = None
            if len(user_exist) == 0:
                error_message = {
                    "status_code": status.HTTP_404_NOT_FOUND,
                    "message": 'Not found',
                    "error": '{} is not register'.format(request.data['email'])
                }
            else:
                error_message = {
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "message": 'Bad request',
                    "error": 'password is wrong'
                }
            return Response(error_message, status=error_message.status_code)
        else:
            user_serialized = GetUserSerializer(user)
            token = Token.objects.get(user=user)
            return Response({
                'token': token.key,
                'user': user_serialized.data
            }, status=status.HTTP_200_OK)
    else:
        return Response({
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": 'Bad request',
            "error": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def users(request):
    paginator = PageNumberPagination()
    if request.method == 'GET':
        users = User.objects.all()
        page = paginator.paginate_queryset(users, request)
        users_serialized = GetUserSerializer(page, many=True)
        return paginator.get_paginated_response({
                "status_code": status.HTTP_200_OK,
                "message": 'OK',
                "data": users_serialized.data
            }, status=status.HTTP_200_OK)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([permissions.IsAuthenticated])
def manage_users(request, user_id):

    response = None

    try:
        user = User.objects.get(id=user_id)
    except:
        return Response({
            "status_code": status.HTTP_404_NOT_FOUND,
            "message": "Not found",
            "error": "task you’re trying to access doesn’t exist",
        }, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        user_serialized = GetUserSerializer(user)
        response = {
            "status_code": status.HTTP_200_OK,
            "message": 'OK',
            "data": user_serialized.data
        }
    elif request.method == 'PUT':
        user_serialized = UpdateUserSerializer(data=request.data)
        if user_serialized.is_valid():
            user.first_name = request.data['first_name']
            user.last_name = request.data['last_name']
            user.save()

            user_serialized = GetUserSerializer(user)

            response = {
                "status_code": status.HTTP_200_OK,
                "message": 'user has been successfully updated',
                "data": user_serialized.data
            }
        else:
            response = {
                "status_code": status.HTTP_404_NOT_FOUND,
                "message": "Not found",
                "error": user_serialized.errors
            }
    elif request.method == 'DELETE':
        response = {
            "status_code": status.HTTP_200_OK,
            "message": "OK",
            "data": "User '{} {}' has been successfully removed".format(user.first_name, user.last_name)
        }
        user.delete()

    return Response(response, status=response.status_code)



@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_projects(request, user_id):
    paginator = PageNumberPagination()
    try:
        user = User.objects.get(id=user_id)
    except:
        return Response({
            "status_code": status.HTTP_404_NOT_FOUND,
            "message": "Not found",
            "error": "user you’re trying to access doesn’t exist",
        }, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        user_projects = user.projects.all()
        page = paginator.paginate_queryset(user_projects, request)
        user_projects_serialized = ProjectsSerializer(page, many=True)
        return paginator.get_paginated_response({
            "status_code": status.HTTP_200_OK,
            "message": "OK",
            "projects": user_projects_serialized.data,
        }, status=status.HTTP_200_OK)

