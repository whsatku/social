from rest_framework.response import Response
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.exceptions import NotAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from newsfeed.models import Post
from newsfeed.models import Comment
from newsfeed.serializer import GroupPostSerializer
from newsfeed.serializer import CommentSerializer
from notification.views import NotificationViewList
from models import *
from serializers import *
from django.http import Http404
from rest_framework import status
from rest_framework.renderers import JSONRenderer
import json


class MemberViewSet(ListCreateAPIView):

    serializer_class = GroupMemberSerializer

    def get_group_id(self):
        try:
            return int(self.kwargs['group_id'])
        except ValueError:
            return ValidationError('group id cannot be parsed')

    def get_queryset(self):
        this_group = Group.objects.get(id=self.get_group_id)
        return GroupMember.objects.filter(group=this_group)

    def create(self, *args, **kwargs):
        if not self.request.user.is_authenticated():
            raise NotAuthenticated
        try:
            group = Group.objects.get(id=self.get_group_id())
        except Group.DoesNotExist:
            raise NotFound('no such group')
        member, created = GroupMember.objects.get_or_create(
            group=Group.objects.get(id=self.get_group_id),
            user=User.objects.get(id=self.request.user.id),
            defaults={
                'role': 0
            }
        )

        if not created:
            raise ValidationError('request already exists')

        return Response(GroupMemberSerializer(member).data)


class PendingMemberViewSet(ListCreateAPIView):
    serializer_class = GroupMemberSerializer

    def get_queryset(self):
        this_group = Group.objects.get(id=int(self.kwargs['group_id']))
        return GroupMember.objects.filter(group=this_group, role=0)


class AcceptedMemberViewSet(ListCreateAPIView):
    serializer_class = GroupMemberSerializer

    def get_queryset(self):
        this_group = Group.objects.get(id=int(self.kwargs['group_id']))
        return GroupMember.objects.filter(group=this_group, role=1)


class GroupViewSet(APIView):
    serializer_class = GroupSerializer

    def get(self, request, id=None, format=None):
        group = Group.objects.all()
        response = self.serializer_class(group, many=True)

        return Response(response.data)

    def post(self, request, format=None):
        serializer = GroupSerializer(data=request.data)

        if serializer.is_valid():
            # serializer.user = self.request.user
            serializer.save(group=Group.objects.get(id=self.request.group.id))
            print request.data
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GroupViewDetail(APIView):
    serializer_class = GroupSerializer

    def get_group(self, group_id):
        try:
            return Group.objects.get(id=group_id)
        except Group.DoesNotExist:
            raise Http404

    def get(self, request, group_id=None, format=None):
        group_object = self.get_group(group_id)

        if request.user.is_authenticated():
            group_object.member_status = -1

            try:
                member_status = group_object.groupmember_set.filter(user=request.user).get()
                group_object.member_status = member_status.role
            except GroupMember.DoesNotExist:
                pass

        response = self.serializer_class(group_object)
        return Response(response.data)

    def post(self, request, group_id, format=None):
        serializer = GroupSerializer(data=request.data)

        if serializer.is_valid():
            # serializer.user = self.request.user
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MemberDetail(APIView):
    """This class is an API for managing member in group.



    """
    serializer_class = GroupMemberSerializer

    def get_member(self, group_id, user_id):
        """Get user from group's database.

        Args:
                request: Django Rest Framework request object
                group_id: ID of group
                format: pattern for Web APIs

        Return:

        """
        try:
            return GroupMember.objects.get(group=group_id, user=user_id)
        except GroupMember.DoesNotExist:
            raise Http404

    def delete(self, request, group_id, pk, format=None):
        """Delete user from group.

        Args:
                request: Django Rest Framework request object
                group_id: ID of group
                pk: ID of user
                format: pattern for Web APIs

        Return:

        """
        member = self.get_member(group_id, pk)
        member.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, group_id, pk, format=None):
        """Add or update member in group.

        Args:
                request: Django Rest Framework request object
                group_id: ID of group
                pk: ID of user
                format: pattern for Web APIs

        Return:

        """
        member = self.get_member(group_id, pk)
        member.role = 1
        member.save()
        return Response(status=status.HTTP_201_CREATED)

    def get(self, request, group_id, pk, format=None):
        """Sending data of member in group from server to client.

        Args:
                request: Django Rest Framework request object
                group_id: ID of group
                pk: ID of user
                format: pattern for Web APIs

        Return:

        """
        group_member_object = self.get_member(group_id, pk)
        response = self.serializer_class(group_member_object)
        return Response(response.data)

class EditInfo(APIView):
    """This class is an API for editing information in the group.



    """
    serializer_class = GroupSerializer

    def put(self, request, group_id, format=None):
        """Edit or add information in the group.

        Args:
                request: Django Rest Framework request object
                group_id: ID of group
                format: pattern for Web APIs

        Return:


        """
        try:
            group = Group.objects.get(pk=group_id)
        except Group.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = GroupSerializer(group, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GroupByCategory(APIView):
    """This class an API for query groups by its category.



    """

    serializer_class = GroupSerializer

    def get(self, request, cat, format=None):
        """Get a list of group with the same category selected.

        Args:
                request: Django Rest Framework request object.
                cat: category of groups.
                format: pattern for Web APIs.

        Return:
                List of group with same category.

        """
        try:
            cate = GroupCategory.objects.get(name=cat)
        except GroupCategory.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        groups = Group.objects.filter(category=cate.id)
        for g in groups:
            g.member_count = len(GroupMember.objects.filter(group=g))
        response = self.serializer_class(groups, many=True)
        return Response(response.data)


class AllCategory(APIView):
    """This class an API for querying list of all category in the database.



    """
    serializer_class = GroupCategorySerializer

    def get(self, request, format=None):
        """Get a list of all category.

        Args:
                request: Django Rest Framework request object.
                format: pattern for Web APIs.

        Return:
                List of all category.

        """
        category = GroupCategory.objects.all()
        response = self.serializer_class(category, many=True)
        return Response(response.data)

class GroupPostView(APIView):
    serializer_class = GroupPostSerializer
    group_model_id = 15

    def get(self, request, group_id, format=None):
        post = Post.objects.filter(target_id=group_id, target_type=self.group_model_id).order_by('-datetime')
        response = self.serializer_class(post, many=True)
        return Response(response.data)

    def post(self, request, group_id, format=None):
        serializer = GroupPostSerializer(data=request.data)
        notification = NotificationViewList()
        if serializer.is_valid():
            # if User.objects.get(id=self.request.user.id) in GroupMember.objects.filter(group_id=group_id):
                if self.request.user.is_authenticated():
                    request.data['target_type'] = 15
                    request.data['target_id'] = group_id
                    serializer.save(user=User.objects.get(id=self.request.user.id), target_id=group_id, target_type=ContentType.objects.get(id=self.group_model_id))
                    data = {}
                    data['type'] = 'group'
                    data['group_id'] = group_id
                    data['group_name'] = Group.objects.get(id=group_id).name
                    json_data = json.dumps(data)
                    notification.post(request, User.objects.filter(id__in=GroupMember.objects.values('user').filter(group_id=group_id)), ContentType.objects.get(id=13), JSONRenderer().render(serializer.data), json_data)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateGroup(APIView):

    serializer_class = GroupSerializer

    def post(self, request, format=None):

        serializer = GroupSerializer(data=request.data)
        if serializer.is_valid():
            # serializer.user = self.request.user
            this_group = serializer.save()
            GroupMember.objects.create(
                group=this_group,
                user=request.user,
                role=1
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GroupList(ListAPIView):
    """List groups that the requesting user is member of

    It could be accessed at :http:get:`/api/group`"""
    serializer_class = GroupSerializer

    def get_queryset(self):
        if not self.request.user.is_authenticated():
            raise NotAuthenticated

        return Group.objects.filter(
            groupmember__user=self.request.user,
            groupmember__role__gte=1
        )
