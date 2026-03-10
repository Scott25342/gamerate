from django.contrib import admin
from django.utils.html import format_html
from .models import VideoGame

class VideoGameAdmin(admin.ModelAdmin):
    list_display = ('title', 'developer', 'release_year', 'thumbnail')

    def thumbnail(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" />', obj.image)
        return ""

admin.site.register(VideoGame, VideoGameAdmin)