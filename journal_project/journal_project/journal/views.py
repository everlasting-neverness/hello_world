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


# works for viewing and changing kid profile. No photo
class KidView(RetrieveUpdateAPIView):
# class KidView(CreateModelMixin, ListAPIView):
    lookup_field = 'pk'
    serializer_class = KidSerializer

    def get_queryset(self):
        qs = Kid.objects.all()
        query = self.request.GET.get('q')
        if query is not None:
            qs = qs.filter(Q(pk=query)).distinct()
        return qs

    # def post(self, request, *args, **kwargs):
    #     return self.create(request, *args, **kwargs)

# works for creating new kid profile. No photo
class CreateKid(CreateModelMixin, APIView):
    lookup_field = 'pk'
    serializer_class = KidSerializer

    def post(self, request, *args, **kwargs):
        context = request
        serializer = KidSerializer(data=request.data, context=context)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response()

# @api_view(['GET', 'POST'])
# def journal_list(request):
#     if request.method == 'GET':
#         kids = Kid.objects.filter(is_present=False) # just for now
#         # journal_items = Journal.objects.filter(
#         # serializer = JournalSerializer(journal_items, many=True)
#         print kids.distinct().values()
#         kids = [child.pk for child in kids]
#         # print kids
#
#         # journal_items = [Journal.objects.filter(name=item) for item in kids]
#         # journal_items = (lambda x: Journal.objects.filter(name=x), kids)
#         # print journal_items
#         o = Journal.objects.all()
#         print o
#         # serializer = JournalSerializer(journal_items, many=True)
#         serializer = JournalSerializer(o, many=True)
#         print serializer.data
#         # return Response(serializer.data)
#         t = timezone.now()
#         print t
#         return Response('wg')
#
#     elif request.method == 'POST':
#         serializer = JournalSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# PUT does't work
@api_view(['GET', 'PUT'])
def view_kid(request, pk):
    if request.method == 'GET':
        kid = Kid.objects.get(pk=pk)
        serializer = KidSerializer(kid)
        return Response(serializer.data)
    elif request.method == 'PUT':
        context = request
        serializer = KidSerializer(data=request.data, context=context)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def create_kid(request):
    # if request.method == 'GET':
    #     k = Kid.objects.all()[0]
    #     a = KidSerializer(k)
    #     # a.is_valid()
    #     return Response(a.data)

    if request.method == 'POST':
        context = request
        serializer = KidSerializer(data=request.data, context=context)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response()
