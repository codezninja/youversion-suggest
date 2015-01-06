#!/usr/bin/env python
import unittest
import yv_suggest as yvs

class SearchChapterTestCase(unittest.TestCase):
    '''test the searching of Bible chapters'''

    def test_search_chapter(self):
        '''should match chapters by full reference'''
        results = yvs.get_result_list('matthew 5')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, 'Matthew 5')

    def test_search_chapter_ambig(self):
        '''should match chapters by ambiguous book reference'''
        results = yvs.get_result_list('a 3')
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].title, 'Amos 3')
        self.assertEqual(results[1].title, 'Acts 3')

    def test_search_chapter_id(self):
        '''should use correct ID for chapters'''
        results = yvs.get_result_list('luke 4')
        self.assertEqual(results[0].uid, 'niv/luk.4')

    def test_search_chapter_nonexistent(self):
        '''should not match nonexistent chapters'''
        results = yvs.get_result_list('psalm 160')
        self.assertEqual(len(results), 0)

if __name__ == '__main__':
    unittest.main()
