from django.contrib import admin

from .models import Profile, Follow


# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'birth_date', 'bio']
    list_filter = ['birth_date']
    search_fields = ['bio']


class FollowAdmin(admin.ModelAdmin):
    list_display = ['follower', 'following', 'created_at']
    list_filter = ['follower', 'following']


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Follow, FollowAdmin)
