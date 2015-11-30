
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.exceptions import NotAuthenticated
from rest_framework.exceptions import NotFound
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from models import *
from serializers import *
from django.http import Http404
from rest_framework import status


# Create your views here.
class CreateEvent(APIView):

    serializer_class = EventSerializer

    def post(self, request, format=None):
        serializer = EventSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            this_event = serializer.save()
            EventMember.objects.create(
                event=this_event,
                user=request.user,
                role=1
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, group_id=None, format=None):

        event_object = self.get_group(group_id)

        if request.user.is_authenticated():
            event_object.member_status = -1

            try:
                member_status = event_object.eventmember_set.filter(
                    user=request.user).get()
                event_object.member_status = member_status.role
            except GroupMember.DoesNotExist:
                pass

        response = self.serializer_class(group_object)
        return Response(response.data)

    def get_group(self, event_id):

        try:
            return Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            raise Http404


class EventViewSet(APIView):

    serializer_class = EventSerializer

    def get(self, request, id=None, format=None):
        event = Event.objects.all()
        response = self.serializer_class(event, many=True)

        return Response(response.data)


class EventInformationViewDetail(APIView):

    """This class is an API for managing one event.
    """
    serializer_class = EventSerializer

    def get_event(self, event_id):
        """Get one event from the database.
        Args:
                event_id: id of the query event
        Return:
                Query event.
        """

        try:
            return Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            raise Http404

    def get(self, request, event_id=None, format=None):
        """.GET function for sending the request event to the frontend
        Args:
                request: Django Rest Framework request object
                event_id: id of the query event
                format: pattern for Web APIs

        Return:
                Query group.
        """
        event_object = self.get_event(event_id)

        if request.user.is_authenticated():
            event_object.member_status = -1

            try:
                member_status = event_object.eventmember_set.filter(user=request.user).get()
                event_object.member_status = member_status.role
            except EventMember.DoesNotExist:
                pass

        response = self.serializer_class(event_object)
        return Response(response.data)
