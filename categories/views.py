from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status
from categories.models import Category
from .serializers import *
from tasks.serializers import *
# Create your views here.


@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticated])
def categories(request):
    paginator = PageNumberPagination()
    page = None
    response = None
    if request.method == 'GET':
        categories = Category.objects.all()
        page = paginator.paginate_queryset(categories, request)
        categories_serialized = CategoriesSerializers(page, many=True)
        response = {
            "status_code": status.HTTP_200_OK,
            "message":"OK",
            "data": categories_serialized.data
        }
        return paginator.get_paginated_response(response)
    elif request.method == 'POST':
        try:
            Category.objects.get(name=request.data['name'])
            response = {
                "status_code": status.HTTP_409_CONFLICT,
                "message": "Conflict",
                "error":"category with this name already exists",
            }
        except:
            category_serialized =  CategoriesSerializers(data=request.data)
            if category_serialized.is_valid():
                category = Category.objects.create(
                    name=request.data['name']
                )

                created_category = Category.objects.get(id=category.id)
                category_serialized = CategoriesSerializers(created_category)
                response ={
                    "status_code": status.HTTP_201_CREATED,
                    "message": "category has been successfully created",
                    "error": category_serialized.data
                }
            else:
                response = {
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "message": "Bad request",
                    "error": category_serialized.errors
                }
        return Response(response)



@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([permissions.IsAuthenticated])
def manage_category(request, category_id):
    response = None

    try:
        category = Category.objects.get(id=category_id)
    except:
        return Response({
            "status_code": status.HTTP_404_NOT_FOUND,
            "message": "Not found",
            "error": "category you’re trying to access doesn’t exist",
        })

    if request.method == 'GET':
        category_serialized = CategoriesSerializers(category)
        response = {
            "status_code": status.HTTP_200_OK,
            "message":"OK",
            "data": category_serialized.data
        }

    elif request.method == 'PUT':
        try:
            category = Category.objects.get(name=request.data['name'])
            response = {
                "status_code": status.HTTP_409_CONFLICT,
                "message": "Conflict",
                "error":"category with this name already exists",
            }
        except:
            category_serialized = CategoriesSerializers(data=request.data)
            if category_serialized.is_valid():
                category.name = request.data['name']
                category.save()

                category_serialized = CategoriesSerializers(category)

                response = {
                    "status_code": status.HTTP_200_OK,
                    "message":"OK",
                    "data": category_serialized.data
                }
            else:
                response = {
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "message": "Bad request",
                    "error": category_serialized.errors
                }
    elif request.method == 'DELETE':
        response = {
            "status_code": status.HTTP_200_OK,
            "message": "OK",
            "data": "category '{}' has been successfully removed".format(category)
        }
        category.delete()

    return Response(response)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def category_tasks(request, category_id):
    paginator = PageNumberPagination()
    response = None

    try:
        category = Category.objects.get(id=category_id)
    except:
        return Response({
            "status_code": status.HTTP_404_NOT_FOUND,
            "message": "Not found",
            "error": "category you’re trying to access doesn’t exist",
        })

    if request.method == 'GET':
        tasks_category = category.tasks.all()
        page = paginator.paginate_queryset(tasks_category, request)
        tasks_category_serialized = TasksSerializer(page, many=True)
        response = {
            "status_code": status.HTTP_200_OK,
            "message":"OK",
            "data": tasks_category_serialized.data
        }
    return paginator.get_paginated_response(response)