from django import views
from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutPage, name="logout"),
    path('activity_check/<int:id>', views.checkActivity, name="check"),
    path('activity_delete/<int:id>', views.deleteActivity, name="delete"),
    path('add_activity/', views.addActivity, name="add_activity"),
    path('meow/', views.meow, name="meow"),
]
