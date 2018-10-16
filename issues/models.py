from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models.signals import pre_save
from django.dispatch import receiver
from datetime import datetime, timezone

class IssueCategory(models.Model):
    name = models.CharField(max_length=254)
    priority = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "issue categories"

class Issue(models.Model):
    BUG = 'BG'
    FEATURE_REQUEST = 'FR'
    TYPE_CHOICES = (
        (BUG, 'Bug'),
        (FEATURE_REQUEST, 'Feature Request'),
    )

    NEW = 'NW'
    UNDER_REVIEW = 'UR'
    DECLINED = 'DE'
    NEEDS_MORE_INFO = 'NM'
    PLANNED = 'PD'
    IN_PROGRESS = 'IP'
    COMPLETED = 'CP'
    STATUS_CHOICES = (
        (NEW, 'new'),
        (UNDER_REVIEW, 'under-review'),
        (DECLINED, 'declined'),
        (NEEDS_MORE_INFO, 'needs-more-info'),
        (PLANNED, 'planned'),
        (IN_PROGRESS, 'in-progress'),
        (COMPLETED, 'completed'),
    )

    title = models.CharField(max_length=254)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(IssueCategory, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=2, choices=STATUS_CHOICES, default=NEW)
    issue_type = models.CharField(
        max_length=2, choices=TYPE_CHOICES, default=BUG)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(blank=True, null=True, editable=False)
    completed = models.DateTimeField(blank=True, null=True, editable=False)

    class Meta:
        ordering=['-updated']

    def __str__(self):
        return self.title

    def is_feature_request(self):
        return self.issue_type == self.FEATURE_REQUEST

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('view_issue', args=[str(self.id)])

    @property
    def status_label(self):
        return self.get_status_display().replace("-", " ").title()

    @property
    def total_credits(self):
        issue_total = Issue.objects.filter(id=self.id).aggregate(total_credits=Sum('upvotes__credits'))
        if issue_total['total_credits']:
            return issue_total['total_credits']
        else:
            return 0

    @property
    def total_upvotes(self):
        return self.upvotes.count()

    @property
    def is_complete(self):
        return self.completed is not None

'''
Compares updates to previous instance of Issue to make automated changes to
un-editable fields
Solution to getting previous instance from https://stackoverflow.com/a/7934958
'''
@receiver(pre_save, sender=Issue)
def handle_updates(sender, instance, **kwargs):
    try:
        original = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        pass
    else:
        # Only some fields being modified should change the updated timestamp
        if ((original.category != instance.category) or
            (original.status != instance.status) or
            (original.issue_type != instance.issue_type)):
            instance.updated = datetime.now(timezone.utc)
        # When admin sets issue status to declined or completed, completed
        # date is set also because issue is now closed either way.
        if ((original.status != instance.status) and 
                ((instance.status == Issue.DECLINED) or 
                (instance.status == Issue.COMPLETED))):
            instance.completed = datetime.now(timezone.utc)