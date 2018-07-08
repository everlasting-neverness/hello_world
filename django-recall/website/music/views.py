from django.views import generic
from django.views.generic import View
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, UpdateModelMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Album, Song
from .serializers import AlbumSerializer, SongSerializer
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import UserForm


class AlbumList(UpdateModelMixin, APIView):
    # lookup_field = 'pk'
    # serializer_class = AlbumSerializer
    #
    # def get_queryset(self):
    #     return Album.objects.all()

    def put(self, request, *args, **kwargs):
        pk = request.data['pk']
        album = Album.objects.get(pk=pk)
        serializer = AlbumSerializer(album, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        albums = Album.objects.all()
        serializer = AlbumSerializer(albums, many=True)
        return Response(serializer.data)

class SongList(CreateModelMixin, RetrieveUpdateDestroyAPIView):
    # lookup_field = 'pk'
    serializer_class = SongSerializer

    def get_queryset(self):
        print self.kwargs.get('pk')
        # return Song.objects.filter(album=self.kwargs.get('pk'))
        return Song.objects.all()

    def get(self, request, pk):
        # pk = self.kwargs.get('pk')
        songs = Song.objects.filter(album=pk)
        serializer = SongSerializer(songs, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        context = request
        serializer = SongSerializer(data=request.data, context=context)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response()

    # def put(self, request, *args, **kwargs):
    #     pk = request.data['pk']
    #     song = Song.objects.get(pk=pk)
    #     serializer = SongSerializer(song, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #
    #
    # def delete(self, request, *args, **kwargs):
    #     pk = request.data['pk']
    #     song = Song.objects.get(pk=pk)
    #     song.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)



class UserFormView(View):
    form_class = UserForm
    template_name = 'music/registration_form.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # sets the password because of hash and so on
            user.set_password(password)
            user.save()

            # returns User object if all inputs are correct
            user = authenticate(username=username, password=password)
            if user is not None:
                # django allows to ban users e.t.c. so this is validation for it
                if user.is_active:
                    login(request, user)
                    return redirect('music:index')
        return render(request, self.template_name, {'form': form})

def logout_view(request):
    logout(request)
    return redirect('music:index')

class IndexView(generic.ListView):
    template_name = 'music/index.html'
    context_object_name = 'all_albums'

    def get_queryset(self):
        return Album.objects.all()

class DetailView(generic.DetailView):
    model = Album
    template_name = 'music/detail.html'

class AlbumCreate(CreateView):
    model = Album
    fields = ['artist', 'album_title', 'genre', 'album_logo']

class AlbumUpdate(UpdateView):
    model = Album
    fields = ['artist', 'album_title', 'genre', 'album_logo']
    template_name = 'music/album_form.html'
    template_name_suffix = '_update_form'

class AlbumDelete(DeleteView):
    model = Album
    template_name = 'music/album_form.html'
    template_name_suffix = '_check_delete'
    success_url = reverse_lazy('music:index')

class SongAdd(CreateView):
    model = Song
    fields = ['song_title', 'album', 'file_type']
    template_name = 'music/song-template.html'

class SongUpdate(UpdateView):
    model = Song
    fields = ['song_title', 'album', 'file_type', 'is_favorite']
    template_name = 'music/song-template.html'
    template_name_suffix = '_update_form'

class SongDelete(DeleteView):
    model = Song
    template_name = 'music/song-template.html'
    template_name_suffix = '_check_delete'
    success_url = reverse_lazy('music:index')
