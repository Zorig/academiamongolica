#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tweepy

from choppy.handler import BaseRequestHandler as BaseHandler

from config.secret_keys import TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET

from bundle.twauth import models


class Login(BaseHandler):
    def get(self):
        auth = tweepy.OAuthHandler(
            TWITTER_CONSUMER_KEY,
            TWITTER_CONSUMER_SECRET,
            self.request.host_url + '/twitter_back')

        url = auth.get_authorization_url()

        models.OAuthToken(
            token_key=auth.request_token.key,
            token_secret=auth.request_token.secret).put()

        return self.redirect(url)


class Logout(BaseHandler):
    def get(self):
        del self.session['twitter_user']
        del self.session['twitter_token_key']
        del self.session['twitter_token_secret']

        return self.redirect('/')


class Back(BaseHandler):
    def get(self):
        oauth_token = self.request.get('oauth_token', None)
        oauth_verifier = self.request.get('oauth_verifier', None)

        request_token = models.OAuthToken.gql("WHERE token_key=:key", key=oauth_token).get()

        if request_token is None:
            return self.response.write('Invalid token')

        auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
        auth.set_request_token(request_token.token_key, request_token.token_secret)
        auth.get_access_token(oauth_verifier)
        api = tweepy.API(auth)

        self.session['twitter_user'] = api.me().screen_name
        self.session['twitter_token_key'] = auth.access_token.key
        self.session['twitter_token_secret'] = auth.access_token.secret

        return self.redirect('/')
