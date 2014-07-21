from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.core.mail import send_mail
from django.conf import settings

from djangopolls.models import Poll, Choice, Vote


def home(request):
    open_polls = Poll.objects.filter(close_date=None).exclude(open_date=None)
    closed_polls = Poll.objects.exclude(close_date=None)

    response = render_to_response('home.html',
                                  {'SITE_TITLE': settings.SITE_TITLE, 'host': request.get_host(),
                                   'open_polls': open_polls, 'closed_polls': closed_polls},
                                  context_instance=RequestContext(request))

    return response


def poll(request, poll_id):
    try:
        poll = Poll.objects.exclude(open_date=None).get(pk=poll_id)
        choices = Choice.objects.filter(poll=poll)

        if poll.close_date != None or (
                        request.user.is_authenticated() and request.user.is_superuser and 'results' in request.GET):
            votes = Vote.objects.filter(validation_slug='').all()
            vote_counts = {}
            vote_percentages = {}
            for choice in choices:
                vote_count = Vote.objects.filter(choice=choice, validation_slug='').count()
                vote_counts[choice.pk] = vote_count
                vote_percentages[choice.pk] = (float(vote_count) / float(
                    votes.count())) * 100 if vote_count > 0 else 0

            response = render_to_response('poll_results.html',
                                          {'SITE_TITLE': settings.SITE_TITLE, 'host': request.get_host(), 'poll': poll,
                                           'choices': choices, 'votes': votes, 'vote_counts': vote_counts,
                                           'vote_percentages': vote_percentages},
                                          context_instance=RequestContext(request))
        else:
            if choices.count() > 0:
                response = render_to_response('poll_open.html',
                                              {'SITE_TITLE': settings.SITE_TITLE, 'host': request.get_host(),
                                               'poll': poll, 'choices': choices},
                                              context_instance=RequestContext(request))
            else:
                response = render_to_response('status.html', {'SITE_TITLE': settings.SITE_TITLE,
                                                              'host': request.get_host(), 'heading': 'No Dice',
                                                              'message': 'Looks like the poll creator hasn\'t made any choices yet for this poll.'},
                                              context_instance=RequestContext(request))
    except Poll.DoesNotExist:
        response = render_to_response('status.html', {'SITE_TITLE': settings.SITE_TITLE, 'host': request.get_host(),
                                                      'heading': 'No Dice',
                                                      'message': 'Sorry, we couldn\'t find a poll here. Maybe it\'s not open yet?'},
                                      context_instance=RequestContext(request))

    return response


def vote(request, poll_id):
    try:
        poll = Poll.objects.exclude(open_date=None).get(pk=poll_id)

        if request.method == 'POST':
            if 'email' in request.POST:
                if not settings.REQUIRED_EMAIL_EXTENSION or settings.REQUIRED_EMAIL_EXTENSION in request.POST['email']:
                    if 'choice' in request.POST:
                        choice = Choice.objects.get(pk=request.POST['choice'])
                        if Vote.objects.filter(email=request.POST['email'], choice__poll=poll).count() == 0:
                            vote = Vote.objects.create(email=request.POST['email'], choice=choice)

                            send_mail('Validate Your Vote',
                                      'Click this link to validate your vote: http://' + request.get_host() + '/poll/' + poll_id + '/vote?validation_slug=' + vote.validation_slug + '',
                                      'noreply@mysite.com', [vote.email], fail_silently=False)

                            response = render_to_response('status.html',
                                                          {'SITE_TITLE': settings.SITE_TITLE, 'host': request.get_host(),
                                                           'heading': 'You\'re Almost There!',
                                                           'message': 'Your vote will be cast once you click the link in the email that has been sent to you.'},
                                                          context_instance=RequestContext(request))
                        else:
                            response = render_to_response('status.html', {'SITE_TITLE': settings.SITE_TITLE,
                                                                          'host': request.get_host(), 'heading': 'No Dice',
                                                                          'message': 'You can\'t vote more than once. Cheater.'},
                                                          context_instance=RequestContext(request))
                    else:
                        response = render_to_response('status.html', {'SITE_TITLE': settings.SITE_TITLE,
                                                                      'host': request.get_host(), 'heading': 'No Dice',
                                                                      'message': 'Either you\'re an indecisive voter, or you forgot to select something. Either way, we can\'t count it.'},
                                                      context_instance=RequestContext(request))
                else:
                    response = render_to_response('status.html', {'SITE_TITLE': settings.SITE_TITLE,
                                                                  'host': request.get_host(), 'heading': 'No Dice',
                                                                  'message': 'You must enter an email address ending in ' + settings.REQUIRED_EMAIL_EXTENSION + '.'},
                                                  context_instance=RequestContext(request))
            else:
                response = render_to_response('status.html', {'SITE_TITLE': settings.SITE_TITLE,
                                                              'host': request.get_host(), 'heading': 'No Dice',
                                                              'message': 'You must enter an email address to vote.'},
                                              context_instance=RequestContext(request))
        else:
            if 'validation_slug' in request.GET:
                try:
                    vote = Vote.objects.get(validation_slug=request.GET['validation_slug'])
                    vote.validation_slug = ''
                    vote.save()

                    response = render_to_response('status.html', {'SITE_TITLE': settings.SITE_TITLE,
                                                                  'host': request.get_host(), 'heading': 'Tada!',
                                                                  'message': 'Congratulations, your vote has been cast!'},
                                                  context_instance=RequestContext(request))
                except Vote.DoesNotExist:
                    response = render_to_response('status.html', {'SITE_TITLE': settings.SITE_TITLE,
                                                                  'host': request.get_host(), 'heading': 'No Dice',
                                                                  'message': 'That\'s not a real validation slug, or you\'ve already voted. Stop cheating.'},
                                                  context_instance=RequestContext(request))
            else:
                choices = Choice.objects.filter(poll=poll)
                response = redirect('http://' + request.get_host() + '/poll/' + str(poll.pk))
    except Poll.DoesNotExist:
        response = render_to_response('status.html', {'SITE_TITLE': settings.SITE_TITLE, 'host': request.get_host(),
                                                      'heading': 'No Dice',
                                                      'message': 'Sorry, we couldn\'t find a poll here.'},
                                      context_instance=RequestContext(request))

    return response