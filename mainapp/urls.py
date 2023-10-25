from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("", views.test, name="test"),
    # path("add", views.addition, name="add"),
    path("user-list", views.ListUsers.as_view(), name="userlist"),
]