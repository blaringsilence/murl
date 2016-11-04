#!/usr/bin/env python
import unittest
from mrf_murl import Murl

class TestCommonParse(unittest.TestCase):
    """Test the common parsing case: complete, absolute web URL, 
    with all the components present.
    """
    def setUp(self):
        self.murl = Murl('http://usr:pw@blog.test.com.eg'\
                    +':122/path/to/happiness?this=that#frag')

    def test_string_representation(self):
        """String representation should be = re-constructed URI."""
        self.assertEqual(str(self.murl), 'http://usr:pw@blog.test.com.eg'\
                                    +':122/path/to/happiness?this=that#frag')

    def test_scheme(self):
        self.assertEqual(self.murl.scheme, 'http')

    def test_host(self):
        self.assertEqual(self.murl.host, 'blog.test.com.eg')

    def test_domain(self):
        self.assertEqual(self.murl.domain, 'test.com.eg')

    def test_authentication(self):
        self.assertEqual(self.murl.auth, dict(username='usr', password='pw'))

    def test_username(self):
        self.assertEqual(self.murl.username, 'usr')

    def test_password(self):
        self.assertEqual(self.murl.password, 'pw')

    def test_port(self):
        self.assertEqual(self.murl.port, 122)

    def test_path(self):
        self.assertEqual(self.murl.path, 'path/to/happiness')

    def test_querystring(self):
        self.assertEqual(self.murl.queryString, '?this=that')

    def test_fragment(self):
        self.assertEqual(self.murl.fragment, 'frag')

class TestCommonCreate(unittest.TestCase):
    """Test dynamically add/change components."""
    def setUp(self):
        self.murl = Murl()

    def test_query_delimeter_default(self):
        self.assertEqual(self.murl.queryDelim, '&')

    def test_set_scheme(self):
        self.murl.scheme = 'http'
        self.assertEqual(self.murl.scheme, 'http')

    def test_fail_scheme(self):
        with self.assertRaises(ValueError):
            self.murl.scheme = '1nvalid Scheme'

    def test_set_host(self):
        self.murl.host = 'blog.test.com.eg'
        self.assertEqual(self.murl.host, 'blog.test.com.eg')

    def test_fail_host(self):
        with self.assertRaises(ValueError):
            self.murl.host = '[122:11212'

    def test_set_auth(self):
        self.murl.host = 'blog.test.com.eg' # to avoid ValueError here
        self.murl.auth = dict(username='usr', password='pw')
        self.assertEqual(self.murl.auth, dict(username='usr',\
                                            password='pw'))

    def test_fail_auth_no_host(self):
        with self.assertRaises(ValueError):
            self.murl.auth = dict(username='usr', password='pw')

    def test_fail_auth_incorrect_value(self):
        with self.assertRaises(ValueError):
            self.murl.auth = 'not_dict'

    def test_set_username_password(self):
        self.murl.host = 'blog.test.com.eg'
        self.murl.auth = dict(username='usr', password='pw')
        self.murl.username = 'usr2'
        self.murl.password = 'pw2'
        self.assertEqual(self.murl.auth, dict(username='usr2',\
                                             password='pw2'))

    def test_fail_username_no_auth(self):
        self.murl.host = 'blog.test.com.eg'
        with self.assertRaises(ValueError):
            self.murl.username = 'usr'

    def test_fail_password_no_username(self):
        self.murl.host = 'blog.test.com.eg'
        with self.assertRaises(ValueError):
            self.murl.password = 'pw'

    def test_set_port(self):
        self.murl.host = 'blog.test.com.eg'
        self.murl.port = 122
        self.assertEqual(self.murl.port, 122)

    def test_fail_port(self):
        self.murl.host = 'blog.test.com.eg'
        with self.assertRaises(ValueError):
            self.murl.port = 0
        with self.assertRaises(ValueError):
            self.murl.port = 65536

    def test_set_path(self):
        self.murl.path = 'path/to/happiness'
        self.assertEqual(self.murl.path, 'path/to/happiness')

    def test_fail_path(self):
        with self.assertRaises(ValueError):
            self.murl.path = '//not/a/path'

    def test_add_query(self):
        self.murl.addQuery('this', 'that')
        self.assertEqual(self.murl.queryString, '?this=that')
        self.assertEqual(self.murl.getQuery('this'), ['that'])

    def test_fail_query(self):
        with self.assertRaises(KeyError):
            self.murl.getQuery('this')

    def test_change_query_all(self):
        self.murl.addQuery('this', 'that')
        self.murl.addQuery('this', 'those')
        self.murl.changeQuery('this', 'all')
        self.assertEqual(self.murl.getQuery('this'), ['all'])

    def test_change_query_one(self):
        self.murl.addQuery('this', 'that')
        self.murl.addQuery('this', 'those')
        self.murl.changeQuery('this', 'one', 'those')
        self.assertEqual(self.murl.getQuery('this'), ['that', 'one'])

    def test_remove_query_all(self):
        self.murl.addQuery('this', 'that')
        self.murl.addQuery('this', 'those')
        self.murl.removeQuery('this')
        with self.assertRaises(KeyError):
            deleted_query = self.murl.getQuery('this')

    def test_remove_query_one(self):
        self.murl.addQuery('this', 'that')
        self.murl.addQuery('this', 'those')
        self.murl.removeQuery('this', 'those')
        self.assertEqual(self.murl.getQuery('this'), ['that'])

    def test_set_fragment(self):
        self.murl.fragment = 'frag'
        self.assertEqual(self.murl.fragment, 'frag')

class TestCornerCases(unittest.TestCase):
    """Test the corner case uses."""
    def test_parse_relative_url(self):
        murl = Murl('../path/to/happiness?this=that#frag')
        self.assertEqual(murl.path, '../path/to/happiness') 
        self.assertEqual(murl.fragment, 'frag')
        self.assertEqual(murl.getQuery('this'), ['that'])
        self.assertEqual(murl.scheme, None)

    def test_parse_urn(self):
        murl = Murl('urn:example:mammal:monotreme:echidna')
        self.assertEqual(murl.scheme, 'urn')
        self.assertEqual(murl.path, 'example:mammal:monotreme:echidna')

    def test_create_with_different_delimeter(self):
        murl = Murl('http://test.com', queryDelim=';')
        murl.addQuery('this', 'that')
        murl.addQuery('this', 'those')
        self.assertIs(murl.queryString == '?this=that;this=those'\
                     or murl.queryString == '?this=those;this=that', True)

    def test_unencoded_auth(self):
        murl = Murl('http://test.com')
        murl.auth = dict(username='dave@david', password='&unsafe')
        self.assertEqual(murl.username, 'dave@david') 
        self.assertEqual(murl.password, '&unsafe')
        self.assertEqual(str(murl), 'http://dave%40david:%26unsafe@test.com')

    def test_unencoded_query(self):
        murl = Murl('http://test.com')
        murl.addQuery('hello&', 'world;')
        self.assertEqual(murl.getQuery('hello&'), ['world;'])
        self.assertEqual(str(murl), 'http://test.com?hello%26=world%3B')

    def test_encoded_query(self):
        murl = Murl('http://test.com')
        murl.addQuery('hello%26', 'world%3B')
        self.assertEqual(murl.getQuery('hello&'), ['world;'])
        self.assertEqual(murl.getQuery('hello%26'), ['world;'])
        self.assertEqual(str(murl), 'http://test.com?hello%26=world%3B')

    def test_unencoded_fragment(self):
        murl = Murl('http://test.com')
        murl.fragment = 'haha lol'
        self.assertEqual(murl.fragment, 'haha lol')
        self.assertEqual(str(murl), 'http://test.com#haha%20lol')

    def test_encoded_fragment(self):
        murl = Murl('http://test.com')
        murl.fragment = 'haha%20lol'
        self.assertEqual(murl.fragment, 'haha lol')
        self.assertEqual(str(murl), 'http://test.com#haha%20lol')

    def test_unencoded_path(self):
        murl = Murl('http://test.com')
        murl.path = 'path/to /happiness'
        self.assertEqual(str(murl), 'http://test.com/path/to%20/happiness')
        self.assertEqual(murl.path, 'path/to%20/happiness')

    def test_encoded_path(self):
        murl = Murl('http://test.com')
        murl.path = 'path/to%20/happiness'
        self.assertEqual(str(murl), 'http://test.com/path/to%20/happiness')
        self.assertEqual(murl.path, 'path/to%20/happiness')



if __name__ == "__main__":
    unittest.main()

