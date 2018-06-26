from rest_framework import serializers
from .models import Song, Album

class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ('artist', 'album_title', 'genre', 'album_logo')
        read_only_fields = ('album_logo', )

class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        # fields = ('album', 'song_title', 'file_type')
        exclude = ('is_favorite', )
