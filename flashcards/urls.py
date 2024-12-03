from django.urls import path
from .views import FlashcardDetailView, FlashcardCreateView

urlpatterns = [
    path('<int:id>/', FlashcardDetailView.as_view(), name='flashcard-detail'),  # For GET, PUT, DELETE
    path('', FlashcardCreateView.as_view(), name='flashcard-create'),  # for POST
]
