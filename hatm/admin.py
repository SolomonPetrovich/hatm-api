from django.contrib import admin
from django.forms import Textarea
from django.db import models
from .models import *

class HatmAdmin(admin.ModelAdmin):
    search_fields = ("title__startswith", "description__startswith")
    list_display = ['id', 'creator_id', 'title', 'description', 'is_published', 'is_public', 'is_completed', 'deadline']
    list_filter = ['is_public', 'is_completed','is_published']
    list_editable = ['creator_id', 'title', 'description', 'is_published', 'is_public']
    list_per_page = 10

    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':40})},
    }

class JuzAdmin(admin.ModelAdmin):
    list_display = ['hatm_id', 'user_id', 'juz_number', 'status', 'type', 'deadline']
    list_filter = ['status', 'type', 'hatm_id']
    list_editable = ['status']
    list_per_page = 31


admin.site.register(Hatm, HatmAdmin)
admin.site.register(Juz, JuzAdmin)
admin.site.register(JoinRequest)