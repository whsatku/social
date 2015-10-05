from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^(?P<group_id>[0-9]+)/member', views.MemberViewSet.as_view(), name='GroupMember'),
    url(r'^(?P<group_id>[0-9]+)/$', views.GroupViewDetail.as_view(), name='Group'),
    url(r'^(?P<user_id>[0-9]+)/delete', views.DeleteUser.as_view(), name='DeleteUser'),
]
