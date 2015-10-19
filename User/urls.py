from django.conf.urls import include
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^(?P<user_profile_id>[0-9]+)/userInfo/$', views.UserInformation.as_view(), name='UserInformation'),

]
