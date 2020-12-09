from django import template
from AstroJournalClub.version import VERSION

register = template.Library()


@register.simple_tag
def version():
    return VERSION
