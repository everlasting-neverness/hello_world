# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .forms import SignUpForm, ContactForm

def home(request):
    title = "Welcome"
    # if request.user.is_authenticated():
    #     title = "My title %s" % (request.user)
    form = SignUpForm(request.POST or None) # without None it will always show error-validating message on the page
    context = {
        "title": title,
        "form": form,
    }
    if form.is_valid():
        instance = form.save(commit=False)
        full_name = form.cleaned_data.get('full_name')
        if not full_name:
            full_name = "New full name"
        instance.full_name = full_name
        instance.save()
        context = {
            "title": "Thank you"
        }
    return render(request, "home.html", context)

def contact(request):
    form = ContactForm(request.POST or None)
    if form.is_valid():
        email = cleaned_data.get("email")
        full_name = cleaned_data.get("full_name")
        message = cleaned_data.get("message")
    context = {
        'form': form,
    }
    return render(request, 'forms.html', context)
