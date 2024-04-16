"""
URL mappings for the job app.
"""
from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from globant.views import (
    JobViewSet,
    DepartmentViewSet,
    MultipleFileUploadView,
) 

router = DefaultRouter()
router.register('jobs', JobViewSet, basename='jobs')
router.register('departments', DepartmentViewSet, basename='departments')

app_name = 'globant'

#path('', include(router.urls)),
urlpatterns = [
    path('jobs/', JobViewSet.as_view({'get': 'list'}), name='job-list'),
    path('departments/', DepartmentViewSet.as_view({'get': 'list'}), name='department-list'),
    path('upload-files/', MultipleFileUploadView.as_view(), name='multiple-file-upload'),
]