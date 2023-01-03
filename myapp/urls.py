from django.urls import path
from . import views
urlpatterns = [
    path("", views.home, name="home"),
    path("room/<str:roomId>", views.room, name="room"),
    path("user/<str:userId>", views.userPage, name="user-page"),
    path("create-room/", views.createRoom, name="create-room"),
    path("update-room/<str:roomId>", views.updateRoom, name="update-room"),
    path("delete-room/<str:roomId>", views.deleteRoom, name="delete-room"),
    path("login/", views.loginPage, name="login"),
    path("logout/", views.logoutUser, name='logout'),
    path("register/", views.registerPage, name='register'),
    path("delete-message/<str:mesgId>", views.deleteMessage, name="delete-message")
]