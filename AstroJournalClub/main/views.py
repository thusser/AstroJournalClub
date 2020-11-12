from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import redirect, render
import json
from datetime import datetime, date, time, timedelta
from django.urls import reverse

from AstroJournalClub.main.models import Publication, Vote, Schedule, Meeting


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


def next_meeting(request):
    # get next meeting time
    dt_next, _ = Schedule.all_next_meeting_time()

    # got one?
    data = []
    if dt_next is not None:
        # query publications
        pubs = Publication.objects.annotate(vote_count=Count('vote')).filter(vote_count__gt=0)

        # get date of last meeting
        last_meeting = Meeting.objects.order_by('-time').first()
        if last_meeting is not None:
            pubs.filter(date__gt=last_meeting.time)

        # get data
        data = [pub.to_dict(request.user) for pub in pubs]

    # render page
    return render(request, 'main/next.html', context={'date': dt_next, 'publications': json.dumps(data)})
