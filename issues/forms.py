from django.forms import ModelForm
from .models import *

class IssueForm(ModelForm):
    class Meta:
        model = Issue
        fields = ['title', 'category', 'issue_type', 'description']

class IssueEditForm(ModelForm):
    class Meta:
        model = Issue
        fields = ['title', 'category', 'description']
