from django.shortcuts import render
from rest_framework.views import APIView

# Create your views here.
class EventViewSet(APIView):

	def post(self, request, format=None):

        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            # serializer.user = self.request.user
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
            group_object.member_status = -1

            try:
                member_status = group_object.groupmember_set.filter(user=request.user).get()
                group_object.member_status = member_status.role
            except GroupMember.DoesNotExist:
                pass

        response = self.serializer_class(group_object)
        return Response(response.data)

    def get_group(self, group_id):

        try:
            return Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            raise Http404
