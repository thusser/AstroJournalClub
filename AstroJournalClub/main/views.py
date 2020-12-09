from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import JsonResponse, Http404
from django.shortcuts import redirect, render
import json
import datetime
from django.urls import reverse

from AstroJournalClub.main.models import Publication, Vote, Schedule


def home(request):
    response = redirect(reverse('main:publications'))
    return response


def publications(request, year=None, month=None, day=None):
    # build date
    if year is None or month is None or day is None:
        date = datetime.date.today()
    else:
        date = datetime.date(year=year, month=month, day=day)

    # get data
    data = [pub.to_dict(request.user) for pub in Publication.objects.filter(date=date)]

    # render page
    return render(request, 'main/publications.html', context={'date': date,
                                                              'publications': json.dumps(data)})


@login_required
def vote(request, year, month, day, identifier):
    # build date
    date = datetime.datetime(year=year, month=month, day=day)

    # get publication
    pub = Publication.objects.get(date=date, identifier=identifier)

    # vote up or down?
    if any([request.user == v.user for v in pub.vote_set.all()]):
        Vote.objects.filter(publication=pub, user=request.user).delete()
    else:
        Vote.objects.get_or_create(publication=pub, user=request.user)

    # return number of votes and has_voted
    return JsonResponse(pub.extras(request.user))


@login_required
def present(request, year, month, day, identifier):
    # build date
    date = datetime.datetime(year=year, month=month, day=day)

    # get publication
    pub = Publication.objects.get(date=date, identifier=identifier)

    # vote must exist
    try:
        vote = Vote.objects.get(publication=pub, user=request.user)
    except Vote.DoesNotExist:
        raise Http404

    # present or not?
    vote.present = not vote.present
    vote.save()

    # return number of votes and has_voted
    return JsonResponse(pub.extras(request.user))


def meeting(request):
    # get start date of range
    start = datetime.datetime.utcnow() - datetime.timedelta(days=14)

    # get publications with votes on that meeting
    pubs = Publication.objects\
        .annotate(vote_count=Count('vote'))\
        .filter(vote_count__gt=0, vote__time__gt=start)

    # get publications and date of next meeting
    pubs = [pub.to_dict(request.user) for pub in pubs]
    time, _ = Schedule.all_next_meeting_time()

    # render page
    return render(request, 'main/meeting.html', context={'date': time, 'publications': json.dumps(pubs)})
