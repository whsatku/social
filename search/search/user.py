from django.contrib.auth.models import User
from django.db.models import Q

class UserSearch:
	def search(self, query):
		users = User.objects.filter(
			Q(first_name__icontains=query) | 
			Q(last_name__icontains=query) |
			Q(username__icontains=query)
		)
		return [self.format_item(item) for item in users]

	def format_item(self, item):
		if item.first_name:
			name = '{0} {1}'.format(item.first_name, item.last_name)
		else:
			name = item.username
		
		return {
			'id': item.id,
			'name': name,
			'type': 'user'
		}