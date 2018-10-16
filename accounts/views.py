from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib import messages, auth
from django.core.urlresolvers import reverse
from .forms import UserLoginForm, UserRegistrationForm, ProfileEditForm
from django.template.context_processors import csrf
from django.contrib.auth.decorators import login_required
from accounts.models import Profile, Subscription
from datetime import datetime, timedelta
from django.conf import settings
from django.utils import timezone

def logout(request):
    """A view that logs the user out and redirects back to the index page"""
    auth.logout(request)
    messages.success(request, 'You have successfully logged out')
    return redirect(reverse('home'))

def login(request):
    """A view that manages the login form"""
    if request.method == 'POST':
        user_form = UserLoginForm(request.POST)
        if user_form.is_valid():
            user = auth.authenticate(request.POST['username'],
                                     password=request.POST['password'])
            if user:
                auth.login(request, user)
                messages.error(request, "You have successfully logged in")
                if request.GET and request.GET['next'] !='':
                    next = request.GET['next']
                    return HttpResponseRedirect(next)
                else:
                    return redirect(reverse('home'))
            else:
                user_form.add_error(
                    None, 
                    "Your username or password are incorrect"
                )
    else:
        user_form = UserLoginForm()

    args = {'user_form': user_form, 'next': request.GET.get('next', '')}
    return render(request, 'login.html', args)

@login_required
def profile(request):
    """ A view that displays the profile page of the logged in user """
    profile = request.user.profile
    return render(request, 'profile.html', {'profile': profile})

@login_required
def profile_edit(request):
    """ Edit the profile of the currently logged in user"""
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileEditForm(instance=profile)
    return render(request, "profile_edit.html", {'form': form})

@login_required
def profile_upgrade(request):
    """ Allow the user to upgrade their profile with pro subscription """
    # First check to see if they already have a subscription
    subscription = Subscription.objects.filter(user=request.user).first()
    if not subscription:
        return render(request, 'profile_upgrade_start.html')
    if subscription:
        # Existing subscriptions are renewable if only 30 days are left on them
        if subscription.expires <= (timezone.now() + timedelta(days=30)):
            return render(request, 'profile_upgrade_start.html')
        else:
            # Users existing subscription is not yet renewable
            return render(request, 'profile_upgrade_error.html', {
                'subscription': subscription,
                'reason': 'already_subscribed',
            })

@login_required
def add_credits(request):
    """Allow a user to pick number of Credits to add to their profile"""
    
    return render(request, 'add_credits_start.html', {
        'credits_per_subscription': settings.CREDITS_PER_SUBSCRIPTION
    })

def register(request):
    """A view that manages the registration form"""
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            user_form.save()
            user = auth.authenticate(request.POST.get('email'),
                                     password=request.POST.get('password1'))
            if user:
                auth.login(request, user)
                messages.success(request, "You have successfully registered")
                return redirect(reverse('home'))

            else:
                messages.error(request, "unable to log you in at this time!")
    else:
        user_form = UserRegistrationForm()

    args = {'user_form': user_form}
    return render(request, 'register.html', args)
