from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('smartcity_apps', views.smartcity_apps, name='smartcity_apps'),
    # path('serverless_apps', views.serverless_apps, name='serverless_apps'),
    path('openshift_cloud', views.openshift_cloud, name='openshift_cloud'),
    path('profile_settings', views.profile_settings, name='profile_settings'),

    path('emergency_services', views.EmergencyServiceListView.as_view(), name='emergency_services'),
    path('emergency_vehicles', views.EmergencyVehicleListView.as_view(), name='emergency_vehicles'),
    path('emergency_calls', views.EmergencyCallListView.as_view(), name='emergency_calls'),
    path('plan_route', views.create_route_planning, name='plan_route'),
    path('alert_logs', views.alert_logs, name='alert_logs'),
    path('generate_advisory', views.generate_advisory, name='generate_advisory'),

    path('serverless_apps', views.ServerlessAppListView.as_view(), name='serverless_apps'),
    path('serverless_app_create', views.ServerlessAppCreateView.as_view(), name='serverless_app_create'),
    path('serverless_app_edit/<int:pk>/', views.ServerlessAppEditView.as_view(), name='serverless_app_edit'),

    path('sample_task', views.sample_task, name='sample_task'),
    path('sample_publish', views.sample_publish, name='sample_publish'),

    path('login', views.loginUser, name ='login'),
    path('register', views.registerUser, name ='register'),
    path('logout', views.logoutUser, name ='logout'),
]