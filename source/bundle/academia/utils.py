#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from google.appengine.api import urlfetch

from config.secret_keys import BITLY_LOGIN, BITLY_API_KEY


class BitLy():
    def __init__(self, login, apikey):
        self.login = login
        self.apikey = apikey

    def shorten(self, param):
        # url = "http://" + param
        request = "http://api.bit.ly/shorten?version=2.0.1&longUrl="
        request += param
        request += "&login=" + self.login + "&apiKey=" + self.apikey

        result = urlfetch.fetch(request)
        json_data = json.loads(result.content)
        return json_data


def shorten_url(url):
    bitly = BitLy(BITLY_LOGIN, BITLY_API_KEY)
    return bitly.shorten(url)['results'][url]['shortUrl']
