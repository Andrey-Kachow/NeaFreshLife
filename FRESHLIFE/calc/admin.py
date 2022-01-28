from django.contrib import admin
from .models import Activity, Latest_inputs

# registering the models from calc/models.py
admin.site.register(Activity)
admin.site.register(Latest_inputs)

