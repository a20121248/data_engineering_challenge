"""
Django admin customization.
"""
from django.contrib import admin

from core import models

admin.site.register(models.Job)
admin.site.register(models.Department)
admin.site.register(models.Employee)
