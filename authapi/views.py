from rest_framework.views import APIView
from rest_framework.response import Response

class UserViewSet(APIView):
	def get(self, request):
		if request.user.is_authenticated():
			return Response(request.user.get_username())
		else:
			return Response('', 403)