# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Album, Song


class AlbumModelAdmin(admin.ModelAdmin):
    list_display = ['album_title', 'artist', 'genre', 'pk',]
    list_filter = ['artist', 'genre']
    search_fields = ['album_title', 'artist']
    class Meta:
        model = Album

class SongModelAdmin(admin.ModelAdmin):
    list_display = ['song_title', 'album', 'file_type', 'pk',]
    list_filter = ['song_title', 'file_type']
    search_fields = ['song_title', 'file_type']
    class Meta:
        model = Song


admin.site.register(Album, AlbumModelAdmin)
admin.site.register(Song, SongModelAdmin)
