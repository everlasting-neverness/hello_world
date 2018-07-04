# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Kid, Journal


class KidModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'status']
    list_filter = ['status']
    search_fields = ['name']
    class Meta:
        model = Kid

class JournalModelAdmin(admin.ModelAdmin):
    list_display = ['kid_id', 'departure', 'arrival', 'date']
    list_filter = ['arrival', 'kid_id']
    search_fields = ['kid_id']
    class Meta:
        model = Journal

admin.site.register(Kid, KidModelAdmin)
admin.site.register(Journal, JournalModelAdmin)
