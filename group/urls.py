from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^(?P<group_id>[0-9]+)/member', views.MemberViewSet.as_view(), name='GroupMember'),
    url(r'^(?P<group_id>[0-9]+)/group', views.GroupViewSet.as_view(), name='Group'),
]
