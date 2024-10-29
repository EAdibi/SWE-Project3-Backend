from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request

# Create your views here.
# Decorator to establish that the view takes a GET request
@api_view(['GET'])
def hello(request: Request):
    return Response("Hello, world!")

@api_view(['GET'])
def hello_user(request: Request, username: str): # Note that the function can take in extra params based on what we say in the urls.py file
    return Response(f"Hello, {username}!")

@api_view(['GET'])
def hello_return_dictionary(request: Request):
    return Response({"My custom Message Name": "Hello, world!"})