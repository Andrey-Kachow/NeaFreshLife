from django.urls import path, include
from . import views

app_name = "planner"

urlpatterns = [
    path('', views.meal_planner, name='meal_planner')
]

