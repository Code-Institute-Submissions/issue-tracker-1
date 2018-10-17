# Hello World!
This is my final Exam project.

# Project: Support For You: an issue tracker
Welcome to Support For You, a community-driven site where you can report bugs or
request features, upvote already reported bugs, and give funding to boost 
feature requests.

Visit my website [here](https://annies-issue-tracker.herokuapp.com/) 

## Introduction

*Support For You* is an issue tracking site that lets people report bugs or make 
feature requests. It can be adapted to work with any kind of product that 
requires support - an app, a website, a shop, or a service. 
This helps the company or people that create that product to track and prioritise
the issues that they need to solve for customers.

Issues can be categorised under an admin-controlled list of Issue Categories, 
and they are given a status that shows their progress (such as 'New' or 'Under Review',
'Accepted', or 'Denied'). 
There are just two types of issue: a bug and a feature request. 


Registered users of *Support For You* are encouraged to comment on other bugs and
feature requests, and they can freely 'upvote' any bug that is reported. 
Registered users can also upload a profile photo to help them stand out. 


They are also encouraged to upgrade to the Premium subscription, which gives 
them a number of credits that they can then donate to a Feature Request. 
Requests with the most credits donated to them are more likely to be accepted 
and worked on, and when accepted, the credits are used to provide funding for 
the time and effort needed to create the feature.


Premium users can also purchase additional credits beyond those that they are 
given with their subscription. After a year, their subscription will end and 
they can renew, when they will receive another bundle of credits. 

Premium users are also promised that any bugs or feature requests that they 
themselves create will be given higher priority by admins. 

All payments for credits and subscriptions are processed securely by 
Stripe's Javascript SDK, and details are not stored anywhere but with Stripe. 

For transparency, registered users can view a dashboard on their homepage showing
the monthly progress of issue updates and completions, as well as the most popular
bugs, feature requests, and categories of issue. 


## Development

### Requirements
- [Python 3.5.2 is required](https://www.python.org/downloads/release/python-352/)

### Preparation
- Clone repository
- Copy `env.example` to `env.py` and enter values for all environmental variables listed.
- Run `pip install -r requirements.txt` (or `pip3` if necessary for Python 3).
- Run any migrations using:
  - `python manage.py makemigrations` (or `python3` if necessary)
  - `python manage.py migrate`
- Run `python manage.py collectstatic` to generate static files.
- Run `python manage.py runserver` and browse to generated local URL.

### Deployed code
Visit my website [here](https://annies-issue-tracker.herokuapp.com/) 

## Testing

### Manual Testing Process
- Browse to homepage while logged out, check that correct logged out template is rendered
- Try navigating to /issues/create/ while logged out, check that login is required
- While logged out:
  - Open any issue detail page
  - Open the 'All Open Issues' page (/issues/)
  - Click on the 'Closed' tab on above page and check that 'All Closed Issues' list is loaded
  - Click on issue type dropdown selector in top-right of above page, choose 'Bugs' and check that correctly filtered list of bug issues is shown.
  - Repeat above for 'Feature Requests'
  - Click on the status (New/Under Review/Declined/etc) badge for one of the listed issues and check that issue-by-status list page is correctly loaded.
- From homepage, click 'Learn More' to go to registration form.
- Leave all fields blank and attempt to submit form, see validation error messages.
- Enter random, non-email string in email address field and see that it prompts for a valid email.
- Enter invalid special character in username field, check for validation.
- Enter password confirmation differently to first password, check for validation.
- Fill in form correctly and submit, check that it works and user is redirect to homepage with a logged in status.
- While logged in:
  - Check that homepage now shows issue dashboard with various statistics, particularly the JavaScript rendering 'Monthly Progress' graph.
  - Repeat flow from logged out steps above.
  - Return to homepage and click on one of the categories under 'Top Issue Categories', check that correctly filtered list of issues for that category is shown.
  - Click on 'Your Account' link in header
  - Click 'Edit Profile Picture', select an image to upload, and click 'Upload and Save', then check that photo was correctly updated.
  - Click on 'Subscribe to Premium' button, then again on the next page, then on Card Details page:
    - Try submitting with invalid and blank details to test validation (from Stripe's own JS)
      - Enter the following and click 'Make Payment':
      - Card Number: 4242 4242 4242 4242
      - Expiry: any future date
      - CVC: 123
      - ZIP: 12345
  - Check that payment is successfully processed, user is now upgraded with 'premium' and has been given 500 credits. 
  - Return to 'Your Account' and click 'Buy More Credits', and on the next screen where asked to select amount:
    - Try entering a number that is not a multiple of 10, check validation
    - Try entering a number that is less than 10, check form will not submit
    - Try entering a number that is greater than 500, check form will not submit
    - Use buttons to select '50' credits and click 'Buy more' button
  - Test card details page as above, including successful payment.
  - Check that user now has 550 credits. 
  - Go to 'All Open Feature Requests' list (/issues/requests/) and select one of the requests.
  - Click on the 'Fund' button on top right:
    - Try entering 600 credits, check that 'not enough credits' message is displayed
    - Enter 100 credits and press 'Add credits' button, check that request has now been funded with an extra 100 credits.
  - Go to 'All Open Bugs' list (/issues/bugs/) and select any bug, then click on the 'vote' button in the top right. Check that 1 extra vote has been added and that user cannot click a second time.
  - Still on bug page, click 'Add Comment' button without entering any text, check that empty comment validation message appears.
  - Enter a comment into the comment textarea, and submit again, check that new comment appears via AJAX without page reloading.
  - Return to homepage, type a test string into the search bar, checking:
    - A string that should produce results (ie. appears in some issue titles) does
    - A string that shouldn't produce results shows an empty list
  - Goto issue creation form (/issues/create/) and test validation:
    - Leave all fields blank
    - Leave category as default ('-------')
  - Test form with valid data and submit, check that new issue is created and user is redirect to view it.
  - Click logout, check user is properly logged out.

### Automated Tests

Created unit tests for:
- Testing whether logged out client is properly redirected when login is required for views in issues/ and checkout/
- Testing whether logged in client can properly access login restricted views in issues/ and checkout/
- Testing whether issue creation form rejects empty fields correctly
- Testing that search results view is correctly loaded

[![Build Status](https://travis-ci.org/coffeeipsum/issue-tracker.svg?branch=master)](https://travis-ci.org/coffeeipsum/issue-tracker)

## Third Party Software // Code credits

- [Python 3.5.2](https://www.python.org/downloads/release/python-352/)
- [Django 1.11](https://docs.djangoproject.com/en/2.1/releases/1.11/)
- [jQuery 3.3.1](https://jquery.com/download/)
- [Bootstrap 4.1.2](http://blog.getbootstrap.com/2018/07/12/bootstrap-4-1-2/)
- [Chart.js](https://www.chartjs.org/) (used for 'monthly progress' graph on logged-in homepage)
- [jquery-modal](http://jquerymodal.com/) (used for dialog when 'funding' a feature request)
- [bootstrap-input-spinner](https://www.jqueryscript.net/form/Input-Spinner-Plugin-Bootstrap-4.html) (used to select number of credits)
- [Google Fonts Roboto](https://fonts.google.com/specimen/Roboto)
- [FontAwesome](https://fontawesome.com/) (used for site logo, bug/request icons)
- [django-forms-bootstrap](https://django-bootstrap-form.readthedocs.io/en/latest/) (used to style all forms)
- [django-registration 3.0](https://django-registration.readthedocs.io/en/3.0/) (used to provide login/registration views)
- [Pillow 5.3](https://pillow.readthedocs.io/en/5.3.x/reference/Image.html) (required for thumbnails)
- [easy-thumbnails 2.5](https://easy-thumbnails.readthedocs.io/en/stable/) (generates profile photo thumbnails)
- [django-storages 1.6](https://django-storages.readthedocs.io/en/1.6.2/backends/amazon-S3.html) (used to connect with AWS S3 storage)
- [Stripe JS SDK](https://stripe.com/docs/stripe-js) (used to process payments and generate card details form)