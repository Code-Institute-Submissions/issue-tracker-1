from django.contrib import admin
from .models import *
    
@admin.register(Upvote)
class UpvoteAdmin(admin.ModelAdmin):
    pass

