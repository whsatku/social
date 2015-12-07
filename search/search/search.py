from .group_search import GroupSearch
from .user import UserSearch

strategy = [
	GroupSearch,
	UserSearch
]

class Search:
	limit_per_module = 2
	
	def search(self, query):
		result = []
		for item in strategy:
			result += list(item().search(query)[:self.limit_per_module])

		return result