from django.conf.urls import url
from . import views

urlpatterns = [
    # url(r'^$', views.journal_list),
    # url(r'^(?P<pk>[0-9]+)/$', views.view_kid),
    url(r'^create_kid/$', views.CreateKid.as_view()),
    url(r'^(?P<pk>[0-9]+)/$', views.KidView.as_view())
]
