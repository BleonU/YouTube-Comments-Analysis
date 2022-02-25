import urllib
from urllib.parse import urlparse


def main(url):
    url_data = urlparse(url)
    query = urllib.parse.parse_qs(url_data.query)
    return query
