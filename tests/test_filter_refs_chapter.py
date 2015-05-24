#!/usr/bin/env python

from __future__ import unicode_literals
import nose.tools as nose
import yv_suggest.filter_refs as yvs


def test_basic():
    """should match chapters"""
    results = yvs.get_result_list('matthew 5', prefs={})
    nose.assert_equal(len(results), 1)
    nose.assert_equal(results[0]['title'], 'Matthew 5 (NIV)')


def test_ambiguous():
    """should match chapters by ambiguous book name"""
    results = yvs.get_result_list('a 3', prefs={})
    nose.assert_equal(len(results), 2)
    nose.assert_equal(results[0]['title'], 'Amos 3 (NIV)')
    nose.assert_equal(results[1]['title'], 'Acts 3 (NIV)')


def test_id():
    """should use correct ID for chapters"""
    results = yvs.get_result_list('luke 4', prefs={})
    nose.assert_equal(results[0]['uid'], 'yvs-111/luk.4')


def test_nonexistent():
    """should not match nonexistent chapters"""
    results = yvs.get_result_list('ch 99', prefs={})
    nose.assert_equal(len(results), 2)
    nose.assert_equal(results[0]['title'], '1 Chronicles 29 (NIV)')
    nose.assert_equal(results[1]['title'], '2 Chronicles 36 (NIV)')


def test_zero_chapter():
    """should interpret chapter zero as chapter one"""
    results = yvs.get_result_list('psalm 0', prefs={})
    nose.assert_equal(len(results), 1)
    nose.assert_equal(results[0]['title'], 'Psalm 1 (NIV)')
