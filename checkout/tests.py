from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class TestCheckoutViews(TestCase):
    def setUp(self):
        # Create a user for views that require login
        self.user = User.objects.create_user(username='testuser', password='12345')

    '''
    Test that views that require login redirect to the correct place for
    anonymous users
    '''
    def test_call_view_denies_anonymous(self):
        response = self.client.get(reverse('subscription_purchase'), follow=True)
        self.assertRedirects(response, reverse('login') + "?next=" + reverse('subscription_purchase'))
        response = self.client.get(reverse('credits_purchase'), follow=True)
        self.assertRedirects(response, reverse('login') + "?next=" + reverse('credits_purchase'))

    '''
    Test that logged in user can see views that require login
    '''
    def test_call_view_loads(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('subscription_purchase'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'subscription_checkout.html')
        response = self.client.get(reverse('credits_purchase'))
        self.assertRedirects(response, reverse('add_credits'))

    '''
    Test whether sending empty data to issue creation view fails as expected
    '''
    def test_call_view_fails_blank(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('subscription_purchase'), {})
        self.assertRedirects(response, reverse('subscription_purchase'))
        response = self.client.post(reverse('credits_purchase'), {})
        self.assertRedirects(response, reverse('add_credits'))