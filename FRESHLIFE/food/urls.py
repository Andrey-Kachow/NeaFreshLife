from django.urls import path
from . import views

app_name = 'food'

urlpatterns = [
    path('', views.addfood, name='food'),
    path('add_to_favourite/<int:pk>', views.add_to_favourite, name='add_to_favourite'),
    path('remove_from_favourite/<int:pk>', views.remove_from_favourite, name='remove_from_favourite'),
    path('add_to_ignore/<int:pk>', views.add_to_ignore, name='add_to_ignore'),
    path('remove_from_ignore/<int:pk>', views.remove_from_ignore, name='remove_from_ignore'),

    path('item/<int:pk>', views.food_item, name='food_item'),
    # path('item/add_to_favourite/<int:pk>', views.add_to_favourite, name='add_to_favourite'),
    # path('item/remove_from_favourite/<int:pk>', views.remove_from_favourite, name='remove_from_favourite'),
    # path('item/add_to_ignore/<int:pk>', views.add_to_ignore, name='add_to_ignore'),
    # path('item/remove_from_ignore/<int:pk>', views.remove_from_ignore, name='remove_from_ignore'),
]

