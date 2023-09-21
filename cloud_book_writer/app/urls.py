from django.urls import path
from . import views
from .views import (
    SignUp,
    Login,
    Author,
    LogoutView,
    CreateSection,
    Collaborator,
    Book,
    ViewEditSection,
    CreateBook,
)


urlpatterns = [
    path("", SignUp.as_view(), name="sign-up"),
    path("login/", Login.as_view(), name="login"),
    path("author/", Author.as_view(), name="author"),
    path("collab/", Collaborator.as_view(), name="collab"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("section/", CreateSection.as_view(), name="section"),
    path("ajax/load-sections/", views.load_sections, name="ajax_load_sections"),
    path("book/", Book.as_view(), name="book"),
    path("book/<int:id>/", Book.as_view(), name="book"),
    path("edit-section/", ViewEditSection.as_view(), name="edit-section"),
    path("edit-section/<int:id>/", ViewEditSection.as_view(), name="edit-section"),
    path("create-book/", CreateBook.as_view(), name="create-book"),
    path("edit-book/<int:id>/", CreateBook.as_view(), name="edit-book"),
]
