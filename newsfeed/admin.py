from django.contrib import admin
from models import Post, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'text', 'date',
                    'target_type', 'target_id', 'target_object')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'user', 'text', 'date')

admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
