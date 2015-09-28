from django.contrib import admin
from models import *


class GroupAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'type', 'description', 'long_description',
        'logo', 'header', 'permisssion')

class GroupMemberAdmin(admin.ModelAdmin):
    list_display = (
        'group_id','user_id', 'role')


admin.site.register(Group, GroupAdmin)
admin.site.register(GroupMember, GroupMemberAdmin)
