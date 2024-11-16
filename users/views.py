from django.shortcuts import render
# import check_password
from django.contrib.auth import authenticate
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import UserSerializer
# Create your views here.
@api_view(['GET'])
# This should be changed to IsAdminUser later, when using a cloud db
@permission_classes([IsAuthenticated])
def list_users(request):
    """
    List all users (Admin only)
    """
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password'),
        },
        required=['username', 'password']
    ),
    responses={
        200: 'Login successful',
        401: 'Invalid credentials'
    }
)
@api_view(['POST'])
def login(request):
    """
    Login a user using username and password

    """
    username = request.data.get('username')
    password = request.data.get('password')

    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'}, status=401)

    user = authenticate(username=username, password=password)
    if user is None:
        return Response({'error': 'Invalid credentials'}, status=401)

    refresh = RefreshToken.for_user(user)

    return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'user': UserSerializer(user).data
    })

@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'refresh': openapi.Schema(type=openapi.TYPE_STRING, description='Refresh token')
        },
        required=['refresh']
    ),
    responses={
        200: 'Logout successful',
        401: 'Invalid credentials'
    },
    security=[{'Bearer': []}],
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    """
    Logout a user by blacklisting their refresh token
    """
    try:
        refresh_token = request.data["refresh"]
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({"detail": "Logout successful"}, status=200)
    except Exception as e:
        return Response({"error": str(e)}, status=400)


@swagger_auto_schema(
    method='get',
    responses={
        200: 'User details'
    },
    security=[{'Bearer': []}],
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user(request):
    """
    Get details for the current user
    """
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data)

@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password'),
            'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email'),
            'google_id': openapi.Schema(type=openapi.TYPE_STRING, description='Google ID'),
        }, required=['username', 'password', 'email']
    ),
    responses={
        201: 'User created successfully',
        400: 'Invalid user details'
    }
)
@api_view(['POST'])
def signup(request):
    """
    Register a new user
    """
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')
    google_id = request.data.get('google_id') if 'google_id' in request.data else None
    bio = request.data.get('bio') if 'bio' in request.data else None

    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'}, status=400)

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists'}, status=400)

    User.objects.create_user(username=username, password=password, email=email, google_id=google_id, bio=bio)

    return Response({'message': 'User created successfully'}, status=201)