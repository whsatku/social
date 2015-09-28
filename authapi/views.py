from rest_framework.views import APIView
from rest_framework.response import Response

class UserViewSet(APIView):
	"""Validate current user session

	This API is used to check whether the current user is logged in
	and to retrieve information about the user.

	It could be accessed at /api/auth/check

	"""
	def get(self, request):
		"""Get logged user information

		Args:
			request: Django Rest Framework request object

		Return:
			Current logged username as string, or 403
		"""
		if request.user.is_authenticated():
			return Response(request.user.get_username())
		else:
			return Response('', 403)