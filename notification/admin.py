from django.contrib import admin
from models import Notification


class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'datetime',
                    'message', 'target_type', 'target_id')

admin.site.register(Notification, NotificationAdmin)
