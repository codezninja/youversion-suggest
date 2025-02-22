# tests.test_compliance

import nose.tools as nose
import glob
import json
import jsonschema
import os.path
import pep8
import radon.complexity as radon


def test_pep8():
    file_paths = glob.iglob('*/*.py')
    for file_path in file_paths:
        style_guide = pep8.StyleGuide(quiet=True)
        total_errors = style_guide.input_file(file_path)
        test_pep8.__doc__ = '{} should comply with PEP 8'.format(file_path)
        fail_msg = '{} does not comply with PEP 8'.format(file_path)
        yield nose.assert_equal, total_errors, 0, fail_msg


def test_complexity():
    file_paths = glob.iglob('*/*.py')
    for file_path in file_paths:
        with open(file_path, 'r') as file:
            blocks = radon.cc_visit(file.read())
        for block in blocks:
            test_doc = '{} ({}) should have a low cyclomatic complexity score'
            test_complexity.__doc__ = test_doc.format(
                block.name, file_path)
            fail_msg = '{} ({}) has a cyclomatic complexity of {}'.format(
                block.name, file_path, block.complexity)
            yield nose.assert_less_equal, block.complexity, 10, fail_msg


def test_json():
    schemas = {
        'schema-languages': 'yvs/data/languages.json',
        'schema-defaults': 'yvs/data/defaults.json',
        'schema-chapters': 'yvs/data/bible/chapters.json',
        'schema-bible': 'yvs/data/bible/language-*.json'
    }
    for schema_name, data_path_pattern in schemas.iteritems():
        schema_path = 'yvs/data/schema/{}.json'.format(schema_name)
        with open(schema_path) as schema_file:
            schema = json.load(schema_file)
        data_paths = glob.iglob(data_path_pattern)
        for data_path in data_paths:
            with open(data_path) as data_file:
                data = json.load(data_file)
            test_json.__doc__ = '{} should comply with schema'.format(
                os.path.relpath(data_path, 'yvs/data'))
            validator = jsonschema.validate(data, schema)
            yield nose.assert_is_none, validator
