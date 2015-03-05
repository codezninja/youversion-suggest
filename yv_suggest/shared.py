#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import sys
import os
import os.path
import json
import re
import unicodedata
from xml.etree import ElementTree as ET

alfred_data_dir = os.path.join(os.path.expanduser('~'),
                               'Library', 'Application Support',
                               'Alfred 2', 'Workflow Data',
                               'com.calebevans.youversionsuggest')

prefs_path = os.path.join(alfred_data_dir, 'preferences.json')


def get_package_path():

    if '__file__' in globals():
        package_path = os.path.dirname(os.path.realpath(__file__))
    else:
        package_path = os.path.dirname(os.path.realpath(sys.argv[0]))

    return package_path


def get_bible_data(language):

    bible_data_path = os.path.join(get_package_path(), 'data', 'bible',
                                   'language-{}.json'.format(language))
    with open(bible_data_path, 'r') as bible_data_file:
        bible_data = json.load(bible_data_file)

    return bible_data


def get_chapter_data():

    chapter_data_path = os.path.join(get_package_path(), 'data', 'bible',
                                     'chapters.json')
    with open(chapter_data_path, 'r') as chapter_data_file:
        chapter_data = json.load(chapter_data_file)

    return chapter_data


def get_book(books, book_id):
    for book in books:
        if book['id'] == book_id:  # pragma: no cover
            return book['name']


def get_version(versions, version_id):
    for version in versions:
        if version['id'] == version_id:
            return version


def get_versions(language):

    bible = get_bible_data(language)
    return bible['versions']


def get_languages():

    languages_path = os.path.join(get_package_path(),
                                  'data', 'languages.json')
    with open(languages_path, 'r') as languages_file:
        languages = json.load(languages_file)

    return languages


def get_defaults():

    defaults_path = os.path.join(get_package_path(), 'data',
                                 'defaults.json')
    with open(defaults_path, 'r') as defaults_file:
        defaults = json.load(defaults_file)

    return defaults


def create_prefs():

    try:
        os.makedirs(alfred_data_dir, 0o755)
    except OSError:
        pass
    defaults = get_defaults()
    with open(prefs_path, 'w') as prefs_file:
        json.dump(defaults, prefs_file)

    return defaults


def get_prefs(prefs=None):

    if prefs is not None:
        if 'language' not in prefs:
            prefs = get_defaults()
    else:
        try:
            # Update existing preferences file
            with open(prefs_path, 'r') as prefs_file:
                prefs = json.load(prefs_file)
        except IOError:  # pragma: no cover
            # Otherwise, create preferences file if it doesn't exist
            prefs = create_prefs()

    return prefs


def update_prefs(prefs):

    with open(prefs_path, 'w') as prefs_file:
        json.dump(prefs, prefs_file)


def delete_prefs():
    try:
        os.remove(prefs_path)
    except OSError:
        pass


# Simplifies the format of the query string
def format_query_str(query_str):

    query_str = query_str.lower()
    # Normalize all Unicode characters
    query_str = unicodedata.normalize('NFC', query_str)
    # Remove all non-alphanumeric characters
    query_str = re.sub('[\W_]', ' ', query_str, flags=re.UNICODE)
    # Remove extra whitespace
    query_str = query_str.strip()
    query_str = re.sub('\s+', ' ', query_str)
    # Parse shorthand reference notation
    query_str = re.sub('(\d)(?=[a-z])', '\\1 ', query_str)

    return query_str


# Constructs an Alfred XML string from the given results list
def get_result_list_xml(results):

    root = ET.Element('items')

    for result in results:
        # Create <item> element for result with appropriate attributes
        item = ET.SubElement(root, 'item', {
            'uid': result['uid'],
            'arg': result.get('arg', ''),
            'valid': result.get('valid', 'yes')
        })
        # Create appropriate child elements of <item> element
        title = ET.SubElement(item, 'title')
        title.text = result['title']
        subtitle = ET.SubElement(item, 'subtitle')
        subtitle.text = result['subtitle']
        icon = ET.SubElement(item, 'icon')
        icon.text = 'icon.png'

    return ET.tostring(root)