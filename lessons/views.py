from datetime import datetime

from django.db.models import Count
from drf_yasg import openapi
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.models import User
# Create your views here.
from .models import Lesson
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

    lesson = Lesson.objects.create(title=title, description=description, category=category, created_by=request.user,
                                   is_public=is_public)
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


@swagger_auto_schema(
    method='get',
    responses={
        200: 'List of public lessons created by a specified user',
        401: 'Invalid credentials'
    }
)
@api_view(['GET'])
def list_lessons_by_user(request, user_id):
    """
    List all public lessons created by a specified user
    """
    if not User.objects.filter(id=user_id).exists():
        return Response({'error': 'User not found'}, status=401)

    if request.user.is_staff or request.user.id == user_id:
        lessons = Lesson.objects.filter(created_by=user_id)
    else:
        lessons = Lesson.objects.filter(created_by=user_id, is_public=True)
    serializer = LessonSerializer(lessons, many=True)
    return Response(serializer.data)


@swagger_auto_schema(
    method='get',
    responses={
        200: 'List of lessons created by category',
        401: 'Unauthorized'
    }
)
@api_view(['GET'])
def list_lessons_by_category(request, category):
    """
    List all lessons created by category
    """
    category = category.title()

    if request.user.is_staff:
        lessons = Lesson.objects.filter(category=category)
    else:
        lessons = Lesson.objects.filter(category=category, is_public=True)
    serializer = LessonSerializer(lessons, many=True)
    return Response(serializer.data)


@swagger_auto_schema(
    method='get',
    responses={
        200: 'List of lessons created containing keywords',
        401: 'Unauthorized'
    }
)
@api_view(['GET'])
def list_lessons_by_keywords(request, keywords):
    """
    List all lessons created containing keywords
    """
    keywords = keywords.split()
    lessons = Lesson.objects.filter(title__icontains=keywords[0])
    for keyword in keywords[1:]:
        lessons = lessons | Lesson.objects.filter(title__icontains=keyword)
    serializer = LessonSerializer(lessons, many=True)
    return Response(serializer.data)


@swagger_auto_schema(
    method='patch',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'lesson_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Lesson ID'),
            'title': openapi.Schema(type=openapi.TYPE_STRING, description='Title'),
            'description': openapi.Schema(type=openapi.TYPE_STRING, description='Description'),
            'category': openapi.Schema(type=openapi.TYPE_STRING, description='Category'),
            'is_public': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Is the lesson publically available?'),
        }
    ),
    responses={
        200: 'Lesson updated',
        401: 'Unauthorized'
    }
)
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_lesson(request):
    """
    Update a lesson
    """
    lesson_id = request.data.get('lesson_id')
    title = request.data.get('title')
    description = request.data.get('description')
    category = request.data.get('category')
    is_public = request.data.get('is_public', False)

    if lesson_id is None:
        return Response({'error': 'Please provide lesson_id'}, status=401)

    lesson = Lesson.objects.get(id=lesson_id)
    if lesson.created_by != request.user and not request.user.is_staff:
        return Response({'error': 'Unauthorized'}, status=401)

    if title is not None:
        lesson.title = title
    if description is not None:
        lesson.description = description
    if category is not None:
        lesson.category = category

    lesson.is_public = is_public
    lesson.updated_at = datetime.now()
    lesson.save()

    serializer = LessonSerializer(lesson)
    return Response(serializer.data)


@swagger_auto_schema(
    method='delete',
    responses={
        200: 'Lesson deleted',
        401: 'Unauthorized'
    },
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'lesson_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Lesson ID'),
        }
    )
)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_lesson(request):
    """
    Delete a lesson
    """
    lesson_id = request.data.get('lesson_id')
    if lesson_id is None:
        return Response({'error': 'Please provide lesson_id'}, status=401)

    lesson = Lesson.objects.get(id=lesson_id)
    if lesson.created_by != request.user and not request.user.is_staff:
        return Response({'error': 'Unauthorized'}, status=401)

    lesson.delete()
    return Response({'message': 'Lesson deleted successfully'})

@api_view(['GET'])
def get_top_categories(request):
    """
    Get the top 5 categories by number of lessons
    """
    categories = Lesson.objects.values('category').annotate(count=Count('category')).order_by('-count')[:4]
    return Response(categories)

@api_view(['GET'])
def get_lesson_by_id(request, id):
    """
    Get a lesson by ID
    """
    lesson = Lesson.objects.get(id=id)
    serializer = LessonSerializer(lesson)
    return Response(serializer.data)