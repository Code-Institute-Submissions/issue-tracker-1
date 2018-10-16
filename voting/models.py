from django.db import models
from django.contrib.auth.models import User
from issues.models import Issue

class Upvote(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    target = models.ForeignKey(
        Issue, on_delete=models.CASCADE, related_name='upvotes')
    credits = models.IntegerField(default=0)

    def __str__(self):
        return 'Upvote on %s by %s' % (self.target.title, self.creator.username)