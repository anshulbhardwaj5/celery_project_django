from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("", views.test, name="test"),
    # path("add", views.addition, name="add"),
    path("user-list", views.ListUsers.as_view(), name="userlist"),
    path("generic-list", views.UserList.as_view(), name="genericlist"),
    path('items/', views.ReturnItemList.as_view(), name="itemmixin"),
    path('create-items', views.CreateItemList.as_view(), name="createitemmixin"),
    path('retrieve-items/<int:pk>/', views.ItemRetrieve.as_view(), name="retrieveitemmixin"), # this is not working
    path('destroy-items/<int:pk>', views.ItemDelete.as_view(), name="deleteitemmixin"),
    path('update-items/<int:pk>', views.ItemUpdate.as_view(), name="updateitemmixin"),
    path('list-create-mixin', views.LCItemList.as_view(), name="listcreatemixin"),
    path('read-update-delete-mixin/<int:pk>', views.ItemRUDMixin.as_view(), name="read-del-updt-mixin"),
]