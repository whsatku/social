from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView
from rest_framework.exceptions import ValidationError, NotAuthenticated, NotFound
from models import *
from serializers import *


class MemberViewSet(ListCreateAPIView):

    serializer_class = GroupMemberSerializer

    def get_group_id(self):
        try:
            return int(self.kwargs['group_id'])
        except ValueError:
            return ValidationError('group id cannot be parsed')

    def get_queryset(self):
        return GroupMember.objects.filter(group_id=self.get_group_id())

    def create(self, *args, **kwargs):
        if not self.request.user.is_authenticated():
            raise NotAuthenticated
        try:
            group = Group.objects.get(id=self.get_group_id())
        except Group.DoesNotExist:
            raise NotFound('no such group')
        
        member, created = GroupMember.objects.get_or_create(
            group_id = Group.objects.get(id = self.get_group_id),
            user_id = User.objects.get( id = self.request.user.id),
            defaults = {
                'role': 0
            }
        )

        if not created:
            raise ValidationError('request already exists')

        return Response(GroupMemberSerializer(member).data)