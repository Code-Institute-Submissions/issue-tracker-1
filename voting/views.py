from django.shortcuts import render
from django.http import JsonResponse
from http import HTTPStatus
from issues.models import Issue
from .models import Upvote
from django.db.models import Sum

def add_bug_upvote(request):
    if request.method == 'POST':
        if request.user.is_authenticated():
            issue_id = request.POST.get('issue_id', None)
            if issue_id:
                issue = Issue.objects.filter(id=issue_id).first()
                if not issue:
                    # Issue ID was not valid
                    return JsonResponse({
                        'error': 'issue_not_found',
                    }, status = HTTPStatus.BAD_REQUEST)
                else:
                    if issue.is_feature_request():
                        # Only upvote bugs with this view, not feature requests
                        return JsonResponse({
                            'error': 'request_not_bug',
                        }, status = HTTPStatus.BAD_REQUEST)
                    else:
                        new_vote, created = Upvote.objects.get_or_create(
                            creator = request.user,
                            target = issue
                        )
                        if created:
                            return JsonResponse({
                                'new_vote_count': issue.upvotes.count(),
                            }, status = HTTPStatus.CREATED)
                        else:
                            # Upvote object was found, not created, which means
                            # user had already voted
                            return JsonResponse({
                                'error': 'already_voted',
                            }, status = HTTPStatus.FORBIDDEN)
            else:
                # Issue ID wasn't supplied in POST
                return JsonResponse({
                    'error': 'no_issue_id',
                }, status = HTTPStatus.BAD_REQUEST)
        else:
            # Only logged in user can vote
            return JsonResponse({
                'error': 'user_not_logged_in',
            }, status = HTTPStatus.UNAUTHORIZED)
    else:
        # Need a POST request
        return JsonResponse({
            'error': 'request_not_post',
        }, status = HTTPStatus.BAD_REQUEST)

def add_feature_request_upvote(request):
    if request.method == 'POST':
        if request.user.is_authenticated():
            issue_id = request.POST.get('issue_id', None)
            if issue_id:
                issue = Issue.objects.filter(id=issue_id).first()
                if not issue:
                    return JsonResponse({'error': 'no_issue_found',
                    }, status = HTTPStatus.BAD_REQUEST)
                else:
                    if not issue.is_feature_request():
                        return JsonResponse({
                            'error': 'bug_not_request',
                        }, status = HTTPStatus.BAD_REQUEST)
                    else:
                        credits_voted = request.POST.get('amount', None)
                        if not credits_voted:
                            return JsonResponse({
                                'error': 'no_credit_amount',
                            }, status = HTTPStatus.BAD_REQUEST)
                        credits_voted = int(credits_voted)
                        user_balance = request.user.profile.credits
                        if user_balance < credits_voted:
                            return JsonResponse({
                                'error': 'not_enough_balance',
                            }, status = HTTPStatus.BAD_REQUEST)
                        # We've checked everything, now we can add upvote
                        request.user.profile.credits -= credits_voted
                        request.user.profile.save()
                        new_vote = Upvote.objects.create(
                            creator = request.user,
                            target = issue,
                            credits = credits_voted,
                        )
                        return JsonResponse({
                            'new_vote_count': issue.upvotes.count(),
                            'new_pledge_total': issue.total_credits,
                        })
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