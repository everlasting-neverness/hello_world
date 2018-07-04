from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^logs/$', views.LogViewAndPost.as_view()),
    url(r'^logs/(?P<pk>[0-9]+)/$', views.view_log),
    url(r'^kids/(?P<pk>[0-9]+)/$', views.view_kid),
    url(r'^kids/$', views.CreateKid.as_view()),
]
