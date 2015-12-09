from group.models import Group

class GroupSearch:
	def search(self, query):
		groups = Group.objects.filter(
			name__icontains=query,
			parent=None
		)
		return [self.format_item(item) for item in groups]

	def format_item(self, item):
		return {
			'id': item.id,
			'name': item.name,
			'type': 'group'
		}