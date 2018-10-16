from django.db import models
from django.contrib.auth.models import User
from issues.models import Issue

class Comment(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    target = models.ForeignKey(
        Issue, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return \
            'Comment on %s by %s' % (self.target.title, self.creator.username)