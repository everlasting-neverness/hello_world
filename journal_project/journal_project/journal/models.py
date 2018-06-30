# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

class Kid(models.Model):
    name = models.CharField(max_length=250)
    sex = models.CharField(max_length=20)
    birthday = models.CharField(max_length=10)
    grade = models.CharField(max_length=10)
    is_present = models.BooleanField(default=False)
    photo = models.FileField(blank=True)

    def __str__(self):
        return self.name

class Journal(models.Model):
    name = models.ForeignKey(Kid, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True, auto_now=False) #default = date.today
    arrival_time = models.DateTimeField(auto_now_add=False, auto_now=True)
    departure_time = models.DateTimeField(auto_now_add=False, auto_now=True)
    parents = models.CharField(max_length=250)


    def __str__(self):
        return 'Journal'

# class JournalManager(models.Manager):
#     #all change for active because when edit existing post all will give an error
#     def active(self, *args, **kwargs):
#         #Post.objects.all() = super(PostManager, self).all() - the same things
#         return super(JournalManager, self).filter(draft=False).filter(arrival_time__lte=timezone.now())
