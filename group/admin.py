from django.contrib import admin
from models import *


class GroupAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'type', 'description', 'long_description',
        'logo', 'header', 'permisssion')

class GroupMemberAdmin(admin.ModelAdmin):
    list_display = (
        'group','user', 'role')


admin.site.register(Group, GroupAdmin)
admin.site.register(GroupMember, GroupMemberAdmin)
