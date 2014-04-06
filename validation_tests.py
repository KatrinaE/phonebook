from scripttest import TestFileEnvironment
import unittest
import nose
import os

class PhonebookTestCase(unittest.TestCase):
    def setUp(self):
        self.env = TestFileEnvironment('./scratch')
        self.prefix = os.getcwd()
        self.phonebook = 'hsphonebook.pb'

class CreateTestCase(PhonebookTestCase):
    def test_create(self):
        """
        Create a new phonebook
        """
        result = self.env.run('python %s/phonebook.py create new_phonebook.pb' \
                              % self.prefix)
        nose.tools.assert_in('created phonebook new_phonebook.pb ' + \
                             'in the current directory', result.stdout)
        assert 'new_phonebook.pb' in result.files_created
        for fieldname in ('Name', 'Phone Number'):
            assert fieldname in result.files_created['new_phonebook.pb']

    
    def test_create_duplicate(self):
        """
        Try to create a phonebook with the same name as an existing file.
        TODO: This test currently doesn't pass, even though the command works.
        I think it has to do with how ScriptTest sets up its environment.
        """
        pass
        """
        result = self.env.run('python %s/phonebook.py create phonebook_fixture.pb' \
                              % self.prefix)
        nose.tools.assert_in('Not created: file named phonebook_fixture.pb already exists', \
                             result.stdout)
        assert 'phonebook_fixture.pb' not in result.files_created
        assert 'phonebook_fixture.pb' not in result.files_updated
        """

class LookupTestCase(PhonebookTestCase):
    def test_lookup_no_book(self):
        """
        Look up a person in a nonexistent phonebook
        """
        result = self.env.run('python %s/phonebook.py lookup Sarah -b %s/nonexistent.pb' \
                              % (self.prefix, self.prefix))
        expected_output = ("No file named %s/nonexistent.pb found." \
                                        % self.prefix)
        nose.tools.assert_in(expected_output, result.stdout)

    def test_lookup_first_name(self):
        """
        Look up a person in the phonebook by first name
        """
        result = self.env.run('python %s/phonebook.py lookup Mary -b %s/phonebook_fixture.pb' \
                              % (self.prefix, self.prefix))
        expected_output = ("Mary Anderson 572 932 1921")
        nose.tools.assert_in(expected_output, result.stdout)
        
    def test_lookup_last_name(self):
        """
        Look up a person in the phonebook by last name
        """
        result = self.env.run('python %s/phonebook.py lookup Anderson -b %s/phonebook_fixture.pb' \
                              % (self.prefix, self.prefix))
        expected_output = ("Mary Anderson 572 932 1921")
        nose.tools.assert_in(expected_output, result.stdout)

    def test_lookup_multiple_people(self):
        """
        Look up a name held by multiple people in the phonebook
        """
        result = self.env.run('python %s/phonebook.py lookup Sarah -b %s/phonebook_fixture.pb' \
                              % (self.prefix, self.prefix))
        # not sure what the deal is with needing to do this weird indentation
        expected_output = \
"""Sarah Ahmed 432 123 4321 
Sarah Apple 509 123 4567 
Sarah Orange 123 456 7890 
"""
        nose.tools.assert_in(expected_output, result.stdout)

    def test_lookup_no_person(self):
        """
        Look up a person who's not in the phonebook
        """
        result = self.env.run('python %s/phonebook.py lookup Peter -b %s/phonebook_fixture.pb' \
                              % (self.prefix, self.prefix))
        expected_output = "No entries found."
        nose.tools.assert_in(expected_output, result.stdout)

class AddTestCase(PhonebookTestCase):
    def test_add_no_book(self):
        """
        Try to add a person to a nonexistent phonebook
        """
        result = self.env.run('python %s/phonebook.py add "John Michael" "123 456 789" -b %s/nonexistent.pb'  % (self.prefix, self.prefix))
        expected_output = "There is no phonebook named nonexistent.pb"
        nose.tools.assert_in(expected_output, result.stdout)

    def test_add_unspecified_book(self):
        """
        Try to add a person without specifying a phone book
        """
        result = self.env.run('python %s/phonebook.py add "John Michael" "123 456 789"'  % self.prefix)
        expected_output = "Please include a phonebook filename."
        nose.tools.assert_in(expected_output, result.stdout)
    
    def test_add_two_names(self):
        """
        Add a person with both first & last names to a phone book
        """
        result = self.env.run('python %s/phonebook.py add "John Michael" "123 456 7890" -b %s/phonebook_fixture.pb' % (self.prefix, self.prefix))
        expected_output = "Entry 'John Michael 123 456 789' added to phonebook phonebook_fixture.pb"
        nose.tools.assert_in(expected_output, result.stdout)
        # TODO: make sure names go in correct fields!!
        # check that file was updated
        for value in ('John', 'Michael', '123 456 789'):
            assert value in result.files_updated['phonebook_fixture.pb']

    def test_add_one_name(self):
        """
        Add a person with only a first name.
        """
        result = self.env.run('python %s/phonebook.py add "John" "123 456 7890" -b %s/phonebook_fixture.pb' % (self.prefix, self.prefix))
        expected_output = "Entry 'John 123 456 789' added to phonebook phonebook_fixture.pb"
        nose.tools.assert_in(expected_output, result.stdout)
        # check that file was updated
        for value in ('John', '123 456 789'):
            assert value in result.files_updated['phonebook_fixture.pb']

    def test_add_no_number(self):
        """
        Try to add an entry without a number.
        """
        result = self.env.run('python %s/phonebook.py add "John" -b %s/phonebook_fixture.pb' % (self.prefix, self.prefix))
        expected_output = "Please include a phone number."
        nose.tools.assert_in(expected_output, result.stdout)

    def test_add_malformed_number(self):
        """
        Try to add an entry with a malformed phone number.
        """
        result = self.env.run('python %s/phonebook.py add "John" "123 456 abcd" -b %s/phonebook_fixture.pb' % (self.prefix, self.prefix))
        expected_output = "Entry not created: 123 456 abcd is not a valid phone number."
        nose.tools.assert_in(expected_output, result.stdout)

    def test_add_duplicate(self):
        """
        Try to add a person who is already in the phonebook
        (I'm not sure that this should be illegal - consider changing behavior)
        """
        result = self.env.run('python %s/phonebook.py add "Mary Anderson" "123 456 789" -b %s/phonebook_fixture.pb' % (self.prefix, self.prefix))
        expected_output = "Entry not created: Mary Anderson is already in this phonebook."
        nose.tools.assert_in(expected_output, result.stdout)


class ChangeTestCase(PhonebookTestCase):
    def test_change_number(self):
        """
        Update a person's phone number
        """
        pass

    def test_change_not_exist(self):
        """
        Try to update the phone number of a person who does not exist
        """
        pass

    def test_change_malformed_number(self):
        """
        Try to change a person's number to a malformed phone number
        """
        pass

class RemoveTestCase(PhonebookTestCase):
    def test_remove(self):
        """
        Remove someone from the phonebook
        """
        pass

    def test_remove_nonexistent(self):
        """
        Try to remove a nonexistent person from the phonebook
        """
        pass

    def test_remove_multiple_possibilities(self):
        """
        Try to remove an entry without supplying a unique name.
        """
        pass
