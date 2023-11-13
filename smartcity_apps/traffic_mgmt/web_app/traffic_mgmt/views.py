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


def index(request):
    context = {'serverless_apps': models.ServerlessApp.objects.all()}
    return render(request, 'traffic_mgmt/index.html', context)


@login_required
def dashboard(request):
    context = {}
    return render(request, 'traffic_mgmt/dashboard.html', context)


@login_required
def alert_logs(request):
    context = {}
    return render(request, 'traffic_mgmt/alert_logs.html', context)


@login_required
def generate_advisory(request):
    context = {}
    if request.method == 'POST':
        messages.success(request, f"Advisory sent to citizens in this <strong>{request.POST.get('traffic_area')}</strong> area for <strong>{request.POST.get('transport_type')}</strong>.")
        return redirect('generate_advisory')
    
    return render(request, 'traffic_mgmt/generate_advisory.html', context)


class EmergencyServiceListView(ListView):
    model = models.EmergencyService
    template_name = 'traffic_mgmt/emergency_service_list.html'
    context_object_name = 'emergency_services'


class EmergencyVehicleListView(ListView):
    model = models.EmergencyVehicle
    template_name = 'traffic_mgmt/emergency_vehicle_list.html'
    context_object_name = 'emergency_vehicles'


class EmergencyCallListView(ListView):
    ordering = ['-id']
    model = models.EmergencyCall
    template_name = 'traffic_mgmt/emergency_call_list.html'
    context_object_name = 'emergency_calls'


def create_route_planning(request):
    if request.method == 'POST':
        form = forms.RoutePlanningForm(request.POST)
        if form.is_valid():
            emergency_call = form.save()
            emergency_call.assigned_vehicle = random.choice(models.EmergencyVehicle.objects.filter(service=emergency_call.emergency_service))
            emergency_call.status = "In Progress"
            emergency_call.save()
            # TODO: send alerts to user and vehicle operator
            messages.success(request, 'Vehicle assigned, route planned and notification sent to user.')
            return redirect('emergency_calls')
    else:
        form = forms.RoutePlanningForm()
    
    return render(request, 'traffic_mgmt/create_route_planning.html', {'form': form})


class ServerlessAppListView(ListView):
    model = models.ServerlessApp
    template_name = 'traffic_mgmt/serverlessapp_list.html'
    context_object_name = 'apps'

class ServerlessAppCreateView(CreateView):
    model = models.ServerlessApp
    form_class = forms.ServerlessAppForm
    template_name = 'traffic_mgmt/serverlessapp_form.html'
    success_url = '/serverless_apps'

class ServerlessAppEditView(UpdateView):
    model = models.ServerlessApp
    form_class = forms.ServerlessAppForm
    template_name = 'traffic_mgmt/serverlessapp_form.html'
    success_url = '/serverless_apps'


@login_required
def sample_task(request):
    tasks.sample_task.delay(2, 5)
    return HttpResponse("Task Sent")

@login_required
def sample_publish(request):
    rabbitmq_producer.publish('sample_publish', {'msg': 'msg from traffic_mgmt'})
    return HttpResponse("Published")


@login_required
def smartcity_apps(request):
    context = {}
    return render(request, 'traffic_mgmt/smartcity_apps.html', context)


@login_required
def profile_settings(request):
    context = {}
    return render(request, 'traffic_mgmt/profile_settings.html', context)

# @login_required
# def serverless_apps(request):
#     context = {}
#     return render(request, 'traffic_mgmt/serverless_apps.html', context)


@login_required
def openshift_cloud(request):
    context = {}
    return render(request, 'traffic_mgmt/openshift_cloud.html', context)


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
    return render(request, 'traffic_mgmt/register.html', context)


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
    return render(request, 'traffic_mgmt/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('index')