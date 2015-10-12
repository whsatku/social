from django.conf.urls import include
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^(?P<group_id>[0-9]+)/members', views.MemberViewSet.as_view(), name='GroupMember'),
    url(r'^(?P<group_id>[0-9]+)/member/pending', views.PendingMemberViewSet.as_view(), name='GroupMemberPending'),
    url(r'^(?P<group_id>[0-9]+)/member/accepted', views.AcceptedMemberViewSet.as_view(), name='GroupMemberAccepted'),
    url(r'^(?P<group_id>[0-9]+)/', views.GroupViewDetail.as_view(), name='Group'),
    url(r'^(?P<user_id>[0-9]+)/delete', views.DeleteUser.as_view(), name='DeleteUser'),
]
