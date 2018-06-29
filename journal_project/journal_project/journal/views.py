# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from journal.models import Kid, Journal

# @api_view(['GET', 'POST'])
# def journal_list(request):
#     if request.method == 'GET':
#         journal_items = Journal.objects.all()
#         serializer = JournalSerializer(journal_items, many=True)
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = JournalSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
# @api_view(['POST'])
# def create_kid(request):
