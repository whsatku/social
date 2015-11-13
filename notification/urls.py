from django.conf.urls import url
from django.conf.urls import include
from . import views


urlpatterns = [
    url(r'^all/$', views.NotificationViewList.as_view()),
    url(r'^get/$', views.NotificationView.as_view()),
    url(r'^read/(?P<noti_id>\d+)/$', views.UpdateNotification.as_view()),
]
