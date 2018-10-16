from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class TestIssueViews(TestCase):
    def setUp(self):
        # Create a user for views that require login
        self.user = User.objects.create_user(username='testuser', password='12345')

    '''
    Test that views that require login redirect to the correct place for
    anonymous users
    '''
    def test_call_view_denies_anonymous(self):
        response = self.client.get(reverse('create_issue'), follow=True)
        self.assertRedirects(response, reverse('login') + "?next=" + reverse('create_issue'))
        response = self.client.get(reverse('home'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    '''
    Test that logged in user can see views that require login
    '''
    def test_call_view_loads(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('create_issue'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'issue_create.html')
        response = self.client.get(reverse('home'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard.html')

    '''
    Test whether sending empty data to issue creation view fails as expected
    '''
    def test_call_view_fails_blank(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('create_issue'), {})
        self.assertFormError(response, 'form', 'title', 'This field is required.')