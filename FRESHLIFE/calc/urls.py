from django.urls import path, include
from . import views

app_name = 'calc'

urlpatterns = [
    path('', views.calculator, name='calculator'),
    path('<int:user_came_from_planner>/', views.calculator, name='calculator2'),
]  # calculator2 redirects user to the meal planner instead of showing results

