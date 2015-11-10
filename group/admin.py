from django.contrib import admin
from models import *


class GroupAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'type', 'category', 'description',
        'short_description', 'activities', 'logo',
        'header', 'permisssion')


class GroupMemberAdmin(admin.ModelAdmin):
    list_display = (
        'group', 'user', 'role')


class GroupCategoryAdmin(admin.ModelAdmin):
	list_display = (
		'name',)


admin.site.register(GroupCategory, GroupCategoryAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(GroupMember, GroupMemberAdmin)
