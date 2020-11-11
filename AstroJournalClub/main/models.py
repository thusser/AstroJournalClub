from typing import List

from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Category(models.Model):
    """Category for publications."""

    name = models.CharField('Category name', max_length=20, db_index=True)

    def __str__(self):
        return self.name


class Author(models.Model):
    """Author of a publication."""

    name = models.CharField('Name of author', max_length=50, db_index=True)
    url = models.CharField('arXiv URL', max_length=100)

    def __str__(self):
        return '<a href="%s">%s</a' % (self.url, self.name)


class Vote(models.Model):
    """A vote for a publication."""

    publication = models.ForeignKey('Publication', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField('Time of vote', auto_now_add=True)


class Publication(models.Model):
    """A publication in arxiv."""

    identifier = models.CharField('arXiv identifier', max_length=10, db_index=True)
    date = models.DateField('Date of submission.')
    number = models.IntegerField('arXiv post number on day')
    title = models.CharField('Title of publication', max_length=200)
    url = models.CharField('arXiv URL', max_length=100)
    summary = models.TextField('Summary')
    categories = models.ManyToManyField(Category)

    def to_dict(self, user: User):
        # basic data
        data = {
            'identifier': self.identifier,
            'date': self.date.strftime('%Y-%m-%d'),
            'number': self.number,
            'title': self.title,
            'url': self.url,
            'summary': self.summary,
            'categories': [str(cat) for cat in self.categories.all()],
            'authors': [str(author) for author in self.authors]
        }

        # private stuff
        if user.is_authenticated:
            data['votes'] = self.vote_set.count()
            data['has_voted'] = any([user == v.user for v in self.vote_set.all()])

        # finished
        return data

    @property
    def authors(self) -> List[Author]:
        """Return list of authors in order."""

        return [pa.author for pa in PublicationAuthor.objects.filter(publication=self).order_by('order')]

    def add_author(self, order: int, author: Author):
        """Add a new author to this publication.

        Args:
            order: Order of new author in this publication.
            author: Author to add.
        """

        # get or create connection
        PublicationAuthor.objects.get_or_create(publication=self, order=order, author=author)


class PublicationAuthor(models.Model):
    """Authors for a publication."""

    publication = models.ForeignKey(Publication, on_delete=models.CASCADE, db_index=True)
    order = models.IntegerField('Order of authors in this publication.')
    author = models.ForeignKey(Author, on_delete=models.CASCADE, db_index=True)

    class Meta:
        db_table = "main_publication_authors"
