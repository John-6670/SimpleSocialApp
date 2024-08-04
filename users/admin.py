from django.contrib import admin

from .models import Profile, ProfileImage


# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_verified']


admin.site.register(Profile, ProfileAdmin)
admin.site.register(ProfileImage)
