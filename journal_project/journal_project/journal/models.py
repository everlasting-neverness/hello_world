# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Kid(models.Model):
    name = models.CharField(max_length=250)
    sex = models.CharField(max_length=20)
    birthday = models.CharField(max_length=10)
    grade = models.CharField(max_length=10)
    is_present = models.BooleanField(default=False)
    photo = models.FileField()

class Journal(models.Model):
    kid_name = models.ForeignKey(Kid, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True, auto_now=False)
    arrival_time = models.DateTimeField(auto_now_add=False, auto_now=True)
    leaving_time = models.DateTimeField(auto_now_add=False, auto_now=True)
    parents = models.CharField(max_length=250)
