"""
Alright, remember urls.py? If not, go back and refresh your memory. Django's views are simply Python functions,
so you can import any of the functions below into urls.py for reference in a django.conf.urls.ulr().

Bottom line: HttpRequest comes in to a Django view, HttpResponse goes out. Parameters in your URL's regular expression
are passed in sequentlly as additional arguments after Django's "request".

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/http/views/
"""

from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.conf import settings

# Import our models so we can interact with our database in our views
from djangopolls.models import Poll, Choice, Vote


def home(request):
    # When accessing the Django ORM, we can chain database calls like "filter" and "exclude" together
    # to further refine our search ... don't worry, Django won't evaluate the expression until your
    # variable is actually
    open_polls = Poll.objects.filter(close_date=None).exclude(open_date=None)
    closed_polls = Poll.objects.exclude(close_date=None)

    # The HttpResponse that we return from this function is what Django will render for our user, so
    # this case have a look ino the "templates" folder for "home.html" to see what's being rendered
    # and how we're using variables like "SITE_TITLE" and "closed_polls"
    response = render_to_response('home.html',
                                  {'SITE_TITLE': settings.SITE_TITLE, 'host': request.get_host(),
                                   'open_polls': open_polls, 'closed_polls': closed_polls},
                                  context_instance=RequestContext(request))

    return response


def poll(request, poll_id):
    # If you look in urls.py, you'll see that our URL accepts the regular expression parameter of ([0-9]+),
    # meaning one (or more) digits should be passed as an argument to this view; lo and behold, this
    # function has a poll_id argument for just such an occassion
    try:
        # Get from the database the Poll that has this unique ID, but only if it's been opened for voting
        poll = Poll.objects.exclude(open_date=None).get(pk=poll_id)
        # Get from the database the list of Choices associated with this Poll
        choices = Choice.objects.filter(poll=poll)

        # If the poll is closed, or we're a super user trying to view the results of an open poll ...
        if poll.close_date != None or (
                        request.user.is_authenticated() and request.user.is_superuser and 'results' in request.GET):
            # Note that until we call some evaluative function like count() or all(), we have a chained and
            # optimized Django QuerySet
            votes = Vote.objects.filter(accepted=True).all()
            vote_counts = {}
            vote_percentages = {}
            # All this processing is building toward passing something to a Django template, right? Django's template
            # language is intentionally simplistic, as intensive processing within the template won't be as speedy as
            # processing in Python, so we should do as much heavy lifting in Python and pass the results into the
            # template instead of trying to process data during template parsing
            for choice in choices:
                vote_count = Vote.objects.filter(choice=choice, accepted=True).count()
                vote_counts[choice.pk] = vote_count
                vote_percentages[choice.pk] = (float(vote_count) / float(
                    votes.count())) * 100 if vote_count > 0 else 0

            response = render_to_response('poll_results.html',
                                          {'SITE_TITLE': settings.SITE_TITLE, 'host': request.get_host(), 'poll': poll,
                                           'choices': choices, 'votes': votes, 'vote_counts': vote_counts,
                                           'vote_percentages': vote_percentages},
                                          context_instance=RequestContext(request))
        # If the poll is open for voting ...
        else:
            if choices.count() > 0:
                # No processing to do, just render the page and let the user vote, which will trigger our vote() view
                response = render_to_response('poll_open.html',
                                              {'SITE_TITLE': settings.SITE_TITLE, 'host': request.get_host(),
                                               'poll': poll, 'choices': choices},
                                              context_instance=RequestContext(request))
            else:
                response = render_to_response('status.html', {'SITE_TITLE': settings.SITE_TITLE,
                                                              'host': request.get_host(), 'heading': 'No Dice',
                                                              'message': 'Looks like the poll creator hasn\'t made any choices yet for this poll.'},
                                              context_instance=RequestContext(request))
    
    # The Poll ID given in the URL doesn't exist in the Database, so Django throw's an exception
    except Poll.DoesNotExist:
        response = render_to_response('status.html', {'SITE_TITLE': settings.SITE_TITLE, 'host': request.get_host(),
                                                      'heading': 'No Dice',
                                                      'message': 'Sorry, we couldn\'t find a poll here. Maybe it\'s not open yet?'},
                                      context_instance=RequestContext(request))

    # Whew. Now return the HttpResponse object that our render_to_response() call created for us
    return response


def vote(request, poll_id):
    try:
        poll = Poll.objects.exclude(open_date=None).get(pk=poll_id)

        # If the user is POSTing ...
        if request.method == 'POST':
            # Voting requires an email address
            if 'email' in request.POST:
                # We can reference our variables we set in settings.py to see if certain things are enabled or not,
                # in this case, do we want to validate against a particular email domain?
                if not settings.REQUIRED_EMAIL_EXTENSION or settings.REQUIRED_EMAIL_EXTENSION in request.POST['email']:
                    # If the user gave a choice for their vote ...
                    if 'choice' in request.POST:
                        # Try to retrieve the choice from the database to ensure it's valid (Django will throw an exception if not)
                        choice = Choice.objects.get(pk=request.POST['choice'])
                        
                        # If the user has not attempted voting before
                        if Vote.objects.filter(email=request.POST['email'], choice__poll=poll).count() == 0:
                            vote = Vote.objects.create(email=request.POST['email'], choice=choice)

                            # We have problems with cheaters, so let's try out Django's SMTP functionality (check out
                            # "EMAIL_" variables in settings.py to better understand how this is configured).
                            send_mail('Validate Your Vote',
                                      'Click this link to validate your vote: http://' + request.get_host() + '/poll/' + poll_id + '/vote?validation_slug=' + vote.validation_slug + '',
                                      'noreply@mysite.com', [vote.email], fail_silently=False)

                            response = render_to_response('status.html',
                                                          {'SITE_TITLE': settings.SITE_TITLE, 'host': request.get_host(),
                                                           'heading': 'You\'re Almost There!',
                                                           'message': 'Your vote will be cast once you click the link in the email that has been sent to you.'},
                                                          context_instance=RequestContext(request))
                        # If the user is a cheater ...
                        else:
                            response = render_to_response('status.html', {'SITE_TITLE': settings.SITE_TITLE,
                                                                          'host': request.get_host(), 'heading': 'No Dice',
                                                                          'message': 'You can\'t vote more than once. Cheater.'},
                                                          context_instance=RequestContext(request))
                    
                    # If the user didn't specify a vote
                    else:
                        response = render_to_response('status.html', {'SITE_TITLE': settings.SITE_TITLE,
                                                                      'host': request.get_host(), 'heading': 'No Dice',
                                                                      'message': 'Either you\'re an indecisive voter, or you forgot to select something. Either way, we can\'t count it.'},
                                                      context_instance=RequestContext(request))
                    
                # If the user's email was invalid ...
                else:
                    response = render_to_response('status.html', {'SITE_TITLE': settings.SITE_TITLE,
                                                                  'host': request.get_host(), 'heading': 'No Dice',
                                                                  'message': 'You must enter an email address ending in ' + settings.REQUIRED_EMAIL_EXTENSION + '.'},
                                                  context_instance=RequestContext(request))
                
            # If the user did not enter an email address ...
            else:
                response = render_to_response('status.html', {'SITE_TITLE': settings.SITE_TITLE,
                                                              'host': request.get_host(), 'heading': 'No Dice',
                                                              'message': 'You must enter an email address to vote.'},
                                              context_instance=RequestContext(request))
            
        # If the user is not POSTing ...
        else:
            # If the user is validating their vote from the link emailed to them ...
            if 'validation_slug' in request.GET:
                # When a URL containing a validation_slug in the database is visited, that Vote will then
                # be officially submitted and counted in the results; this URL is what is emailed to the
                # user when they first cast their vote
                vote = Vote.objects.get(validation_slug=request.GET['validation_slug'])
                vote.accepted = True
                vote.save()

                response = render_to_response('status.html', {'SITE_TITLE': settings.SITE_TITLE,
                                                              'host': request.get_host(), 'heading': 'Tada!',
                                                              'message': 'Congratulations, your vote has been cast!'},
                                              context_instance=RequestContext(request))
            # If the user is a cheater ...
            else:
                # URLs change, your app may be deployed to multiple hosts, etc., so using Django's "reverse"
                # shortcut tells Django to handle figuring out the actual URL upon evaluation
                response = redirect(reverse('vote_id', args=[str(poll.pk)]))
    
    # The Poll ID given in the URL doesn't exist in the Database
    except Poll.DoesNotExist:
        response = render_to_response('status.html', {'SITE_TITLE': settings.SITE_TITLE, 'host': request.get_host(),
                                                      'heading': 'No Dice',
                                                      'message': 'Sorry, we couldn\'t find a poll here.'},
                                      context_instance=RequestContext(request))
    # The Choice ID given when POSTing a Vote does not exist in the database
    except Vote.DoesNotExist:
        response = render_to_response('status.html', {'SITE_TITLE': settings.SITE_TITLE,
                                                      'host': request.get_host(), 'heading': 'No Dice',
                                                      'message': 'A valid choice was not selected. Doh!'},
                                      context_instance=RequestContext(request))
    # The validation_slug does not exist for a Vote in the database
    except Vote.DoesNotExist:
        response = render_to_response('status.html', {'SITE_TITLE': settings.SITE_TITLE,
                                                      'host': request.get_host(), 'heading': 'No Dice',
                                                      'message': 'That\'s not a real validation slug, or you\'ve already voted. Stop cheating.'},
                                      context_instance=RequestContext(request))

    return response