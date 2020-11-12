from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import redirect, render
import json
import datetime
from django.urls import reverse

from AstroJournalClub.main.models import Publication, Vote, Schedule, Meeting


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
    return render(request, 'main/publications.html', context={'date': date, 'publications': json.dumps(data)})


@login_required
def vote(request, year, month, day, identifier):
    # build date
    date = datetime.datetime(year=year, month=month, day=day)

    # get publication
    pub = Publication.objects.get(date=date, identifier=identifier)

    # get next meeting
    meeting = Schedule.all_next_meeting()

    # got any?
    if meeting is not None:
        # vote up or down?
        if any([request.user == v.user for v in pub.vote_set.all()]):
            Vote.objects.filter(publication=pub, user=request.user, meeting=meeting).delete()
        else:
            Vote.objects.get_or_create(publication=pub, user=request.user, meeting=meeting)

    # return number of votes and has_voted
    return JsonResponse({'votes': pub.vote_set.count(),
                         'has_voted': any([request.user == v.user for v in pub.vote_set.all()])})


def meetings(request, year: int = None, month: int = None, day: int = None):
    # build date
    if year is None or month is None or day is None:
        date = Schedule.all_next_meeting_time()[0].date()
    else:
        date = datetime.date(year=year, month=month, day=day)

    # get meetings on given date
    start = datetime.datetime.combine(date, datetime.time(hour=0, minute=0, second=0))
    end = datetime.datetime.combine(date, datetime.time(hour=23, minute=59, second=59))

    # we just assume to have only one meeting per day
    meeting = Meeting.objects.filter(time__gte=start, time__lte=end).first()

    # got a meeting?
    if meeting is None:
        date = None
        publications = []

    else:

        # get publications with votes on that meeting
        pubs = Publication.objects\
            .annotate(vote_count=Count('vote'))\
            .filter(vote_count__gt=0, vote__meeting=meeting)

        # store
        publications = [pub.to_dict(request.user) for pub in pubs]
        date = meeting.time

    # render page
    return render(request, 'main/meetings.html', context={'date': date, 'publications': json.dumps(publications)})
