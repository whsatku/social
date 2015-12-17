from django.contrib.auth.models import User
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from notification.models import Notification
from notification.models import UserNotification
from django.contrib.contenttypes.models import ContentType
from notification.serializer import NotificationSerializer
from notification.serializer import GetNotificationSerializer
from notification.serializer import UpdateNotificationSerializer


class NotificationViewList(APIView):
    """This class is an API for create and get all notification.
    """
    serializer_class = NotificationSerializer

    def add(self, user, data, receiver_set, type,
            link_item, reference_detail, format=None):
        """Create and save notification to database.
        Args:
                user: user who create notification.
                data: Json information of target of post
                receiver_set: set of receiver who will receive
                              this notification.
                type: type of action that create this notification.
                link_item: information of action that create this notification.
                reference_detail: information of the post target object
                format: pattern for Web APIs.
        Return:

        """
        receiver_set = receiver_set.exclude(id=user.id)
        notification = Notification.objects.create(
            user=User.objects.get(id=user.id),
            target_id=data['target_id'],
            target_type=ContentType.objects.get(id=data['target_type']),
            text=data['text'],
            link_type=type,
            link_item=link_item,
            reference_detail=reference_detail
        )
        notification.save()
        for i in receiver_set:
            UserNotification(
                notification=notification,
                receiver=i
            ).save()
        return Response(status=status.HTTP_201_CREATED)

    def get(self, request, format=None):
        """Get all of notification in database.
        Args:
                request: Django Rest Framework request object.
                format: pattern for Web APIs.
        Return:
            list of all notification in database.
        """
        notification = Notification.objects.order_by('-datetime')
        response = self.serializer_class(notification, many=True)

        return Response(response.data)


class NotificationView(APIView):
    """This class is an API for get specific notification.
    """
    serializer_class = GetNotificationSerializer

    def get(self, request):
        """Get notification of specific user.
        Args:
                request: Django Rest Framework request object.
                format: pattern for Web APIs.
        Return:
            list of notification of that user.
        """
        noti = Notification.objects.filter(
            receiver=self.request.user).order_by('-datetime')
        for i in noti:
            if self.request.user in i.readed.all():
                i.read = True
            else:
                i.read = False
        response = self.serializer_class(noti, many=True)
        return Response(response.data)


class UpdateNotification(APIView):
    """This class is an API for update readed notification.
    """
    serializer_class = UpdateNotificationSerializer

    def get_object(self, noti_id):
        """Get notification object by id.
        Args:
                noti_id: id of notification.
        Return:
            notification object.
        """
        try:
            return Notification.objects.get(id=noti_id)
        except Notification.DoesNotExist:
            raise Http404

    def update_read(self, noti_id, format=None):
        """Update notification to readed by id.
        Args:
                noti_if: id of notification.
                format: pattern for Web APIs.
        Return:

        """
        noti = self.get_object(noti_id)
        noti.readed.add(User.objects.get(id=self.request.user.id))
        noti.save()

    def get(self, request, noti_id, format=None):
        """Get notification in database and mark as readed.
        Args:
                request: Django Rest Framework request object.
                noti_id: id of notification.
                format: pattern for Web APIs.
        Return:
            updated notificaton.
        """
        self.update_read(noti_id)
        notification = Notification.objects.get(id=noti_id)
        response = self.serializer_class(notification)
        return Response(response.data)
