from django.conf.urls import url
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from journal import views

urlpatterns = [
    url(r'^journal/$', views.journal_list),
    url(r'^journal/(?P<pk>[0-9]+)$', views.kid_detail),
]

urlpatterns = format_suffix_patterns(urlpatterns)
