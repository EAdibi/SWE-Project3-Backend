from django.urls import path

from .views import hello, hello_user, hello_return_dictionary

# Here we map urls to specific views
# These urls are added to the main urls.py file in the QuizWhiz_backend folder
urlpatterns = [
    path("", hello),
    path("<str:username>", hello_user),
    # Be careful with the order of the paths. The one with the variable should be at the end
    path("test/dictionary", hello_return_dictionary),

]
