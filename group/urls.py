from django.conf.urls import include
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^(?P<group_id>[0-9]+)/member/$', views.MemberViewSet.as_view(), name='GroupMember'),
    url(r'^(?P<group_id>[0-9]+)/member/pending', views.PendingMemberViewSet.as_view(), name='GroupMemberPending'),
    url(r'^(?P<group_id>[0-9]+)/member/accepted', views.AcceptedMemberViewSet.as_view(), name='GroupMemberAccepted'),
    url(r'^(?P<group_id>[0-9]+)/$', views.GroupViewDetail.as_view(), name='Group'),
    url(r'^(?P<group_id>[0-9]+)/member/(?P<pk>[0-9]+)/$', views.MemberDetail.as_view(), name='MemberDetail'),
    url(r'^all/$', views.GroupViewSet.as_view(), name='LookForGroup'),
    url(r'^(?P<group_id>[0-9]+)/edit/$', views.EditInfo.as_view(), name='EditInfo'),
    url(r'^category/get/(?P<cat>[a-zA-Z]+)/$', views.GroupByCategory.as_view(), name='GroupByCategory'),
    url(r'^(?P<group_id>[0-9]+)/post$', views.GroupPostView.as_view(), name='PostDetail'),
    url(r'^(?P<group_id>[0-9]+)/post&limit=(?P<limit>\d+)$', views.GroupPostView.as_view(), name='PostDetail'),
    url(r'^(?P<group_id>[0-9]+)/post/(?P<action>\w+)/(?P<post_id>\d+)$', views.GroupPostPegination.as_view(), name='PostPegination'),
    url(r'^(?P<group_id>[0-9]+)/post/(?P<action>\w+)/(?P<post_id>\d+)&limit=(?P<limit>\d+)$', views.GroupPostPegination.as_view(), name='PostPegination'),
    url(r'^create/$', views.CreateGroup.as_view(), name='CreateGroup'),
    url(r'^$', views.GroupList.as_view(), name='GroupList'),
    url(r'^category/all/$', views.AllCategory.as_view(), name='CategoryList'),
    url(r'^(?P<group_parent_id>[0-9]+)/subgroup$', views.SubGroupViewSet.as_view(), name='SubGroupViewSet'),
    url(r'^(?P<group_id>[0-9]+)/post/(?P<post_id>\d+)/unpin$', views.PostUnpin.as_view(), name='PostUnpin'),
]
