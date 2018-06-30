from rest_framework import serializers
from .models import Kid, Journal

class JournalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Journal
        fields = ('pk', 'name', 'arrival_time', 'departure_time', 'parents', 'date')

class KidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kid
        fields = ('name', 'pk', 'sex', 'birthday', 'grade', 'photo', 'is_present')
