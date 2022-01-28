from django.contrib import admin
from . import models
# Registering models from planner/models.py
admin.site.register(models.Plan)
admin.site.register(models.Meal)
admin.site.register(models.Meal_has_Food)

