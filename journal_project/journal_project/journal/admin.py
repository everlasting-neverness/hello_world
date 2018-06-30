# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Kid, Journal


class KidModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_present']
    list_filter = ['is_present']
    search_fields = ['name']
    class Meta:
        model = Kid

class JournalModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'departure_time', 'arrival_time', 'date']
    list_filter = ['arrival_time', 'name']
    search_fields = ['name']
    class Meta:
        model = Journal

admin.site.register(Kid, KidModelAdmin)
admin.site.register(Journal, JournalModelAdmin)
