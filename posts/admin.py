from django.contrib import admin

from .models import Post, Comment


# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ['author', 'content', 'status']
    list_filter = ['author']
    search_fields = ['content']
    ordering = ['-created_at']


class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'content', 'status', 'post']
    list_filter = ['author', 'post']
    search_fields = ['content']


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
