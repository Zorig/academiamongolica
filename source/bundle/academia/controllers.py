#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tweepy
import random

from choppy.handler import BaseRequestHandler as BaseHandler

from config.secret_keys import TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET

from bundle.academia import models
from bundle.academia.utils import shorten_url


class LastEntry(BaseHandler):
    def get(self, *args, **kwargs):
        """
        redirect to last entry url
        """
        # initial data
        if models.Entry.all().count() == 0:
            models.Entry(
                entry='mongolia',
                description='The country we love!',
                user='dagvadorj'
                ).put()

        # get entry
        entry = models.Entry.all().order('-when').get()

        return self.redirect('/' + str(entry.key().id()))


class EntryPage(BaseHandler):
    def get(self, entry_id):
        self.context['entry'] = entry = models.Entry.get_by_id(int(entry_id))

        if entry is None:
            return self.redirect('/')

        self.context['new_entries'] = models.Entry.all().order('-when').fetch(10)
        self.context['translations'] = models.Translation.all().filter('entry =', entry).order('-vote')
        self.context['activity_list'] = self.get_activity_list()

        self.context['user'] = self.session.get('twitter_user', None)
        self.context['title'] = entry.entry

        return self.render('index.html')

    def post(self, entry_id):
        query = self.request.get('lookup')
        entry = models.Entry.all().filter('entry =', query).get()

        if entry is None:
            return self.redirect('/')

        return self.redirect('/%s' % entry.key().id())

    def get_activity_list(self, count=10):
        ret = []
        data = []

        for item in list(models.Translation.all().order('-when').fetch(count)):
            data += [{
                'action': 'translation',
                'user': item.user,
                'when': item.when,
                'translation': item.translation,
                'entry': item.entry.entry,
                'entry_id': item.entry.key().id(),
                }]

        for item in list(models.Vote.all().order('-when').fetch(count)):
            data += [{
                'action': 'vote' + ('-1', '+1')[item.type == 1],
                'user': item.user,
                'when': item.when,
                'translation': item.translation.translation,
                'entry': item.translation.entry.entry,
                'entry_id': item.translation.entry.key().id(),
                }]

        for item in list(models.Comment.all().order('-when').fetch(count)):
            data += [{
                'action': 'comment',
                'user': item.user,
                'when': item.when,
                'translation': item.translation.translation,
                'entry': item.translation.entry.entry,
                'entry_id': item.translation.entry.key().id(),
                }]

        ret = sorted(data, key=lambda k: k['when'])
        ret.reverse()

        return ret[:count]


class Lookup(BaseHandler):
    def get(self):
        query = self.request.get('query')
        entries = models.Entry.all().filter('entry >=', query).filter('entry <', query + u'\ufffd').fetch(10)
        json = '{"query": "%s", "suggestions": [' % query
        for entry in entries:
            json += '"%s",' % entry.entry
        json = json[:-1] # removing last comma
        json += ']}'
        return self.response.out.write(json)


class Translation(BaseHandler):
    def post(self):
        # require user
        if not 'twitter_user' in self.session:
            return self.redirect('/')

        entry_id = self.request.get('entry_id')
        entry = models.Entry.get_by_id(int(entry_id))

        models.Translation(
            entry=entry,
            translation=self.request.get('translation').replace('\n', ' '),
            user=self.session['twitter_user']
            ).put()

        if not self.request.get('tweet').lower() in ['yes', '1']:
            return self.redirect('/%s' % entry.key().id())

        # tweet this!
        auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
        auth.set_access_token(self.session['twitter_token_key'], self.session['twitter_token_secret'])
        api = tweepy.API(auth)

        translation = self.request.get('translation').replace('\n', ' ')
        short_url = shorten_url('http://academiamongolica.appspot.com/%s' % entry_id)

        tweet_templates = [
            u'"%s"-г "%s" гэж орчуулбал зүгээр юм биш үү? #en2mn %s',
            u'Би #academiamongolica-д "%s - %s" гэсэн орчуулга орууллаа #en2mn %s',
            u'"%s"-г Монголоор "%s" гэж хэлбэл гоё юм биш үү? #en2mn %s',
            u'"%s" гэдэг чинь Монголоор "%s" гэсэн үг биз дээ. #en2mn %s',
            u'AcademiaMongolica-д оруулсан миний хувь нэмэр: "%s - %s" #en2mn %s',
            ]

        tweet = random.choice(tweet_templates) % (entry.entry, translation, short_url)
        api.update_status(tweet)

        return self.redirect('/%s' % entry.key().id())


class Vote(BaseHandler):
    def post(self):
        if not 'twitter_user' in self.session:
            return self.response.out.write('{"info":"NOTLOGGEDIN"}')

        translation_id = int(self.request.get('translation_id'))
        val = 1 if self.request.get('val') == '1' else -1

        translation = models.Translation.get_by_id(translation_id)
        votes = models.Vote.all().filter('translation =', translation).filter('user =', self.session['twitter_user'])

        if votes.count() == 0:
            models.Vote(
                user=self.session['twitter_user'],
                type=val,
                translation=translation).put()
            translation.vote += val
            translation.put()
        else:
            vote = votes[0]
            if val == vote.type:
                return self.response.out.write('{"info":"DUPLICATE"}')
            else:
                vote.type = val
                vote.put()
                translation.vote += 2 * val
                translation.put()

        return self.response.out.write('{"info":"SUCCESS","translation_id":"%s","vote":"%s"}' % (translation.key().id(), translation.vote))


class Comments(BaseHandler):
    def get(self):
        try:
            translation_id = int(self.request.get('translation_id'))
        except ValueError:
            return self.redirect('/')

        self.context['translation'] = translation = models.Translation.get_by_id(translation_id)
        self.context['comments'] = models.Comment.all().filter('translation =', translation).order('-when')
        self.context['user'] = self.session.get('twitter_user', None)

        return self.render('comments.html')

    def post(self):
        if not 'twitter_user' in self.session:
            return self.redirect('/')

        try:
            translation_id = int(self.request.get('translation_id'))
        except ValueError:
            return self.redirect('/')

        translation = models.Translation.get_by_id(translation_id)
        comment = self.request.get('comment').replace('\n', ' ')

        models.Comment(
            user=self.session['twitter_user'],
            comment=comment,
            translation=translation).put()

        return self.redirect('/ajax_comments?translation_id=%s' % translation_id)
