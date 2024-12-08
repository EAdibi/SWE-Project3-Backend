from django.urls import path

from .views import list_lessons, list_public_lessons, list_lessons_by_user, list_lessons_by_category, \
    list_lessons_by_keywords, create_lesson, update_lesson, delete_lesson, get_top_categories, get_lesson_by_id

urlpatterns = [
    path("", list_lessons),
    path("id/<int:id>", get_lesson_by_id),
    path("public", list_public_lessons),
    path("user/<int:user_id>", list_lessons_by_user),
    path("category/<str:category>", list_lessons_by_category),
    path("keywords/<str:keywords>", list_lessons_by_keywords),
    path("new", create_lesson),
    path("update", update_lesson),
    path("delete", delete_lesson),
    path("top-categories", get_top_categories),
]
