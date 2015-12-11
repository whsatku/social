
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

    def get(self, request, event_id=None, format=None):

        event_object = self.get_event(event_id)

        if request.user.is_authenticated():
            event_object.member_status = -1

            try:
                member_status = event_object.eventmember_set.filter(
                    user=request.user).get()
                event_object.member_status = member_status.role
            except eventMember.DoesNotExist:
                pass

        response = self.serializer_class(event_object)
        return Response(response.data)

    def get_event(self, event_id):

        try:
            return Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            raise Http404


class EventViewSet(APIView):

    serializer_class = EventSerializer

    def get(self, request, id=None, format=None):
        event = Event.objects.all()
        for e in event:
            e.member_count = len(EventMember.objects.filter(event=e))
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
                Query event.
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


class EventMemberViewSet(ListCreateAPIView):

    serializer_class = EventMemberSerializer

    def get_event_id(self):
        try:
            return int(self.kwargs['event_id'])
        except ValueError:
            return ValidationError('event id cannot be parsed')

    def get_queryset(self):
        this_event = Event.objects.get(id=self.get_event_id)
        return EventMember.objects.filter(event=this_event)


class EventMemberDetail(APIView):
    """This class is an API for managing member in event.
    """
    serializer_class = EventMemberSerializer

    def get_member(self, event_id, user_id):
        """Get user from event's database.
        Args:
                event_id: ID of event
                user_id: ID of user
        Return:
        """
        try:
            return EventMember.objects.get(event=event_id, user=user_id)
        except EventMember.DoesNotExist:
            return None

    def delete(self, request, event_id, pk, format=None):
        """Delete user from event.
        Args:
                request: Django Rest Framework request object
                event_id: ID of event
                pk: ID of user
                format: pattern for Web APIs
        Return:
        """
        member = self.get_member(event_id, pk)
        member.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, event_id, pk, format=None):
        """Add or update member in event.
        Args1:
                request: Django Rest Framework request object
                event_id: ID of event
                pk: ID of user
                format: pattern for Web APIs
        Return:
        """
        member = self.get_member(event_id, pk)

        if member is None:
            member = EventMember.objects.create(
                event=Event.objects.get(id=event_id),
                user=User.objects.get(id=pk),
                role=0
            )

        member.save()
        return Response(status=status.HTTP_201_CREATED)

    def get(self, request, event_id, pk, format=None):
        """Sending data of member in event from server to client.
        Args:
                request: Django Rest Framework request object
                event_id: ID of event
                pk: ID of user
                format: pattern for Web APIs
        Return:
        """
        event_member_object = self.get_member(event_id, pk)
        response = self.serializer_class(event_member_object)
        return Response(response.data)
