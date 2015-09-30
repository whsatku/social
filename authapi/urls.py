from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^check', views.UserViewSet.as_view(), name='auth_check'),
    url(r'^login', views.LoginViewSet.as_view(), name='auth_login'),
]
