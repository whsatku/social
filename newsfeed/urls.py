from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^post/$', views.PostViewList.as_view()),
    url(r'^post/(?P<id>\d+)/$', views.PostViewDetail.as_view()),
    url(r'^comment/$', views.CommentViewList.as_view()),
    url(r'^comment/(?P<id>\d+)/$', views.CommentViewDetail.as_view()),
]
