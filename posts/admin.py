from django.contrib import admin

from .models import Post, Comment, Like


# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ['author', 'content', 'created_at', 'updated_at', 'post_img']
    list_filter = ['author', 'created_at']
    search_fields = ['content']
    
    
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'post', 'parent', 'content', 'created_at', 'updated_at']
    list_filter = ['author', 'post', 'parent']
    search_fields = ['content']


class LikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'object_id', 'content_type', 'created_at']
    list_filter = ['user', 'content_type', 'object_id']
    
    
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Like, LikeAdmin)
