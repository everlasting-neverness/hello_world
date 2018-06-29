from rest_framework import serializers
from .models import Kid, Journal

class JournalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Journal
        fields = ('pk', 'kid_name', 'arrival_time', 'leaving_time', 'parents', 'date')

class KidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kid
        fields = ('name', 'sex', 'birthday', 'grade', 'photo', 'is_learning_now')
