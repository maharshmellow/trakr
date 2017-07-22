from django.conf.urls import url, include
from . import views
from .api import user_manager

urlpatterns = [
    url(r'^$', views.index, name="index"), 
    url(r'^home$', views.home, name="home"),
    url(r'^status$', views.status, name="status"),
    # url(r'^account$', views.account, name="account"),
    url(r'^logout$', views.logout, name="logout"),


    
    url(r'^loadUserData$', views.loadUserData, name="loadUserData")

    
    # url(r'^test$', user_manager.login_user, name="login_user")
]
