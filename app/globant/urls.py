"""
URL mappings for the job app.
"""
from django.urls import path
from rest_framework.routers import DefaultRouter
from globant.views import (
    JobViewSet,
    DepartmentViewSet,
    EmployeeViewSet,
    MultipleFileUploadView,
    Report1ViewSet,
    Report2ViewSet,
) 

router = DefaultRouter()
router.register('jobs', JobViewSet, basename='jobs')
router.register('departments', DepartmentViewSet, basename='departments')
router.register('employees', EmployeeViewSet, basename='employees')

app_name = 'globant'

urlpatterns = [
    path('departments/', DepartmentViewSet.as_view({'get': 'list'}), name='department-list'),
    path('hired-employees/', EmployeeViewSet.as_view({'get': 'list'}), name='employee-list'),
    path('jobs/', JobViewSet.as_view({'get': 'list'}), name='job-list'),
    path('upload-files/', MultipleFileUploadView.as_view(), name='multiple-file-upload'),
    path('report-1/', Report1ViewSet.as_view({'get': 'list'}), name='report-1-list'),
    path('report-2/', Report2ViewSet.as_view({'get': 'list'}), name='report-2-list'),
]