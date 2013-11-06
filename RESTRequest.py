# -*- coding: utf-8 -*-
import requests
import json


def get_data(protocol, url):
    # TODO: get headers and query-parameters as parameters
    # feks headers: sjekk
    # http://docs.python-requests.org/en/latest/user/quickstart/#passing-parameters-in-urls
    url = protocol + '://' + url
    #headers = {'Accept': 'application/vnd.vegvesen.nvdb-v1+xml'}
    headers = {'Accept': 'text/html'}
    return requests.get(url, headers=headers, allow_redirects=False, verify=False)