
"""
Serializers for job APIs
"""
from rest_framework import serializers

from core.models import (
    Job,
    Department,
    Employee,
)


class JobSerializer(serializers.ModelSerializer):
    """Serializer for jobs."""
    class Meta:
        model = Job
        fields = ['id', 'name']


class DepartmentSerializer(serializers.ModelSerializer):
    """Serializer for deparments."""
    class Meta:
        model = Department
        fields = ['id', 'name']


class EmployeeSerializer(serializers.ModelSerializer):
    """Serializer for employees."""
    class Meta:
        model = Employee
        fields = ['id', 'name', 'hire_datetime', 'department', 'job']


class MultipleFileUploadSerializer(serializers.Serializer):
    """Serializer for uploading multiple files."""
    departments_file = serializers.FileField()
    hired_employees_file = serializers.FileField()
    jobs_file = serializers.FileField()
