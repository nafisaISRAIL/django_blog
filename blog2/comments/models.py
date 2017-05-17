from __future__ import unicode_literals

from django.db import models
from blog2.posts.models import Post
from django.conf import settings


# Create your models here.


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    comment = models.TextField()
    created_at = models.DateField(auto_now=True)

    def __unicode__(self):
        return self.comment
