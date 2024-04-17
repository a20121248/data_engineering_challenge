"""
Tests for job APIs.
"""
from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Job

from globant.serializers import JobSerializer

JOBS_URL = reverse('globant:job-list')

def create_job(**params):
    """Create and return a sample job."""
    defaults = {
        'name': 'Sample job title',
    }
    defaults.update(params)

    job = Job.objects.create(**defaults)
    return job

class PublicJobApiTests(TestCase):
    """Test API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_retrieve_jobs(self):
        """Test retrieving a list of jobs."""
        create_job()
        create_job()

        res = self.client.get(JOBS_URL)

        jobs = Job.objects.all().order_by('id')
        serializer = JobSerializer(jobs, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)