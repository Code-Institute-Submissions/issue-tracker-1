from django.contrib import admin
from .models import *
    
@admin.register(IssueCategory)
class IssueCategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display=('id','title','creator','category','status','issue_type','updated','completed',)
    list_filter=('category','status','issue_type','updated','completed',)
    search_fields=('title','creator__username',)
    readonly_fields=('created','updated','completed',)
