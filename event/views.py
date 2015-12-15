
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.exceptions import NotAuthenticated
from rest_framework.exceptions import NotFound
from django.contrib.contenttypes.models import ContentType
from newsfeed.serializer import EventPostSerializer
from notification.views import NotificationViewList
from django.contrib.auth.models import User
from newsfeed.models import Post
from models import *
from serializers import *
from django.http import Http404
from rest_framework import status
from rest_framework.renderers import JSONRenderer
import json


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

    def put(self, request, event_id, pk, role=0, format=None):
        """Add or update member in event.
        Args1:
                request: Django Rest Framework request object
                event_id: ID of event
                pk: ID of user
                format: pattern for Web APIs
        Return:
        """
        notification = NotificationViewList()
        member = self.get_member(event_id, pk)

        if member is None:
            member = EventMember.objects.create(
                event=Event.objects.get(id=event_id),
                user=User.objects.get(id=pk),
                role=role
            )
            member.role = role
            member.save()
            data_json = {}
            data_json['target_id'] = event_id
            data_json['target_type'] = ContentType.objects.get(model='event').id
            data_json['text'] = 'invited you to an event'
            data = {}
            data['type'] = 'event'
            data['event_id'] = event_id
            data['event_name'] = Event.objects.get(id=event_id).name
            json_data = json.dumps(data)
            notification.add(request.user, data_json, User.objects.filter(id=pk), ContentType.objects.get(model='eventmember'), json.dumps({}), json_data)
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


class EventPostView(APIView):
    """This class an API for managing group post.

    """
    serializer_class = EventPostSerializer

    def get(self, request, event_id, limit=20, format=None):
        """Get a post from database.
        Args:
                request: Django Rest Framework request object.
                event_id: event id of querying post.
                format: pattern for Web APIs.
        Return:
                post from querying event.
        """
        post = Post.objects.filter(target_id=event_id, target_type=ContentType.objects.get(model='event')).order_by('-pinned', '-datetime')[:limit]
        response = self.serializer_class(post, many=True)
        return Response(response.data)

    def post(self, request, event_id, format=None):
        """Create new post to the system.
        Args:
                request: Django Rest Framework request object.
                event_id: event id that we going to post to.
                format: pattern for Web APIs.
        Return:

        """
        serializer = EventPostSerializer(data=request.data)
        notification = NotificationViewList()
        if serializer.is_valid():
            # if self.request.user.id in EventMember.objects.filter(event_id=event_id).values_list('user_id', flat=True):
                if self.request.user.is_authenticated():
                    request.data['target_type'] = ContentType.objects.get(model='event').id
                    request.data['target_id'] = event_id
                    serializer.save(user=User.objects.get(id=self.request.user.id), target_id=event_id, target_type=ContentType.objects.get(model='event'))
                    data = {}
                    data['type'] = 'event'
                    data['event_id'] = event_id
                    data['event_name'] = Event.objects.get(id=event_id).name
                    json_data = json.dumps(data)
                    notification.add(request.user, request.data, User.objects.filter(id__in=EventMember.objects.values('user').filter(id=event_id),role=1,2), ContentType.objects.get(model='post'), JSONRenderer().render(serializer.data), json_data)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventPostPegination(APIView):

    serializer_class = EventPostSerializer
    event_model_id = ContentType.objects.get(model='event').id

    def get(self, request, event_id, action, post_id, limit=20, format=None):

        if action == 'more':
            post = Post.objects.filter(target_id=event_id, target_type=self.event_model_id).filter(id__lt=post_id).order_by('-datetime')[:limit]
        if action == 'new':
            post = Post.objects.filter(target_id=event_id, target_type=self.event_model_id).filter(id__gt=post_id).order_by('-datetime')
        response = self.serializer_class(post, many=True)
        return Response(response.data)


class PostUnpin(APIView):
    serializer_class = EventPostSerializer

    def post(self, request, event_id, post_id):
        post = Post.objects.get(id=post_id)
        if post.target_id != int(event_id):
            raise Http404

        post.pinned = False
        post.save()

        return Response(self.serializer_class(post).data)