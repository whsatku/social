from django.conf.urls import include
from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^create/$', views.EventViewSet.as_view(), name='EventViewSet'),
]