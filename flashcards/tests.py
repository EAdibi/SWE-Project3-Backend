from django.test import TestCase

# Create your tests here.
from django.contrib.auth import get_user_model
from lessons.models import Lesson
from flashcards.models import Flashcard

class FlashcardModelTest(TestCase):
    def setUp(self):
        # Create a user
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='password123'
        )
        
        # Create a lesson
        self.lesson = Lesson.objects.create(
            title="Sample Lesson",
            description="Description of the lesson",
            category="Category",
            user=self.user,
            is_public=True
        )

        # Create a flashcard
        self.flashcard = Flashcard.objects.create(
            front_text="What is Python?",
            back_text="A programming language.",
            lesson=self.lesson,
            created_by=self.user
        )

    def test_flashcard_creation(self):
        # test if the flashcard is created successfully
        self.assertEqual(self.flashcard.front_text, "What is Python?")
        self.assertEqual(self.flashcard.back_text, "A programming language.")
        self.assertEqual(self.flashcard.lesson, self.lesson)
        self.assertEqual(self.flashcard.created_by, self.user)

    def test_flashcard_str_representation(self):
        # test the string representation of the Flashcard model
        self.assertEqual(str(self.flashcard), "What is Python?")
