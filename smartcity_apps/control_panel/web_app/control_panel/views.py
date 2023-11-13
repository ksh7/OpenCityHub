from datetime import datetime
import os
import json
import random
import string

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse, StreamingHttpResponse, FileResponse
from wsgiref.util import FileWrapper
from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django_htmx.http import trigger_client_event

from web_app.settings import MEDIA_URL, BASE_DIR

from . import models
from . import forms
from . import tasks
from . import rabbitmq_producer
from . import chatgpt


def index(request):
    context = {}
    return render(request, 'control_panel/index.html', context)


@login_required
def dashboard(request):
    context = {}
    return render(request, 'control_panel/dashboard.html', context)

@login_required
def ask_gpt(request):

    ## TODO: supply real json data from databases in 'data_set' to get a response.
    gpt_response = chatgpt.gpt_api(prompt_ques=request.POST.get('gptquestion'), data_set={})

    ## NOTE: returning dummy response in lack of real data
    import time
    time.sleep(1)
    gpt_response = "Traffic congestion in New York City has diminished over the past week, with a noticeable 20% decrease. This positive shift is attributed to increased remote work, optimized traffic flow management, and ongoing urban planning efforts. The data underscores progress in alleviating congestion and enhancing the city's transportation dynamics."
    return JsonResponse({'status': 'success', 'data': gpt_response})

@login_required
def sample_task(request):
    tasks.sample_task.delay(2, 5)
    return HttpResponse("Task Sent")

@login_required
def sample_publish(request):
    rabbitmq_producer.publish('sample_publish', {'msg': 'msg from control_panel'})
    return HttpResponse("Published")


@login_required
def smartcity_apps(request):
    context = {}
    return render(request, 'control_panel/smartcity_apps.html', context)


@login_required
def profile_settings(request):
    context = {}
    return render(request, 'control_panel/profile_settings.html', context)

@login_required
def serverless_apps(request):
    context = {}
    return render(request, 'control_panel/serverless_apps.html', context)


@login_required
def openshift_cloud(request):
    context = {}
    return render(request, 'control_panel/openshift_cloud.html', context)


def registerUser(request):
    if request.method == 'POST':
        form = forms.RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            login(request, user)
            return redirect('dashboard')  # Change 'home' to your desired redirect URL
    else:
        form = forms.RegistrationForm()
    
    context = {'form': form}
    return render(request, 'control_panel/register.html', context)


def favicon_ico(request):
    favicon_path = os.path.join(settings.BASE_DIR, 'static', 'favicon.ico')
    return serve(request, os.path.basename(favicon_path), os.path.dirname(favicon_path))


def loginUser(request):
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                print(user)
                login(request, user)
                return redirect('dashboard')  # Change 'home' to your desired redirect URL
            else:
                form.add_error(None, "Email OR password is incorrect.")
    else:
        form = forms.LoginForm()
    
    context = {'form': form}
    return render(request, 'control_panel/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('index')