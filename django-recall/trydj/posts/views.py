# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from urllib import quote_plus
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.utils import timezone
from .forms import PostForm
from .models import Post
from .serializers import PostSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class PostList(APIView):
    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        # print serializer.data
        return Response(serializer.data)

    def post(self, request):
        pass    




def post_list(request):
    # queryset_list = Post.objects.filter(draft=False).filter(publish__lte=timezone.now()) # __lte - means 'less than or equalls to'. timezone.now() - the current time
    today = timezone.now().date()
    queryset_list = Post.objects.active()
    if request.user.is_staff or request.user.is_superuser:
        queryset_list = Post.objects.all()
    query = request.GET.get('q')
    if query:
        queryset_list = queryset_list.filter(
            Q(title__icontains=query)|
            Q(content__icontains=query)|
            Q(user__first_name__icontains=query)|
            Q(user__last_name__icontains=query)
            ).distinct()
    # | means q(smth) OR q(smth) OR .. distinct - makes duplicates not to appear
    paginator = Paginator(queryset_list, 6) # Show 25 contacts per pagepag
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)
    context = {
        'object_list': queryset,
        'title': 'List',
        'page_request_var': page_request_var,
        'today': today
    }
    return render(request, 'post_list.html', context = context)

def post_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        messages.success(request, "Successfully created")
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        'form': form,
    }
    return render(request, 'post_form.html', context = context)

def post_detail(request, slug=None):
    instance = get_object_or_404(Post, slug=slug)
    if instance.draft or instance.publish > timezone.now().date():
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404
    share_string = quote_plus(instance.content)
    context = {
        'title': instance.title,
        'instance': instance,
        'share_string': share_string
    }
    return render(request, 'post_detail.html', context = context)

def post_update(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post, slug=slug)
    form = PostForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Successfully saved")
        return HttpResponseRedirect(instance.get_absolute_url())
    elif form.errors:
        messages.error(request,"Didn't save a post")
    context = {
        'title': instance.title,
        'instance': instance,
        'form': form,
    }
    return render(request, 'post_form.html', context = context)

def post_delete(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post, slug=slug)
    instance.delete()
    messages.success(request, "Successfully deleted")
    return redirect('posts:list')
