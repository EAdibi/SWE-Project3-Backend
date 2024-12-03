from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Flashcard
from .serializers import FlashcardSerializer
from django.shortcuts import get_object_or_404

class FlashcardDetailView(APIView):
    def get(self, request, id):
        flashcard = get_object_or_404(Flashcard, id=id)
        serializer = FlashcardSerializer(flashcard)
        return Response(serializer.data)

    def put(self, request, id):
        flashcard = get_object_or_404(Flashcard, id=id)
        serializer = FlashcardSerializer(flashcard, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        flashcard = get_object_or_404(Flashcard, id=id)
        flashcard.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class FlashcardCreateView(APIView):
    def post(self, request):
        serializer = FlashcardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
