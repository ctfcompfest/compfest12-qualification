from django.contrib import admin

from .models import  ForumTopic, ForumText

class ForumTopicAdmin(admin.ModelAdmin):
    fields = ['topicTitle', 'user']

class ForumTextAdmin(admin.ModelAdmin):
    fields = ['textTitle', 'forumText', 'forumTopic', 'user']

admin.site.register(ForumTopic, ForumTopicAdmin)
admin.site.register(ForumText, ForumTextAdmin)