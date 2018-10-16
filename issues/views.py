from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import Issue, IssueCategory
from .forms import IssueForm, IssueEditForm
from django.contrib import messages
from django.conf import settings
from django.db.models import Sum, Count
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required
from django.db.models.functions import TruncMonth
from datetime import date
from dateutil.relativedelta import relativedelta
from accounts.forms import UserLoginForm
from voting.models import Upvote
from django.core.paginator import Paginator, EmptyPage

def homepage(request):
    issues = Issue.objects.all()
    if request.user.is_authenticated():
        # Create a list of the last 6 months to find issue updates from each
        # month. 
        monthly_counts = []
        last_year = []
        # Solution below from http://blog.e-shell.org/94
        for i in range(0,12):
            last_year.append(
                (date.today() + relativedelta(months=-i))
            )
        # For each month, count the number of issues updated and completed
        for month in last_year:
            updated_count = Issue.objects.filter(
                updated__month__exact=month.month).count()
            completed_count = Issue.objects.filter(
                completed__month__exact=month.month).count()
            monthly_counts.append({
                "month": month,
                "updated": updated_count,
                "completed": completed_count,
            })
        top_open_bugs = (
            Issue.objects.filter(issue_type='BG', completed__isnull=True)
        )
        top_open_requests = (
            Issue.objects.filter(issue_type='FR', completed__isnull=True)
        )
        categories = (IssueCategory.objects
            .annotate(issue_count=Count('issue'))
            .order_by('-issue_count'))
        # sorting using key function so model property can be used
        # https://wiki.python.org/moin/HowTo/Sorting#Key_Functions
        top_open_bugs = sorted(
            top_open_bugs, 
            key=lambda b: b.total_upvotes,
            reverse=True)[:4]
        top_open_requests = sorted(
            top_open_requests, 
            key=lambda b: b.total_credits,
            reverse=True)[:4]
        return render(request, "dashboard.html", {
            "issues": issues,
            "monthly_counts": monthly_counts,
            "top_open_bugs": top_open_bugs,
            "top_open_requests": top_open_requests,
            "categories": categories,
        })
    else:
        user_form = UserLoginForm()
        return render(
            request, "home.html", {'user_form': user_form, "issues": issues})

'''
View to handle all the different ways that issue lists can be displayed:
By open/closed, by type (Bug/Request), by status (New, Under Review, etc.),
and by category.
'''
def issues_list(
        request, 
        page=1, 
        issue_type=None, 
        status=None, 
        open_issues=True, 
        category=None):
    status_choice = None
    category_obj = None
    if issue_type:
        if issue_type == 'BG':
            title = 'Bugs'
            viewname_type = 'all_open_bugs'
        else:
            title = 'Feature Requests'
            viewname_type = 'all_open_requests'
        issues = Issue.objects.filter(
            issue_type=issue_type, completed__isnull=open_issues)
        # Link root in template because pagination links will be different 
        # for different filters
        link_root = reverse(viewname_type)
    else:
        if status:
            # Status is passed as string, so needs to be matched to one of the
            # choices variables
            status_choices = Issue.STATUS_CHOICES
            for choice in status_choices:
                if choice[1] == status:
                    status_choice = choice[0]
            if status_choice:
                title = 'Issues'
                link_root = reverse(
                    'all_issues_by_status', 
                    args=[status])
                issues = Issue.objects.filter(status=status_choice)
                status = status.replace("-", " ").title()
            else:
                # String didn't match any status_choice, so just show all issues
                title = 'Issues'
                link_root = reverse('all_open_issues')
                issues = Issue.objects.filter(completed__isnull=open_issues)
        else:
            if category:
                title = 'Issues'
                link_root = reverse(
                    'all_issues_by_category',
                    args=[category])
                try:
                    category_obj = IssueCategory.objects.get(pk=category)
                    issues = Issue.objects.filter(category=category_obj)
                except DoesNotExist:
                    # Category didn't match any existing categories, so just show all issues
                    link_root = reverse('all_open_issues') 
                    issues = Issue.objects.filter(completed__isnull=open_issues)
            else:
                title = 'Issues'
                link_root = reverse('all_open_issues')
                issues = Issue.objects.filter(completed__isnull=open_issues)
    if open_issues:
        title_prefix = 'Open'
    else:
        title_prefix = 'Closed'
    issues.order_by('-updated')
    paginator = Paginator(issues, settings.ISSUES_PER_PAGE)
    page_range = paginator.page_range
    try:
        issue_page = paginator.page(page)
    except EmptyPage:
        issue_page = None
    return render(request, "issues_list.html", {
        "issue_page": issue_page, 
        "title": title,
        "title_prefix": title_prefix,
        "link_root": link_root,
        "status": status,
        "status_choice": status_choice,
        "show_closed": (not open_issues),
        "page_range": paginator.page_range,
        "category": category_obj
    })

def issue_detail(request, id):
    issue = get_object_or_404(Issue, pk=id)
    votes = {}
    if request.user.is_authenticated():
        votes = Upvote.objects.filter(target=issue, creator=request.user)
    return render(
        request, "issue_detail.html", {"issue": issue, "votes": votes })

@login_required
def issue_create(request):
    if request.method == 'POST':
        form = IssueForm(request.POST)
        if form.is_valid():
            issue_data = form.cleaned_data
            new_issue = Issue.objects.create(
                title = issue_data['title'],
                creator = request.user,
                category = issue_data['category'],
                issue_type = issue_data['issue_type'],
                description = issue_data['description']
            )
            return redirect('view_issue', id=new_issue.id)
    else:
        form = IssueForm()
    return render(request, "issue_create.html", {'form': form})

