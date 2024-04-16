
"""
Serializers for job APIs
"""
from rest_framework import serializers

from core.models import Job, Department

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
        
class MultipleFileUploadSerializer(serializers.Serializer):
    """
    Serializer for uploading multiple files.
    """
    jobs_file = serializers.FileField()
    departments_file = serializers.FileField()
    employees_file = serializers.FileField()
