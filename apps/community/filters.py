import django_filters
from apps.community.models import ForumThread, Announcement, LessonComment


class ForumThreadFilter(django_filters.FilterSet):
    class Meta:
        model = ForumThread
        fields = ['course', 'author']


class AnnouncementFilter(django_filters.FilterSet):
    class Meta:
        model = Announcement
        fields = ['course', 'author']


class LessonCommentFilter(django_filters.FilterSet):
    class Meta:
        model = LessonComment
        fields = ['lesson', 'author', 'parent']
