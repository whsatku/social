from django.conf.urls import include
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^create/$', views.CreateEvent.as_view(), name='CreateEvent'),
    url(r'^all/$', views.EventViewSet.as_view(), name='EventViewSet'),
    url(r'^(?P<event_id>[0-9]+)/$', views.EventInformationViewDetail.as_view(), name='Event'),
    url(r'^(?P<event_id>[0-9]+)/member/$', views.EventMemberViewSet.as_view(), name='EventMemberViewSet'),
    url(r'^(?P<event_id>[0-9]+)/member/(?P<pk>[0-9]+)/$', views.EventMemberDetail.as_view(), name='EventMemberDetail'),
    url(r'^(?P<event_id>[0-9]+)/member/(?P<pk>[0-9]+)/(?P<role>[0-9]+)$', views.EventMemberDetail.as_view(), name='EventMemberDetail'),
    url(r'^(?P<event_id>[0-9]+)/post$', views.EventPostView.as_view(), name='PostDetail'),
    url(r'^(?P<event_id>[0-9]+)/post&limit=(?P<limit>\d+)$', views.EventPostView.as_view(), name='PostDetail'),
    url(r'^(?P<event_id>[0-9]+)/post/(?P<action>\w+)/(?P<post_id>\d+)$', views.EventPostPegination.as_view(), name='PostPegination'),
    url(r'^(?P<event_id>[0-9]+)/post/(?P<action>\w+)/(?P<post_id>\d+)&limit=(?P<limit>\d+)$', views.EventPostPegination.as_view(), name='PostPegination'),
    url(r'^(?P<event_id>[0-9]+)/post/(?P<post_id>\d+)/unpin$', views.PostUnpin.as_view(), name='PostUnpin'),

]
