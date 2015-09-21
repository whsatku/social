from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotAuthenticated

class UserViewSet(APIView):
	def get(self, request):
		if request.user.is_authenticated():
			return Response(request.user.get_username())
		else:
			raise NotAuthenticated()