
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status
from .serializers import *
from projects.serializers import *
from .models import User

# Create your views here.
# CUD

@api_view(['GET','POST'])
@permission_classes([permissions.AllowAny])
def user_signup(request):

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
            return Response({
                "statusCode": status.HTTP_201_CREATED,
                "message": 'User has been successfully created',
                "data": created_user.data
            })
        else:
             return Response({
                "statusCode": status.HTTP_400_BAD_REQUEST,
                "message": 'Bad Request',
                "error": data.errors,
            })


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def user_login(request):
 if request.method == 'POST':
    serializer = LoginUserSerializer(data=request.data)
    print(serializer.is_valid())
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
                    "statusCode": status.HTTP_404_NOT_FOUND,
                    "message": 'Not found',
                    "error": '{} is not register'.format(request.data['email'])
                }
            else:
                error_message = {
                    "statusCode": status.HTTP_400_BAD_REQUEST,
                    "message": 'Bad request',
                    "error": 'password is wrong'
                }
            return Response(error_message)
        else:
            user_serialized = GetUserSerializer(user)
            token = Token.objects.get(user=user)
            return Response({
                'token': token.key,
                'user': user_serialized.data
            })
    else:
        return Response({
            "statusCode": status.HTTP_400_BAD_REQUEST,
            "message": 'Bad request',
            "error": serializer.errors
        })


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def users(request):
    if request.method == 'GET':
        users = User.objects.all()
        users_serialized = GetUserSerializer(users, many=True)
        return Response({
                "statusCode": status.HTTP_200_OK,
                "message": 'OK',
                "data": users_serialized.data
            })

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
        })

    if request.method == 'GET':
        user_serialized = GetUserSerializer(user)
        response = {
            "statusCode": status.HTTP_200_OK,
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
                "statusCode": status.HTTP_200_OK,
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

    return Response(response)



@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_projects(request, user_id):
    response = None
    try:
        user = User.objects.get(id=user_id)
    except:
        return Response({
            "status_code": status.HTTP_404_NOT_FOUND,
            "message": "Not found",
            "error": "user you’re trying to access doesn’t exist",
        })

    if request.method == 'GET':
        user_projects = user.projects.all()
        user_projects_serialized = ProjectsSerializer(user_projects, many=True)
        return Response({
            "status_code": status.HTTP_200_OK,
            "message": "OK",
            "projects": user_projects_serialized.data,
        })
