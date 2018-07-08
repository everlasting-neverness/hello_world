from django.conf.urls import url
from . import views

app_name = 'music'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^register/$', views.UserFormView.as_view(), name='register'),
    url(r'^logout/$', views.logout_view , name='logout'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^album/add/$', views.AlbumCreate.as_view(), name='album-add'),
    url(r'^album/(?P<pk>[0-9]+)/update/$', views.AlbumUpdate.as_view(), name='album-update'),
    url(r'^album/(?P<pk>[0-9]+)/delete/$', views.AlbumDelete.as_view(), name='album-delete'),
    url(r'^album/(?P<pk>[0-9]+)/add_song/$', views.SongAdd.as_view(), name='song-add'),
    url(r'^album/(?P<album_id>[0-9]+)/song/(?P<pk>[0-9]+)/update/$', views.SongUpdate.as_view(), name='song-update'),
    url(r'^album/(?P<album_id>[0-9]+)/song/(?P<pk>[0-9]+)/delete/$', views.SongDelete.as_view(), name='song-delete'),
    url(r'^albumlist/$', views.AlbumList.as_view()),
    url(r'^(?P<pk>[0-9]+)/songlist/$', views.SongList.as_view())
]
