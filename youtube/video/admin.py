from django.contrib import admin
from video.models import Thumbnail, Video

admin.site.site_header = 'Youtube Data Admin'

class ThumbnailInLine(admin.TabularInline):
    model = Thumbnail
    extra = 0

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

class VideoAdmin(admin.ModelAdmin):
    search_fields = ('video_id', 'title', 'description', 'channel_title')
    list_display = ('id', 'video_id', 'title', 'channel_title', 'published_at')
    list_filter = ('channel_title', 'live_brodcast_content')

    inlines = [ThumbnailInLine]

admin.site.register(Thumbnail)
admin.site.register(Video, VideoAdmin)
