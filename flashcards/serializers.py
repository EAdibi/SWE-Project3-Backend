from rest_framework import serializers
from .models import Flashcard

class FlashcardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flashcard
        fields = ['id', 'front_text', 'back_text', 'lesson', 'created_by', 'created_at', 'updated_at']
