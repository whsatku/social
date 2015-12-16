from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.exceptions import NotAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from django.contrib.contenttypes.models import ContentType
from models import *
from serializers import *
from newsfeed.serializer import UserSerializer
from django.http import Http404
from rest_framework import status
from friendship.models import Friend
from friendship.models import FriendshipRequest
from django.utils import timezone
from notification.views import NotificationViewList
from rest_framework.renderers import JSONRenderer
import json


class UserInformation (APIView):
    """This class is an API for getting user's user information

    Attribute:
            serializer_class: serializer for this class.

    """

    serializer_class = UserProfileSerializer

    def get_user(self, user_profile_id):
        """Get user from user profile's database.

        Args:
                user_profile_id: ID of user profile.

        Return:
                UserProfile object by ID.

        """
        try:
            return UserProfile.objects.get(user_id=user_profile_id)
        except UserProfile.DoesNotExist:
            raise Http404

    def get(self, request, user_profile_id, format=None):
        """For client to get user profile's data from server.

        Args:
                request: Django Rest Framework request object.
                user_profile_id: ID of user profile.
                format: pattern for Web APIs.

        Return:
                UserProfile object by ID.

        """
        user_profile_object = self.get_user(user_profile_id)
        response = self.serializer_class(user_profile_object)
        return Response(response.data)

    def put(self, request, user_profile_id, format=None):
        """For client to edit the userprofile

        Args:
                request: Django Rest Framework request object.
                user_profile_id: ID of user profile.
                format: pattern for Web APIs.
        Return:
                response serializer error ????
        """ 
        try:
            profile = UserProfile.objects.get(user_id=user_profile_id)
        except UserProfile.DoesNotExist:
            raise Http404

        serializer = UserProfileSerializer(profile, data=request.data)

        if serializer.is_valid():
            if self.request.user.is_authenticated():
                if 'picture' in self.request.FILES:
                    serializer.data.picture = self.request.FILES.get('picture')
                if 'cover' in self.request.FILES:
                    serializer.data.cover = self.request.FILES.get('cover')
                serializer.save()
                profile.user.first_name = profile.firstname 
                profile.user.last_name = profile.lastname
                profile.user.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfilePicture (APIView):
    """This class is an API for updating user's user profile picture

    Attribute:
            serializer_class: serializer for this class.

    """
    serializer_class = UserProfilePictureSerializer
    def get(self, request, user_profile_id, format=None):
        """For client to get user profile picture's data from server.

        Args:
                request: Django Rest Framework request object.
                user_profile_id: ID of user profile.
                format: pattern for Web APIs.

        Return:
                UserProfile object by ID.

        """
        userprofile = UserProfile.objects.get(user_id=user_profile_id)
        response = self.serializer_class(userprofile)
        return Response(response.data.get('picture'))

    def put(self, request, user_profile_id, format=None):
        """For client to updating UserProfilePicture

        Args:
                request: Django Rest Framework request object.
                user_profile_id: ID of user profile.
                format: pattern for Web APIs.
        Return:
                response serializer error
        """ 
        try:
            profile = UserProfile.objects.get(user_id=user_profile_id)
        except UserProfile.DoesNotExist:
            raise Http404

        serializer = UserProfilePictureSerializer(profile, data=request.data)

        if serializer.is_valid():
            if self.request.user.is_authenticated():
                if 'picture' in self.request.FILES:
                    serializer.data.picture = self.request.FILES.get('picture')
                serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserCover (APIView):
    """This class is an API for updating user's cover picture

    Attribute:
            serializer_class: serializer for this class.

    """
    serializer_class = UserCoverSerializer
    def get(self, request, user_profile_id, format=None):
        """For client to get user cover's data from server.

        Args:
                request: Django Rest Framework request object.
                user_profile_id: ID of user profile.
                format: pattern for Web APIs.

        Return:
                UserProfile object by ID.

        """
        usercover = UserProfile.objects.get(user_id=user_profile_id)
        response = self.serializer_class(usercover)
        return Response(response.data.get('cover'))

    def put(self, request, user_profile_id, format=None):
        """For client to updating UserCover

        Args:
                request: Django Rest Framework request object.
                user_profile_id: ID of user profile.
                format: pattern for Web APIs.
        Return:
                response serializer error
        """ 
        try:
            profile = UserProfile.objects.get(user_id=user_profile_id)
        except UserProfile.DoesNotExist:
            raise Http404

        serializer = UserCoverSerializer(profile, data=request.data)

        if serializer.is_valid():
            if self.request.user.is_authenticated():
                if 'cover' in self.request.FILES:
                    serializer.data.cover = self.request.FILES.get('cover')
                serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FriendshipDetail(APIView):

    def get_user(self, user_profile_id):
        """Get user from user profile's database.

        Args:
                user_profile_id: ID of user profile.

        Return:
                UserProfile object by ID.

        """
        try:
            return User.objects.get(id=user_profile_id)
        except UserProfile.DoesNotExist:
            raise Http404

    # def get(self, request, user_profile_id, format=None):
    #     user_profile_object = self.get_user(user_profile_id)
    #     response = self.serializer_class(user_profile_object)
    #     return Response(response.data)

    def post(self, request, other_user_id, format=None):
        user = request.user
        other_user = self.get_user(other_user_id)
        new_relationship = Friend.objects.add_friend(from_user=user, to_user=other_user)
        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, other_user_id, format=None):
        try:
            user = request.user
            other_user = self.get_user(other_user_id)
            Friend.objects.remove_friend(from_user=other_user, to_user=user)
        except Exception as inst:
            print type(inst)     # the exception instance
            print inst           # __str__ allows args to be printed directly
            raise Http404
        return Respose(status=status.HTTP_200_OK)


class FriendshipPendingViewSet(APIView):
    serializer_class = FriendShipSerializer

    def get(self, request, format=None):
        friend_pending = Friend.objects.unrejected_requests(user=self.request.user)
        response = self.serializer_class(friend_pending, many=True)
        return Response(response.data)


class FriendshipViewSet(APIView):
    serializer_class = UserProfileSerializer

    def get(self, request, format=None):
        friends = Friend.objects.friends(self.request.user)
        friend_list = UserProfile.objects.filter(user__in=friends)

        response = self.serializer_class(friend_list, many=True)
        return Response(response.data)

class FriendshipOtherUserViewSet(APIView):
    serializer_class = UserProfileSerializer

    def get_user(self, user_profile_id):
        """Get user from user profile's database.

        Args:
                user_profile_id: ID of user profile.

        Return:
                UserProfile object by ID.

        """
        try:
            return User.objects.get(id=user_profile_id)
        except UserProfile.DoesNotExist:
            raise Http404

    def get(self, request,other_user_id, format=None):
        other_user = self.get_user(other_user_id)
        friends = Friend.objects.friends(other_user)
        friend_list = UserProfile.objects.filter(user__in = friends)
        response = self.serializer_class(friend_list, many=True)
        return Response(response.data)


class FriendshipforInviteViewSet(APIView):
    serializer_class = UserSerializer

    def get(self, request, format=None):
        friends = Friend.objects.friends(self.request.user)

        response = self.serializer_class(friends, many=True)
        return Response(response.data)


class IsFriendDetail(APIView):
    serializer_class = FriendShipSerializer

    def get_user(self, user_profile_id):
        """Get user from user profile's database.

        Args:
                user_profile_id: ID of user profile.

        Return:
                UserProfile object by ID.

        """
        try:
            return User.objects.get(id=user_profile_id)
        except UserProfile.DoesNotExist:
            raise Http404

    def get(self, request, other_user_id, format=None):
        friend_status = 0
        other_user = self.get_user(other_user_id)
        try:
            if FriendshipRequest.objects.get(from_user=other_user, to_user=request.user):
                friend_status = 2
        except FriendshipRequest.DoesNotExist as inst1:
            try:
                if FriendshipRequest.objects.get(from_user=request.user, to_user=other_user):
                    friend_status = 1
            except FriendshipRequest.DoesNotExist as inst2:
                if Friend.objects.are_friends(request.user, other_user):
                    friend_status = 3
                return Response(friend_status)
        except Exception as instance:
            raise Http404
        return Response(friend_status)

    def put(self, request, other_user_id, format=None):
        notification = NotificationViewList()
        try:
            friend = FriendshipRequest.objects.get(from_user=self.get_user(other_user_id), to_user=request.user)
            friend.accept()
        except Exception as inst:
            print type(inst)     # the exception instance
            print inst           # __str__ allows args to be printed directly
            raise Http404
        data_json = {}
        data_json['target_id'] = other_user_id
        data_json['target_type'] = ContentType.objects.get(model='user').id
        data_json['text'] = 'accepted your friend request'
        notification.add(self.request.user, data_json, User.objects.filter(id=other_user_id), ContentType.objects.get(model='friendshiprequest'), json.dumps({}), json.dumps({}))

        return Response(Friend.objects.are_friends(request.user, self.get_user(other_user_id)))

    def delete(self, request, other_user_id, format=None):
        try:
            friend = FriendshipRequest.objects.get(from_user=self.get_user(other_user_id), to_user=request.user)
            friend.cancel()
        except Exception as inst:
            print type(inst)     # the exception instance
            print inst           # __str__ allows args to be printed directly
            raise Http404
        return Response(Friend.objects.are_friends(request.user, self.get_user(other_user_id)))
