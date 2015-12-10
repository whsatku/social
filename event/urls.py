from django.conf.urls import include
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^create/$', views.CreateEvent.as_view(), name='CreateEvent'),
    url(r'^all/$', views.EventViewSet.as_view(), name='EventViewSet'),
    url(r'^(?P<event_id>[0-9]+)/$', views.EventInformationViewDetail.as_view(), name='Event'),
    url(r'^(?P<event_id>[0-9]+)/member/$', views.EventMemberViewSet.as_view(), name='EventMemberViewSet'),
    url(r'^(?P<event_id>[0-9]+)/member/(?P<pk>[0-9]+)/$', views.EventMemberDetail.as_view(), name='EventMemberDetail'),

]
