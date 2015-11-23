from django.conf.urls import include
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^create/$', views.EventViewDetail.as_view(), name='EventViewDetail'),
    url(r'^all/$', views.EventViewSet.as_view(), name='EventViewSet'),
]
