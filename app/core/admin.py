"""
Django admin customization.
"""
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from core import models

admin.site.register(models.Job)