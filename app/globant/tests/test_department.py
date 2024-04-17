"""
Tests for department APIs.
"""

from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Department

from globant.serializers import DepartmentSerializer

DEPARTMENTS_URL = reverse('globant:department-list')


def create_department(**params):
    """Create and return a sample department."""
    defaults = {
        'name': 'Sample department title',
    }
    defaults.update(params)

    department = Department.objects.create(**defaults)
    return department


class PublicDepartmentApiTests(TestCase):
    """Test API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_retrieve_departments(self):
        """Test retrieving a list of department."""
        create_department()
        create_department()

        res = self.client.get(DEPARTMENTS_URL)

        departments = Department.objects.all().order_by('id')
        serializer = DepartmentSerializer(departments, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
