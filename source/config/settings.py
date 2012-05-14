#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fdm=marker

# BUNDLEWARES {{{1
BUNDLEWARES = [
    # vendor bundles
    'vendor.choppy.bundle.core',

    # bundle
    'bundle.academia',
    'bundle.twauth',
    ]

# MIDDLEWARES {{{1
MIDDLEWARES = [
    ]

# BOOTWARES {{{1
BOOTWARES = [
    'vendor.choppy.bundle.core.bootware.core_bootware',
    ]

# JINJA2_CONFIG {{{1
JINJA2_CONFIG = {}
JINJA2_CONFIG['environment_args'] = {
    'autoescape': True,
    'extensions': [
        'jinja2.ext.autoescape',
        'jinja2.ext.with_',
        ],
    }

# extra settings {{{1
STATIC_URL = '/static'
