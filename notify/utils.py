from lxml import html

from .models.configuration import Configuration


def get_tracking_configuration():
    return Configuration.get_solo().get_configuration()


def adapt_html(notify):
    tree = html.fromstring(notify)
    tree.body.append()
