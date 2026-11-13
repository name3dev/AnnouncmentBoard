from django.contrib import admin

# Register your models here.

from .models import (
    Announcement,
    AnnouncementSubscription,
    SavedAnnouncement
)


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'user',
        'category',
        'price',
        'is_active',
        'created_at',
    )

    list_filter = (
        'category',
        'is_active',
        'created_at',
    )

    search_fields = (
        'title',
        'description',
        'user__username',
    )


@admin.register(AnnouncementSubscription)
class AnnouncementSubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'announcement',
        'created_at',
    )

    search_fields = (
        'user__username',
        'announcement__title',
    )


@admin.register(SavedAnnouncement)
class SavedAnnouncementAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'announcement',
        'created_at',
    )

    search_fields = (
        'user__username',
        'announcement__title',
    )
