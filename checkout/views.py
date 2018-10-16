from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.utils import timezone
from accounts.models import Subscription
from datetime import timedelta
import stripe

stripe.api_key = settings.STRIPE_SECRET

@login_required()
def subscription_purchase(request):
    """ Take users Stripe card token and charge a year's subscription """
    if request.method=="POST":
        # POST request means user submitted Stripe card form
        if "stripeToken" in request.POST:
            try:
                customer = stripe.Charge.create(
                    amount = 60*100,
                    currency = "EUR",
                    description = request.user.email,
                    source = request.POST.get('stripeToken'),
                )
            except stripe.error.CardError:
                messages.error(request, "Your card was declined!")
                return redirect('subscription_purchase')
            if customer.paid:
                """ If a subscription already existed, this was a renewal
                    if not, new Subscription is created, default expiry calculated
                    within the Subscription model """
                subscription, created = Subscription.objects.get_or_create(
                    user=request.user
                )
                # Each subscription renewal adds credits to user's profile
                profile = request.user.profile
                profile.credits += settings.CREDITS_PER_SUBSCRIPTION
                profile.save()
                if created:
                    return render(request, 'subscription_added.html')
                else:
                    # For renewals, add 365 days to expiry date
                    subscription.expires += timedelta(days=365)
                    subscription.save()
                    return render(request, 'subscription_added.html')
            else:
                messages.error(request, "Unable to take payment")
                return redirect('subscription_purchase')
        else:
            messages.error(request, "Stripe token was invalid")
            return redirect('subscription_purchase')
    else:
        # Non-POST request means we render the card form.
        return render(request, "subscription_checkout.html", {
            'publishable': settings.STRIPE_PUBLISHABLE
        })

@login_required()
def credits_purchase(request):
    """ Uses Stripe card form to charge for optional additional credits """
    if request.method=="POST":
        """ POST request can come from card form submit or from initial
            credits amount selection page """
        try:
            credits_amount = int(request.POST.get('credits_amount', None))
        except TypeError:
            messages.error(request, "Amount was invalid")
            return redirect('add_credits')
        if credits_amount or credits_amount == 0:
            if (credits_amount % 10) is not 0:
                # Credits amount wasn't a multiple of 10, so user bypassed
                # JavaScript form validation
                messages.error(
                    request, 
                    "Credits can only be added in multiples of 10"
                )
                return redirect('add_credits')
            credits_cost = \
                settings.COST_PER_TEN_CREDITS * (credits_amount / 10)
            if "stripeToken" in request.POST:
                # POST request came from card form submit
                try:
                    customer = stripe.Charge.create(
                        amount = int(credits_cost*100),
                        currency = "EUR",
                        description = request.user.email,
                        source = request.POST['stripeToken'],
                    )
                except stripe.error.CardError:
                    messages.error(request, "Your card was declined!")
                    return redirect('credits_purchase')
                if customer.paid:
                    # All is good, so add the chosen amount of credits
                    profile = request.user.profile
                    profile.credits += credits_amount
                    profile.save()
                    return render(request, 'credits_added.html')
                else:
                    messages.error(request, "Unable to take payment")
                    return redirect('credits_purchase')
            else:
                """ POST request came from initial credits selection page
                    so now render Stripe card form """
                return render(request, "credits_checkout.html", {
                    'publishable': settings.STRIPE_PUBLISHABLE,
                    'ten_credit_cost': settings.COST_PER_TEN_CREDITS,
                    'credits_amount': credits_amount,
                    'total': credits_cost,
                })
        else:
            messages.error(request, "No amounts of credits selected")
            return redirect('add_credits')
    else:
        return redirect('add_credits')
    