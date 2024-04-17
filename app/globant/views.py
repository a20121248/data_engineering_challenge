"""
Views for the job APIs
"""
import pandas as pd
from rest_framework.views import APIView
from rest_framework import viewsets, status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from core.models import Job, Department, Employee
from globant import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.db import connection


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


class EmployeeViewSet(viewsets.ModelViewSet):
    """View for manage employees APIs."""
    serializer_class = serializers.EmployeeSerializer
    queryset = Employee.objects.all()

    def get_queryset(self):
        """Retrieve employees."""
        return self.queryset.order_by('id')


@extend_schema(
    request=serializers.MultipleFileUploadSerializer,
    responses={status.HTTP_201_CREATED: None}
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
            jobs_file = serializer.validated_data.get(
                'jobs_file'
            )
            if jobs_file:
                jobs_df = pd.read_csv(jobs_file,
                                      header=None,
                                      names=['id', 'name'])
                for _, row in jobs_df.iterrows():
                    id = row['id']
                    name = row['name']
                    job, created = Job.objects.get_or_create(
                        id=id,
                        defaults={'name': name}
                    )
                    if not created:
                        # Update the job if already exists
                        job.id = id
                        job.name = name
                        job.save()

            # Process department file
            departments_file = serializer.validated_data.get(
                'departments_file'
            )
            if departments_file:
                departments_df = pd.read_csv(departments_file,
                                             header=None,
                                             names=['id', 'name'])
                for _, row in departments_df.iterrows():
                    id = row['id']
                    name = row['name']
                    department, created = Department.objects.get_or_create(
                        id=id,
                        defaults={'name': name}
                    )
                    if not created:
                        # Update the department if already exists
                        department.id = id
                        department.name = name
                        department.save()

            # Process employee file
            employees_file = serializer.validated_data.get(
                'hired_employees_file'
            )
            if employees_file:
                cols = ['id', 'name', 'datetime', 'department_id', 'job_id']
                employees_df = pd.read_csv(employees_file,
                                           header=None,
                                           names=cols,
                                           parse_dates=['datetime'])
                for _, row in employees_df.iterrows():
                    id = row['id']
                    name = row['name']
                    hire_datetime = row['datetime']
                    department_id = row['department_id']
                    job_id = row['job_id']

                    if pd.isna(department_id) or \
                       pd.isna(job_id) or \
                       pd.isna(hire_datetime):
                        print(
                            "Skipping employee creation due to null value for "
                            f"department_id={department_id}, job_id={job_id} "
                            f"or hire_datetime={hire_datetime}."
                        )
                        continue

                    try:
                        department = Department.objects.get(id=department_id)
                        job = Job.objects.get(id=job_id)
                        employee, created = Employee.objects.get_or_create(
                            id=id,
                            defaults={
                                'name': name,
                                'hire_datetime': hire_datetime,
                                'department': department,
                                'job': job
                            }
                        )
                        if not created:
                            # Update the employee if already exists
                            employee.id = id
                            employee.name = name
                            employee.hire_datetime = hire_datetime
                            employee.department = department
                            employee.job = job
                            employee.save()
                    except ObjectDoesNotExist:
                        # Case where either Department or Job does not exist
                        print(
                            "Skipping employee creation due "
                            "to missing department or job."
                        )

            # Process the uploaded files as needed
            return Response(
                {'status': 'Files uploaded successfully'},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


class Report1ViewSet(viewsets.ModelViewSet):
    """View for report 1."""
    serializer_class = serializers.EmployeeSerializer

    def list(self, request):
        with connection.cursor() as cursor:
            cursor.execute("""
SELECT D.name AS department, J.name AS job,
SUM(CASE WHEN EXTRACT(QUARTER FROM E.hire_datetime)=1 THEN 1 ELSE 0 END) AS Q1,
SUM(CASE WHEN EXTRACT(QUARTER FROM E.hire_datetime)=2 THEN 1 ELSE 0 END) AS Q2,
SUM(CASE WHEN EXTRACT(QUARTER FROM E.hire_datetime)=3 THEN 1 ELSE 0 END) AS Q3,
SUM(CASE WHEN EXTRACT(QUARTER FROM E.hire_datetime)=4 THEN 1 ELSE 0 END) AS Q4
  FROM core_employee AS E
  JOIN core_department AS D ON D.id=E.department_id
  JOIN core_job AS J ON J.id=E.job_id
 WHERE EXTRACT(YEAR FROM E.hire_datetime)=2021
 GROUP BY D.name,J.name
 ORDER BY D.name,J.name;
            """)
            rows = cursor.fetchall()

        data = [{
            'department': row[0],
            'job': row[1],
            'Q1': row[2],
            'Q2': row[3],
            'Q3': row[4],
            'Q4': row[5]} for row in rows]
        return Response(data)


class Report2ViewSet(viewsets.ModelViewSet):
    """View for report 2."""
    serializer_class = serializers.EmployeeSerializer

    def list(self, request):
        with connection.cursor() as cursor:
            cursor.execute("""
SELECT D1.id, D1.name, COUNT(E1.id) AS num_employees_hired
  FROM core_department AS D1
  JOIN core_employee AS E1 ON D1.id=E1.department_id
 WHERE EXTRACT(YEAR FROM E1.hire_datetime)=2021
 GROUP BY D1.id
HAVING COUNT(E1.id) > (SELECT COUNT(E2.id)/COUNT(DISTINCT D2.id)
                            FROM core_department D2
                            JOIN core_employee E2 ON D2.id=E2.department_id
                        WHERE EXTRACT(YEAR FROM E2.hire_datetime)=2021)
 ORDER BY num_employees_hired DESC;
            """)
            rows = cursor.fetchall()

        data = [{'id': row[0],
                 'department': row[1],
                 'hired': row[2]} for row in rows]
        return Response(data)
