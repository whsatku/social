from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.SearchAPI.as_view()),
]
