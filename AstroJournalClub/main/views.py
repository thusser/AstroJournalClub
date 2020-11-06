from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import redirect, render
import json
from datetime import datetime, date, time, timedelta
from django.urls import reverse

from AstroJournalClub.main.models import Publication, Vote


def home(request):
    now = datetime.now()
    response = redirect(reverse('main:publications', args=(now.year, now.month, now.day)))
    return response


def publications(request, year, month, day):
    # build date
    date = datetime(year=year, month=month, day=day)

    # get data
    data = [pub.to_dict(request.user) for pub in Publication.objects.filter(date=date)]

    # render page
    return render(request, 'main/home.html', context={'date': date, 'publications': json.dumps(data)})


@login_required
def vote(request, year, month, day, identifier):
    # build date
    date = datetime(year=year, month=month, day=day)

    # get publication
    pub = Publication.objects.get(date=date, identifier=identifier)

    # vote up or down?
    if any([request.user == v.user for v in pub.vote_set.all()]):
        Vote.objects.filter(publication=pub, user=request.user).delete()
    else:
        Vote.objects.get_or_create(publication=pub, user=request.user)

    # return number of votes and has_voted
    return JsonResponse({'votes': pub.vote_set.count(),
                         'has_voted': any([request.user == v.user for v in pub.vote_set.all()])})


def next_meeting(request):
    # hardcoded for now
    meet_day = 2
    start = time(hour=13, minute=30, second=00)
    end = time(hour=14, minute=00, second=00)

    # get end of last meeting
    now = datetime.now()
    if now.weekday() == meet_day:
        # today is meeting!
        if now.time() < end:
            # before meeting, take last 7 days
            last_meeting_day = now.date() - timedelta(days=7)
        else:
            # after meeting, start today
            last_meeting_day = now.date()
    else:
        # go back in time until meeting day
        last_meeting_day = now.date()
        while last_meeting_day.weekday() != meet_day:
            last_meeting_day -= timedelta(days=1)
    last_meeting = datetime.combine(last_meeting_day, end)

    # get data
    data = [pub.to_dict(request.user) for pub in Publication.objects.annotate(vote_count=Count('vote')).filter(date__gt=last_meeting, vote_count__gt=0)]

    # render page
    return render(request, 'main/home.html', context={'date': now, 'publications': json.dumps(data)})
