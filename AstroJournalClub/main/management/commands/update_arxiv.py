from django.core.management.base import BaseCommand
import feedparser
import re
from lxml import html
from AstroJournalClub.main import models
from datetime import datetime


class Command(BaseCommand):
    help = 'Update from arxiv.org'

    #def add_arguments(self, parser):
    #    parser.add_argument('files', type=str, nargs='+', help='Names of files to ingest')

    def handle(self, *args, **options):
        # get and parse RSS feed
        feed = feedparser.parse('http://export.arxiv.org/rss/astro-ph/')

        # loop all entries
        for number, entry in enumerate(feed['entries'], 1):
            # extract identifier, title and summary
            identifier = entry.id[entry.id.rfind('/') + 1:]
            title = entry.title[:entry.title.find('(arXiv:')]

            # get/create publication
            date = datetime.now()
            publication, _ = models.Publication.objects.get_or_create(identifier=identifier, date=date,
                                                                      defaults={'title': title, 'number': number,
                                                                                'url': entry.link,
                                                                                'summary': entry.summary})

            # add category
            category_name = entry.title[entry.title.rfind('[') + 1:entry.title.rfind(']')]
            category, _ = models.Category.objects.get_or_create(name=category_name)
            publication.categories.add(category)
            publication.save()

            # extract authors
            tree = html.fromstring(entry.author)
            for a in tree.xpath('//a'):
                author, _ = models.Author.objects.get_or_create(name=a.text, defaults={'url': a.get('href')})
                publication.authors.add(author)
