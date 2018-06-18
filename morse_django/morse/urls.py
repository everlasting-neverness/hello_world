from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', views.main_page, name="main_page"),
    url(r'^about/$', views.about, name="about")
]
