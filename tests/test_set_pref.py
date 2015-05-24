#!/usr/bin/env python

import nose.tools as nose
import yv_suggest.set_pref as yvs
import context_managers as ctx


def test_set_language():
    """should set preferred language"""
    with ctx.use_default_prefs():
        new_language = 'es'
        yvs.main('language:{}'.format(new_language))
        prefs = yvs.shared.get_prefs()
        nose.assert_equal(prefs['language'], new_language)
        bible = yvs.shared.get_bible_data(prefs['language'])
        nose.assert_equal(prefs['version'], bible['default_version'])


def test_set_version():
    """should set preferred version"""
    with ctx.use_default_prefs():
        bible = yvs.shared.get_bible_data('en')
        new_version = 59
        yvs.main('version:{}'.format(new_version))
        prefs = yvs.shared.get_prefs()
        nose.assert_equal(prefs['version'], new_version)
