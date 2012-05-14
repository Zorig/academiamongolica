#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from config.secret_keys import SESSION_SECRET_KEY

DEBUG = os.environ.get('SERVER_SOFTWARE', '').startswith('Dev')

CONFIG = {
    'webapp2_extras.sessions': {
        'secret_key': SESSION_SECRET_KEY,
        'session_max_age': 3600 * 24 * 14, # 2 week
        'cookie_args': {
            'max_age': 3600 * 24 * 14, # 2 week
            'httponly': True
            },
        },
    }

PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
VENDOR_ROOT  = os.path.join(PROJECT_ROOT, 'vendor')
