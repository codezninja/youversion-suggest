#!/usr/bin/env python

from __future__ import unicode_literals
import nose.tools as nose
import yv_suggest.copy_ref as yvs
from decorators import redirect_stdout
from mock import Mock, patch


with open('tests/files/psa.23.html') as file:
    patch_urlopen = patch(
        'yv_suggest.copy_ref.urllib2.urlopen',
        return_value=Mock(read=Mock(return_value=file.read())))


def setup():
    patch_urlopen.start()


def teardown():
    patch_urlopen.stop()


@redirect_stdout
def test_copy_chapter(out):
    '''should copy reference content for chapter'''
    yvs.main('111/psa.23')
    ref_content = out.getvalue()
    nose.assert_regexp_matches(ref_content, 'Lorem')
    nose.assert_regexp_matches(ref_content, 'nunc nulla')
    nose.assert_regexp_matches(ref_content, 'fermentum')


@redirect_stdout
def test_copy_verse(out):
    '''should copy reference content for verse'''
    yvs.main('111/psa.23.2')
    ref_content = out.getvalue()
    nose.assert_not_regexp_matches(ref_content, 'Lorem')
    nose.assert_regexp_matches(ref_content, 'nunc nulla')
    nose.assert_not_regexp_matches(ref_content, 'fermentum')


@redirect_stdout
def test_copy_verse_range(out):
    '''should copy reference content for verse range'''
    yvs.main('111/psa.23.1-2')
    ref_content = out.getvalue()
    nose.assert_regexp_matches(ref_content, 'Lorem')
    nose.assert_regexp_matches(ref_content, 'nunc nulla')
    nose.assert_not_regexp_matches(ref_content, 'fermentum')


@redirect_stdout
def test_header(out):
    '''should prepend reference header to copied string'''
    yvs.main('59/psa.23')
    ref_content = out.getvalue()
    nose.assert_regexp_matches(ref_content, '^Psalm 23 \(ESV\)')


@redirect_stdout
def test_header_language(out):
    '''reference header should reflect chosen language'''
    yvs.main('128/psa.23', prefs={
        'language': 'es'
    })
    ref_content = out.getvalue()
    nose.assert_regexp_matches(ref_content, '^Salmos 23 \(NVI\)')


@redirect_stdout
def test_charref_dec(out):
    '''should evaluate decimal character references'''
    yvs.main('111/psa.23')
    ref_content = out.getvalue().decode('utf-8')
    nose.assert_regexp_matches(ref_content, '\u201cLorem ipsum\u201d')


@redirect_stdout
def test_charref_hex(out):
    '''should evaluate hexadecimal character references'''
    yvs.main('111/psa.23')
    ref_content = out.getvalue().decode('utf-8')
    nose.assert_regexp_matches(ref_content, '\u203a Nunc sem leo')


@redirect_stdout
def test_whitespace_words(out):
    '''should handle spaces appropriately'''
    yvs.main('111/psa.23')
    ref_content = out.getvalue()
    nose.assert_regexp_matches(ref_content, 'adipiscing elit.',
                               'should respect content consisting of spaces')
    nose.assert_regexp_matches(ref_content, 'consectetur adipiscing',
                               'should collapse consecutive spaces')


@redirect_stdout
def test_whitespace_lines(out):
    '''should add line breaks where appropriate'''
    yvs.main('111/psa.23')
    ref_content = out.getvalue()
    nose.assert_regexp_matches(ref_content, 'Psalm 23 \(NIV\)\n\n\S',
                               'should add two line breaks after header')
    nose.assert_regexp_matches(ref_content, 'amet,\nconsectetur',
                               'should add newline before each p block')
    nose.assert_regexp_matches(ref_content, 'erat.\n\n\S',
                               'should add newline after each p block')
    nose.assert_regexp_matches(ref_content, 'nec\nfermentum',
                               'should add newline between each q block')
    nose.assert_regexp_matches(ref_content, 'elit.\n\nUt',
                               'should add newlines around each li1 block')
    nose.assert_regexp_matches(ref_content, 'leo,\n\nhendrerit',
                               'should add two newlines for each b block')


@redirect_stdout
def test_url_always_chapter(out):
    '''should always fetch HTML from chapter URL'''
    yvs.urllib2.urlopen.reset_mock()
    yvs.main('59/psa.23.2')
    ref_content = out.getvalue()
    yvs.urllib2.urlopen.assert_called_once_with(
        'https://www.bible.com/bible/59/psa.23')
