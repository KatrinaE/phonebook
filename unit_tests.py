import os
import sys
from unittest import TestCase
import nose.tools

from phonebook import Phonebook
from phonebook import create_parser, instantiate_phonebook, load_phonebook, \
    perform_phonebook_action


class PhonebookTestCase(TestCase):
    """
    (Thanks to http://dustinrcollins.com/testing-python-command-line-apps)
    """
    @classmethod
    def setUp(cls):
        parser = create_parser()
        cls.parser = parser

        phonebook_fixture = load_phonebook('phonebook_fixture.pb')
    
    def tearDown(cls):
        try:
            os.remove('new-phonebook.csv')
        except:
            # new-phonebook.csv not created
            pass

class PhonebookTestCase(PhonebookTestCase):
    def test_create(self):
        """
        Correctly create a phonebook
        """
        args = self.parser.parse_args(['create', 'new-phonebook.csv'])
        phonebook = instantiate_phonebook(args)
        nose.tools.assert_equal(phonebook.filename, 'new-phonebook.csv')
        nose.tools.assert_equal(phonebook.people, [])
        perform_phonebook_action(args)
        phonebook_file = open('new-phonebook.csv')

class LookupTestCase(PhonebookTestCase):
    pass
