"""
Views for the job APIs
"""
import pandas as pd
from rest_framework.views import APIView
from rest_framework import (
    viewsets,
    mixins,
    status,
)
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets
from drf_spectacular.utils import extend_schema
from core.models import (
    Job,
    Department,
)
from globant import serializers

class JobViewSet(viewsets.ModelViewSet):
    """View for manage job APIs."""
    serializer_class = serializers.JobSerializer
    queryset = Job.objects.all()

    def get_queryset(self):
        """Retrieve jobs."""
        return self.queryset.order_by('id')
    
class DepartmentViewSet(viewsets.ModelViewSet):
    """View for manage department APIs."""
    serializer_class = serializers.JobSerializer
    queryset = Department.objects.all()

    def get_queryset(self):
        """Retrieve departments."""
        return self.queryset.order_by('id')
    
@extend_schema(
    request=serializers.MultipleFileUploadSerializer,  # Specify the request serializer
    responses={status.HTTP_201_CREATED: None}  # Specify the response schema
)
class MultipleFileUploadView(APIView):
    """
    View for uploading multiple files.
    """
    serializer_class = serializers.MultipleFileUploadSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            # Process job file
            jobs_file = serializer.validated_data.get('jobs_file')
            if jobs_file:
                jobs_df = pd.read_csv(jobs_file, header=None, names=['id','name'])
                for _, row in jobs_df.iterrows():
                    id = row['id']
                    name = row['name']
                    job, created = Job.objects.get_or_create(id=id, defaults={'name':name})
                    if not created:
                        # If the job already exists, update its name
                        job.id = id
                        job.name = name
                        job.save()

            # Process department file
            departments_file = serializer.validated_data.get('departments_file')
            if departments_file:
                departments_df = pd.read_csv(departments_file, header=None, names=['id','name'])
                for _, row in departments_df.iterrows():
                    id = row['id']
                    name = row['name']
                    department, created = Department.objects.get_or_create(id=id, defaults={'name':name})
                    if not created:
                        # If the department already exists, update its name
                        department.id = id
                        department.name = name
                        department.save()
                    
            # Process employee file
            employees_file = serializer.validated_data.get('employees_file')
            if employees_file:
                jobs_df = pd.read_csv(employees_file, header=None, names=['id','name','datetime','department_id','job_id'])
            
            # Process the uploaded files as needed
            return Response({'status': 'Files uploaded successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
