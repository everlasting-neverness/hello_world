# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from journal.models import Kid, Journal
from django.utils import timezone
from .serializers import JournalSerializer, KidSerializer
from django.db.models import Q

from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, UpdateModelMixin
from rest_framework.views import APIView

from django.test.client import encode_multipart, RequestFactory

import datetime


class CreateKid(CreateModelMixin, ListAPIView):
    lookup_field = 'pk'
    serializer_class = KidSerializer

    def get_queryset(self):
        qs = Kid.objects.all()
        return qs

    def post(self, request, *args, **kwargs):
        context = request
        serializer = KidSerializer(data=request.data, context=context)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response()

@api_view(['GET', 'PUT', 'DELETE'])
def view_kid(request, pk):
    if request.method == 'GET':
        kid = Kid.objects.get(pk=pk)
        serializer = KidSerializer(kid)
        return Response(serializer.data)

    elif request.method == 'PUT':
        kid = Kid.objects.get(pk=pk)
        context = request
        serializer = KidSerializer(kid, data=request.data, context=context)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        kid = Kid.objects.get(pk=pk)
        kid.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class LogViewAndPost(CreateModelMixin, ListAPIView):
    lookup_field = 'pk'
    serializer_class = JournalSerializer

    def get_queryset(self):
        qs = Journal.objects.filter(departure='')
        return qs

    def post(self, request, *args, **kwargs):
        context = request
        serializer = JournalSerializer(data=request.data, context=context)
        if serializer.is_valid():
            serializer.save()
            print 'save'
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print 'miss'
        return Response()

@api_view(['GET', 'PUT', 'DELETE'])
def view_log(request, pk):
    if request.method == 'GET':
        log = Journal.objects.get(pk=pk)
        serializer = JournalSerializer(log)
        return Response(serializer.data)

    elif request.method == 'PUT':
        log = Journal.objects.get(pk=pk)
        context = request
        serializer = JournalSerializer(log, data=request.data, context=context)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        log = Journal.objects.get(pk=pk)
        log.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
