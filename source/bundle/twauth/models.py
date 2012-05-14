#!/usr/bin/env python
# -*- coding: utf-8 -*-

from google.appengine.ext import db


class OAuthToken(db.Model):
    token_key = db.StringProperty(required=True)
    token_secret = db.StringProperty(required=True)
