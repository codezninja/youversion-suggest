#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import nose.tools as nose
import yv_suggest.filter_refs as yvs


def test_empty():
    """should not match empty input"""
    results = yvs.get_result_list('', prefs={})
    nose.assert_equal(len(results), 0)


def test_invalid():
    """should not match invalid input"""
    results = yvs.get_result_list('!!!', prefs={})
    nose.assert_equal(len(results), 0)


def test_invalid_xml():
    """should not match input containing XML reserved characters"""
    results = yvs.get_result_list('<&>', prefs={})
    nose.assert_equal(len(results), 0)