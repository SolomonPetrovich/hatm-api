from django.contrib import admin
from .models import Hatm, Juz

class HatmAdmin(admin.ModelAdmin):
    search_fields = ("title__startswith", "description__startswith")
    list_display = ['creator_id', 'title', 'description', 'isPublic', 'isPublished', 'isCompleted', 'deadline']
    list_filter = ['isPublic', 'isCompleted','isPublished', 'deadline']
    list_editable = ['title', 'description']
    list_per_page = 10

admin.site.register(Hatm, HatmAdmin)
admin.site.register(Juz)