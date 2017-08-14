from django.conf.urls import url, include
from . import views
from .api import user_manager

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^home$', views.home, name="home"),
    url(r'^status$', views.status, name="status"),
    url(r'^loadUserData$', views.loadUserData, name="loadUserData"),
    url(r'^updateWebsites$', views.updateWebsites, name="updateWebsites"),
    url(r'^deleteWebsite$', views.deleteWebsite, name="deleteWebsite"),
    url(r'^service$', views.service, name="service"),
    url(r'^3464b$', views.xavier, name="xavier")
]
