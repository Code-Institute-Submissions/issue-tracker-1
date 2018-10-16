from django.shortcuts import render
from issues.models import Issue

def do_search(request):
    issues = Issue.objects.filter(title__icontains=request.GET['q'])
    return render(request, "search_results.html", {
        "issues": issues,
        "query": request.GET.get('q', None)
    })
