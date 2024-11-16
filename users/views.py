from django.shortcuts import render
# import check_password
from django.contrib.auth import authenticate
from django.core.validators import validate_email
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
            'bio': openapi.Schema(type=openapi.TYPE_STRING, description='Bio'),
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

    try:
        validate_email(email)
    except Exception as e:
        return Response({'error': 'Invalid email'}, status=400)

    User.objects.create_user(username=username, password=password, email=email, google_id=google_id, bio=bio)

    return Response({'message': 'User created successfully'}, status=201)

@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter(
            'user_id', openapi.IN_PATH, type=openapi.TYPE_INTEGER, required=True, description='User ID'
        )
    ],
    responses={
        200: 'User details'
    },
    security=[{'Bearer': []}],
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_by_id(request, user_id):
    """
    Get user details by ID
    """
    requesting_user = request.user
    if not requesting_user.is_staff and requesting_user.id != user_id:
        return Response({'error': 'You do not have permission to view this user'}, status=403)

    user = User.objects.get(id=user_id)
    serializer = UserSerializer(user)
    return Response(serializer.data)

@swagger_auto_schema(
    method='patch',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'user_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='User ID'),
            'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password'),
            'email': openapi.Schema(type=openapi.TYPE_STRING, description='Password'),
            'google_id': openapi.Schema(type=openapi.TYPE_STRING, description='Google ID'),
            'bio': openapi.Schema(type=openapi.TYPE_STRING, description='Bio')
       }, required=['user_id']
    ),
    responses={
        200: 'User updated successfully',
        400: 'Invalid user details',
        403: 'You do not have permission to update this user'
    },
    security=[{'Bearer': []}],
)
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_user(request):
    """
    Update user details. Note that if the user's password is changed, they will be logged out, and the frontend should delete their access and refresh tokens and redirect them to the login page
    """
    user = request.user
    user_data = request.data
    print(user_data)

    if not user_data:
        return Response({'error': 'Please provide details to update'}, status=400)

    # If the user is trying to change someone else's details
    if 'user_id' in user_data and user_data['user_id'] != user.id:
        if not user.is_staff:
            return Response({'error': 'You do not have permission to update this user'}, status=403)


    if 'password' in user_data:
        user.set_password(user_data['password'])
        user_data.pop('password')

        # If the password is changed, the user should be logged out
        refresh_token = RefreshToken.for_user(user)
        refresh_token.blacklist()

    if 'email' in user_data:
        try:
            validate_email(user_data['email'])
        except Exception as e:
            return Response({'error': 'Invalid email'}, status=400)

    # Update the user data
    for key, value in user_data.items():
        setattr(user, key, value)

    user.save()
    return Response(UserSerializer(user).data)