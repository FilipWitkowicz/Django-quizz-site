from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.loginPage, name="login"),
    path("logout/", views.logoutUser, name="logout"),
    path("register/", views.registerPage, name="register"),
    #
    path("", views.home, name="home"),
    path("ranking/", views.ranking, name="ranking"),
    path("quest/<str:pk>", views.quest, name="quest"),
    path("profile/<str:pk>", views.userProfile, name="user-profile"),
    path("followPage/<str:pk>", views.followPage, name="followPage"),
    path("edit-user/<str:pk>", views.editUser, name="edit-user"),
    # CRUD
    path("create-quest/", views.createQuest, name="create-quest"),
    path("edit-quest/<str:pk>", views.editQuest, name="edit-quest"),
    path("delete-quest/<str:pk>", views.deleteQuest, name="delete-quest"),
]
