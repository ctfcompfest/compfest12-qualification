from django.db import models
from django.contrib.auth.models import User

class ForumTopic(models.Model):
    topicTitle = models.CharField(max_length=25)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date = models.DateTimeField("Published at")

    def __str__(self):
        return self.topicTitle

class ForumText(models.Model):
    textTitle = models.CharField(max_length=25)
    forumText = models.CharField(max_length=5000)
    forumTopic = models.ForeignKey(ForumTopic, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.forumText
