from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

class Kid(models.Model):
    name = models.CharField(max_length=250)
    gender = models.CharField(max_length=20)
    birthday = models.CharField(max_length=10)
    grade = models.CharField(max_length=10)
    status = models.CharField(max_length=50)
    photo = models.FileField(blank=True)

    def __str__(self):
        return self.name

class Journal(models.Model):
    kid_id = models.ForeignKey(Kid, on_delete=models.CASCADE)
    date = models.CharField(max_length=10) #default = date.today
    arrival = models.CharField(max_length=25)
    departure = models.CharField(max_length=25, blank=True)
    parents = models.CharField(max_length=250)


    def __str__(self):
        return 'Journal'
