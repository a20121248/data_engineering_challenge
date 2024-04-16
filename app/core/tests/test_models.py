"""
Tests for models.
"""
from decimal import Decimal

from django.test import TestCase

from core import models

class ModelTests(TestCase):
    """Test models."""
    
    def test_create_job(self):
        """Test creating a job is successful."""
        job = models.Job.objects.create(
            name='Sample Job title',
        )

        self.assertEqual(str(job), job.name)