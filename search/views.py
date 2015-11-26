from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from search import Search

class SearchAPI(APIView):
	def get(self, request):
		query = request.query_params.get('q', None)

		if not query:
			raise ValidationError('No query given')

		result = Search().search(query)

		return Response(result)