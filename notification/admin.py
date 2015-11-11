
from django.contrib import admin
from models import Notification


class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'datetime',
                    'text', 'target_type', 'target_id',
                    'link_type', 'link_item')

admin.site.register(Notification, NotificationAdmin)
