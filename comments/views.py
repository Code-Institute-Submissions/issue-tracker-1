from django.shortcuts import render
from django.http import JsonResponse
from http import HTTPStatus
from issues.models import Issue
from .models import Comment
from django.utils.html import escape
from django.core import serializers

def add_comment(request):
    if request.method == 'POST':
        if request.user.is_authenticated():
            issue_id = request.POST.get('issue_id', None)
            if issue_id:
                issue = Issue.objects.filter(id=issue_id).first()
                if not issue:
                    return JsonResponse({
                        'error': 'issue_not_found',
                    }, status = HTTPStatus.BAD_REQUEST)
                else:
                    text = request.POST.get('text', None)
                    if not text or text == '':
                        return JsonResponse({
                            'error': 'empty_comment',
                        }, status = HTTPStatus.BAD_REQUEST)
                    # We've checked everything, now we can comment
                    new_comment = Comment.objects.create(
                        creator=request.user,
                        text=escape(text),
                        target=issue, 
                    )
                    return JsonResponse({
                        # Have to wrap with list for JSON
                        # https://stackoverflow.com/a/3289057/850947
                        'new_comment': new_comment.text
                    }, status = HTTPStatus.CREATED)
            else:
                return JsonResponse({
                    'error': 'no_issue_id',
                }, status = HTTPStatus.BAD_REQUEST)
        else:
            return JsonResponse({
                'error': 'user_not_logged_in',
            }, status = HTTPStatus.UNAUTHORIZED)
    else:
        return JsonResponse({
            'error': 'request_not_post',
        }, status = HTTPStatus.BAD_REQUEST)
