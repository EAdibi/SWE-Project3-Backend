from django.urls import path
from .views import FlashcardDetailView, FlashcardCreateView,FlashcardListView, FlashcardByLessonView

urlpatterns = [
    path('<int:id>/', FlashcardDetailView.as_view(), name='flashcard-detail'),  # For GET, PUT, DELETE
    path('', FlashcardCreateView.as_view(), name='flashcard-create'),  # for POST
    path('public/', FlashcardListView.as_view(), name='flashcard-list'),  # for GET
    path('by-lesson/<int:id>/', FlashcardByLessonView.as_view(), name='flashcard-by-lesson'),  # for GET
]
