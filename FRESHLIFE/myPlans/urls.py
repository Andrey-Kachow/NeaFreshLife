from django.urls import path
from . import views

app_name = 'myPlans'

urlpatterns = [
    path('', views.user_plans, name='plans'),
    path('<int:index>', views.user_plan, name='plan'),
    path('delete/<int:pk>', views.delete_plan, name='delete'),
]
