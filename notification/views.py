from django.contrib.auth.models import User
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from notification.models import Notification
from notification.serializer import NotificationSerializer


class NotificationViewList(APIView):
    serializer_class = NotificationSerializer

    def post(self, request, format=None):
        serializer = NotificationSerializer(data=request.data)

        if serializer.is_valid():

            if request.user.is_authenticated():
                serializer.save(user=User.objects.get(id=request.user.id))
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, id=None, format=None):
        notification = Notification.objects.order_by('-datetime')
        response = self.serializer_class(notification, many=True)

        return Response(response.data)
