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

from super_admin import views, apis

urlpatterns = [
    url(r'^api/sites/$', apis.SiteListView.as_view()),
    url(r'^api/site/overview/$', apis.SiteOverviewView.as_view()),
    url(r'^api/tasks/$', apis.TaskListView.as_view()),
    url(r'^api/task/$', apis.TaskView.as_view()),

    url(r'^view/sites/$', views.SiteListView.as_view()),
    url(r'^view/tasks/$', views.TaskListView.as_view()),
]
