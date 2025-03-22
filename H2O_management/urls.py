"""
URL configuration for H2O_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from H2O_usage import views

urlpatterns = [
    path( 'admin/', admin.site.urls ),
    path( '', views.signup_page_view, name = 'signup_page' ),
    path( 'signup', views.signup_view, name = 'signup' ),
    path( 'signin', views.signin_view, name = 'signin' ),
    path( 'record-usage', views.record_usage_view, name = 'record_usage' ),
    path( 'filter-admin-usage', views.filter_admin_usage_view, name = 'filter_admin_usage' ),
    path( 'filter-client-usage', views.filter_client_usage_view, name = 'filter_client_usage' ),
    path( 'delete-admin', views.delete_admin_view, name = 'delete_admin' ),
    path( 'delete-client', views.delete_client_view, name = 'delete_client' ),
    path( 'get-clients/', views.get_clients_view, name = 'get_clients' ),
    # path( 'get-prediction', views.predict_usage, name = 'predict_usage' )
]