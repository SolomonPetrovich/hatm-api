from django.contrib import admin
from .models import CustomUser
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'nickname', 'created_at']


admin.site.register(CustomUser, UserAdmin)