from django.db import models
from django.conf import settings #reference AUTH_USER_MODEL

# Create your models here.
class Flashcard(models.Model):
    front_text = models.TextField()
    back_text = models.TextField()
    lesson = models.ForeignKey('Lesson', on_delete=models.CASCADE, related_name='flashcards') #link to lesson
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) #link to user

    #Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
