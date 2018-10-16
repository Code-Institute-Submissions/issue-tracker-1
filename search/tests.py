from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class TestSearchViews(TestCase):
    '''
    Test that search results page is loaded
    '''
    def test_call_view_loads(self):
        response = self.client.get('%s?q=%s' % (reverse('search'), 'test'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search_results.html')