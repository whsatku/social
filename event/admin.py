from django.contrib import admin
from models import *

# Register your models here.


class EventAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'start_date', 'end_date', 'description')


class EventMemberAdmin(admin.ModelAdmin):
    list_display = (
        'event', 'user', 'role')

admin.site.register(Event, EventAdmin)
admin.site.register(EventMember, EventMemberAdmin)
