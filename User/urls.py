from django.conf.urls import include
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^(?P<user_profile_id>[0-9]+)/userInfo/$', views.UserInformation.as_view(), name='UserInformation'),
    url(r'^(?P<user_profile_id>[0-9]+)/userPicture/$', views.UserProfilePicture.as_view(), name='UserProfile'),
    url(r'^(?P<user_profile_id>[0-9]+)/userCover/$', views.UserCover.as_view(), name='UserCover'),
    url(r'^friend/(?P<other_user_id>[0-9]+)$', views.FriendshipDetail.as_view(), name='AddFriend'),
    url(r'^friend/pending/$', views.FriendshipPendingViewSet.as_view(), name="PendingFriends"),
    url(r'^friend/isFriend/(?P<other_user_id>[0-9]+)/$', views.IsFriendDetail.as_view() , name="isFriend"),
    url(r'^friends/$', views.FriendshipViewSet.as_view(), name="friendFriends"),
    url(r'^friends/(?P<other_user_id>[0-9]+)/$', views.FriendshipOtherUserViewSet.as_view(), name="friendFriends"),
    url(r'^friends/invite/$', views.FriendshipforInviteViewSet.as_view(), name="for invite friends"),

]
