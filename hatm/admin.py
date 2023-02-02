from django.contrib import admin
from django.forms import Textarea
from django.db import models
from .models import Hatm, Juz

class HatmAdmin(admin.ModelAdmin):
    search_fields = ("title__startswith", "description__startswith")
    list_display = ['creator_id', 'title', 'description', 'isPublished', 'isPublic', 'isCompleted', 'deadline']
    list_filter = ['isPublic', 'isCompleted','isPublished', 'deadline']
    list_editable = ['title', 'description', 'isPublished']
    list_per_page = 10

    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':40})},
    }

class JusAdmin(admin.ModelAdmin):
    list_display = ['hatm_id', 'user_id', 'juz_number', 'status', 'type']
    list_filter = ['status', 'type', 'hatm_id']
    list_editable = ['status']
    list_per_page = 31


admin.site.register(Hatm, HatmAdmin)
admin.site.register(Juz, JusAdmin)