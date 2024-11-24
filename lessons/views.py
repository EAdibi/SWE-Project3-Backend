from django.shortcuts import render
from django.contrib.auth import authenticate
from django.core.validators import validate_email
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.
from .models import Lesson
from users.models import User
from .serializers import LessonSerializer



@swagger_auto_schema(
    method='get',
    responses={
        200: 'List of lessons',
        401: 'Invalid credentials'
    }
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_lessons(request):
    """
    List all lessons
    """
    if not request.user.is_staff:
        return Response({'error': 'Unauthorized'}, status=401)
    lessons = Lesson.objects.all()
    serializer = LessonSerializer(lessons, many=True)
    return Response(serializer.data)

@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'title': openapi.Schema(type=openapi.TYPE_STRING, description='Title'),
            'description': openapi.Schema(type=openapi.TYPE_STRING, description='Description'),
            'category': openapi.Schema(type=openapi.TYPE_STRING, description='Category'),
            'is_public': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Is the lesson publically available?'),
        },
        required=['title', 'description', 'category']
    ),
    responses={
        200: 'Lesson created',
        401: 'Unauthorized'
    }
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_lesson(request):
    """
    Create a lesson
    """
    title = request.data.get('title')
    description = request.data.get('description')
    category = request.data.get('category')
    is_public = request.data.get('is_public', False)

    if title is None or description is None or category is None:
        return Response({'error': 'Please provide title, description and category'}, status=401)

    lesson = Lesson.objects.create(title=title, description=description, category=category, created_by=request.user, is_public=is_public)
    serializer = LessonSerializer(lesson)
    return Response(serializer.data)

@swagger_auto_schema(
    method='get',
    responses={
        200: 'List of public lessons',
        401: 'Invalid credentials'
    }
)
@api_view(['GET'])
def list_public_lessons(request):
    """
    List all public lessons
    """
    lessons = Lesson.objects.filter(is_public=True)
    serializer = LessonSerializer(lessons, many=True)
    return Response(serializer.data)