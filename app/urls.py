from django.conf.urls import url, include
from django.contrib import admin
from accounts import urls as urls_accounts
from search import urls as urls_search
from checkout import urls as urls_checkout
from issues import urls as urls_issues
from comments import urls as urls_comments
from voting import urls as urls_voting
from issues.views import homepage
from django.views import static
from .settings import MEDIA_ROOT

urlpatterns = [
    url(r'^$', homepage, name='home'),
    url(r'^accounts/', include(urls_accounts)),
    url(r'^admin/', admin.site.urls),
    url(r'^checkout/', include(urls_checkout)),
    url(r'^comments/', include(urls_comments)),
    url(r'^issues/', include(urls_issues)),
    url(r'^search/', include(urls_search)),
    url(r'^upvote/', include(urls_voting)),
    url(r'^media/(?P<path>.*)$', static.serve,{'document_root': MEDIA_ROOT}),
]