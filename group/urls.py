from django.conf.urls import include
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^(?P<group_id>[0-9]+)/member/$', views.MemberViewSet.as_view(), name='GroupMember'),
    url(r'^(?P<group_id>[0-9]+)/member/pending', views.PendingMemberViewSet.as_view(), name='GroupMemberPending'),
    url(r'^(?P<group_id>[0-9]+)/member/accepted', views.AcceptedMemberViewSet.as_view(), name='GroupMemberAccepted'),
    url(r'^(?P<group_id>[0-9]+)/$', views.GroupViewDetail.as_view(), name='Group'),
    url(r'^(?P<group_id>[0-9]+)/member/(?P<pk>[0-9]+)/$', views.MemberDetail.as_view(), name='MemberDetail'),
    url(r'^(?P<group_id>[0-9]+)/edit/$', views.EditInfo.as_view(), name='EditInfo'),
]
