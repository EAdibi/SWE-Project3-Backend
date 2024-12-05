from django.urls import path
from .views import FlashcardDetailView, FlashcardCreateView,FlashcardListView

urlpatterns = [
    path('<int:id>/', FlashcardDetailView.as_view(), name='flashcard-detail'),  # For GET, PUT, DELETE
    path('', FlashcardCreateView.as_view(), name='flashcard-create'),  # for POST
    path('public/', FlashcardListView.as_view(), name='flashcard-list'),  # for GET
]
