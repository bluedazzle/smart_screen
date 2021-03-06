"""SmartScreen URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from smart_admin.views import *

urlpatterns = [
    url(r'^login/$', AdminLoginView.as_view()),
    url(r'^upload/$', UploadPictureView.as_view()),
    url(r'^inventories/$', InventoryListView.as_view()),
    url(r'^inventory/(?P<iid>(\w)+)/$', UpdateInventoryView.as_view()),
    url(r'^site/$', SiteInfoView.as_view()),
    url(r'^plans/$', FuelPlanListView.as_view()),
    url(r'^plan/(?P<pid>(\w)+)/$', FuelPlanView.as_view()),
    url(r'^plan/$', FuelPlanView.as_view()),
    url(r'^excel/$', ExcelUploadView.as_view()),
    url(r'^budget/$', UpdateBudgetView.as_view()),
]
