from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('smartcity_apps', views.smartcity_apps, name='smartcity_apps'),
    path('serverless_apps', views.serverless_apps, name='serverless_apps'),
    path('openshift_cloud', views.openshift_cloud, name='openshift_cloud'),
    path('profile_settings', views.profile_settings, name='profile_settings'),


    path('ask_gpt', views.ask_gpt, name='ask_gpt'),
    path('sample_task', views.sample_task, name='sample_task'),
    path('sample_publish', views.sample_publish, name='sample_publish'),

    path('login', views.loginUser, name ='login'),
    path('register', views.registerUser, name ='register'),
    path('logout', views.logoutUser, name ='logout'),
]