"""
Database models.
"""

from django.db import models


class Job(models.Model):
    """
    Job object.
    """
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Department(models.Model):
    """
    Department object.
    """
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Employee(models.Model):
    """
    Employee object.
    """
    name = models.CharField(max_length=100)
    hire_datetime = models.DateTimeField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
