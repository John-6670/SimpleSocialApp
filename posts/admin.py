from django.contrib import admin

from .models import Post, Comment, Image


# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ['content', 'author', 'is_published']
    list_filter = ['author', 'is_published']
    search_fields = ['content']
    ordering = ['-created_at']


class CommentAdmin(admin.ModelAdmin):
    list_display = ['content', 'author', 'is_published']
    list_filter = ['author', 'is_published']
    search_fields = ['content']
    ordering = ['-created_at']


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Image)
