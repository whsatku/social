from django.contrib import admin

# Register your models here.
class EventAdmin(admin.ModelAdmin):
	list_display = (
        'name', 'start_date', 'end_date', 'description')

class EventMemberAdmin(admin.ModelAdmin):
	list_display = (
        'event', 'user', 'role')
