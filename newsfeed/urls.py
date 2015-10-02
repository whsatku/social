from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^post', views.PostView.as_view(), name='auth_check'),
]
