#!/usr/bin/env python
# -*- coding: utf-8 -*-

from choppy.utils import Route
from config.constants import DEBUG

ROUTES = [
    Route(r'/')                            <= 'academia.LastEntry',
    Route(r'/lookup')                      <= 'academia.Lookup',
    Route(r'/new_translation')             <= 'academia.Translation',
    Route(r'/ajax_vote')                   <= 'academia.Vote',
    Route(r'/ajax_comments')               <= 'academia.Comments',

    # twauth
    Route(r'/twitter_login')               <= 'twauth.Login',
    Route(r'/twitter_back')                <= 'twauth.Back',
    Route(r'/twitter_logout')              <= 'twauth.Logout',

    # entry
    Route(r'/<entry_id:[0-9]+>')           <= 'academia.EntryPage',
    ]

# if DEBUG
ROUTES += ([], [
    Route(r'/dev-static/<file_url:[\S]+>') <= 'core.Static',
    ])[DEBUG]
