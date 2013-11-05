# -*- coding: utf-8 -*-
import requests


def get_data():
    # TODO: get headers and query-parameters as parameters
    # feks headers: sjekk
    # http://docs.python-requests.org/en/latest/user/quickstart/#passing-parameters-in-urls
    return requests.get('http://example.com').content