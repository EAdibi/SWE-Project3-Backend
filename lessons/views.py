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