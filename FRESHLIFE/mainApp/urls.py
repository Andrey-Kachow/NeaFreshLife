from django.urls import path, include
from . import views

app_name = "mainApp"

urlpatterns = [
    path('', views.mainPage, name='mainPage'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_user, name='logout_user'),
]

