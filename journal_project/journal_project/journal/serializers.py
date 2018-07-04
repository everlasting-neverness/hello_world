from rest_framework import serializers
from .models import Kid, Journal

class JournalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Journal
        fields = ('pk', 'kid_id', 'arrival', 'departure', 'parents', 'date')

class KidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kid
        fields = ('name', 'pk', 'gender', 'birthday', 'grade', 'photo', 'status')
