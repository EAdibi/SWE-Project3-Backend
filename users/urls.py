from django.urls import path

from .views import list_users, login, logout, get_user, signup, get_user_by_id, update_user, delete_user

urlpatterns = [
    path("", get_user),
    path("list", list_users),
    path("login", login),
    path("logout", logout),
    path("signup", signup),
    path("update", update_user),
    path("delete", delete_user),
    path("user/<int:user_id>", get_user_by_id),
]
