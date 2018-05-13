# -*- coding: utf-8 -*-
# from __future__ import unicode_literals
#
# from django.shortcuts import render

# Create your views here.
# from django.http import Http404
from .models import Album
# from django.template import loader
from django.shortcuts import render, get_object_or_404

def index(request):
    all_albums = Album.objects.all()
    # template = loader.get_template('music/index.html')
    context = {'all_albums': all_albums}
    # return HttpResponse(template.render(context, request))
    return render(request, 'music/index.html', context)

def detail(request, album_id):
    # return HttpResponse('<h2>Here is the album - %s</h2>' % str(album_id))
    # album = Album.objects.get(pk=album_id)
    album = get_object_or_404(Album, pk=album_id)
    return render(request, 'music/detail.html', {'album': album})

def favorite(request, album_id):
    album = get_object_or_404(Album, pk=album_id)
    try:
        selected_song = album.song_set.get(pk=request.POST['song'])
    except (KeyError, Song.DoesNotExist):
        return render(request, 'music/detail.html', {'album': album, 'error_message': "You did not select a valid song."})
    else:
        selected_song.is_favorite = True
        selected_song.save()
        return render(request, 'music/detail.html', {'album': album})
