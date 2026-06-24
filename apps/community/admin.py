from django.contrib import admin
from apps.community.models import ForumThread, ForumPost, Announcement, LessonComment


@admin.register(ForumThread)
class ForumThreadAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'author', 'created_at')
    list_filter = ('course',)


@admin.register(ForumPost)
class ForumPostAdmin(admin.ModelAdmin):
    list_display = ('thread', 'author', 'created_at')


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'author', 'created_at')
    list_filter = ('course',)


@admin.register(LessonComment)
class LessonCommentAdmin(admin.ModelAdmin):
    list_display = ('lesson', 'author', 'parent', 'created_at')
