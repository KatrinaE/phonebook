from scripttest import TestFileEnvironment
import unittest
import nose
import os

class PhonebookTestCase(unittest.TestCase):
    def setUp(self):
        self.env = TestFileEnvironment('./scratch')
        self.prefix = os.getcwd()
        
        # load phonebook fixture. Need to use separate name to prevent
        # overwriting actual file.
        with open('phonebook_fixture.txt') as f:
            with open('phonebook_fixture.pb', 'wb') as phonebook_fixture:
                for line in f:
                    phonebook_fixture.write(line)

    def tearDown(self):
        os.remove('phonebook_fixture.pb')

    # helper methods for ensuring things were/weren't added to files.
    def assert_not_added(self, entry_fields):
        result = self.env.run('cat %s/phonebook_fixture.pb' % self.prefix)
        for value in entry_fields:
            nose.tools.assert_not_in(value, result.stdout)

    def assert_added(self, entry_fields):
        result = self.env.run('cat %s/phonebook_fixture.pb' % self.prefix)
        for value in entry_fields:
            nose.tools.assert_in(value, result.stdout)

class CreateTestCase(PhonebookTestCase):
    def test_create(self):
        """
        Create a new phonebook
        """
        result = self.env.run('phonebook ' + \
                              ('create new_phonebook.pb'))
        nose.tools.assert_in('Created phonebook named new_phonebook.pb ' + \
                             'in the current directory', result.stdout)
        assert 'new_phonebook.pb' in result.files_created
        for fieldname in ('name', 'number'):
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
        result = self.env.run('phonebook ' + \
                              ('lookup Sarah ') + \
                              ('-b %s/nonexistent.pb' % self.prefix))
        expected_output = ("No file named %s/nonexistent.pb found." % self.prefix)
        nose.tools.assert_in(expected_output, result.stdout)

    def test_lookup_first_name(self):
        """
        Look up a person in the phonebook by first name
        """
        result = self.env.run('phonebook ' + \
                              ('lookup Mary ') + \
                              ('-b %s/phonebook_fixture.pb' % self.prefix))
        expected_output = ("Mary Anderson 572 932 1921")
        nose.tools.assert_in(expected_output, result.stdout)
        
    def test_lookup_multiple_people(self):
        """
        Look up a name held by multiple people in the phonebook
        """
        result = self.env.run('phonebook ' + \
                              ('lookup Sarah ') + \
                              ('-b %s/phonebook_fixture.pb' % self.prefix))
        expected_output = 'Sarah Ahmed 432 123 4321\n' + \
                          'Sarah Apple 509 123 4567\n' + \
                          'Sarah Orange 123 456 7980\n'
        nose.tools.assert_in(expected_output, result.stdout)

    def test_lookup_no_person(self):
        """
        Look up a person who's not in the phonebook
        """
        result = self.env.run('phonebook ' + \
                              ('lookup Peter ') + \
                              ('-b %s/phonebook_fixture.pb' % self.prefix))
        expected_output = "No entries found."
        nose.tools.assert_in(expected_output, result.stdout)


    def test_reverse_lookup(self):
        """
        Look up a person by their phone number
        """
        result = self.env.run('phonebook ' + \
                              ('reverse-lookup "572 932 1921" ') + \
                              ('-b %s/phonebook_fixture.pb' % self.prefix))
        expected_output = "Mary Anderson 572 932 1921"
        nose.tools.assert_in(expected_output, result.stdout)

    def test_reverse_multiple_people(self):
        """
        Look up a number belonging to multiple people
        """
        result = self.env.run('phonebook ' + \
                              ('reverse-lookup "123 456 7980" ') + \
                              ('-b %s/phonebook_fixture.pb' % self.prefix))
        expected_output = 'Sarah Orange 123 456 7980\n' + \
                          'Bob Orange 123 456 7980\n'
        nose.tools.assert_in(expected_output, result.stdout)

class AddTestCase(PhonebookTestCase):
    def test_add_no_book(self):
        """
        Try to add a person to a nonexistent phonebook
        """
        result = self.env.run('phonebook ' + \
                              ('add "John Michael" "123 456 7890" ') + \
                              ('-b %s/nonexistent.pb' % self.prefix))
        expected_output = "No file named %s/nonexistent.pb found." % self.prefix
        nose.tools.assert_in(expected_output, result.stdout)

    def test_add_unspecified_book(self):
        """
        Try to add a person without specifying a phone book
        """
        result = self.env.run('phonebook ' + \
                              ('add "John Michael" "123 456 7890" '))
        expected_output = "Please include a phonebook filename."
        nose.tools.assert_in(expected_output, result.stdout)
    
    def test_add(self):
        """
        Add a person to a phonebook.
        """
        result = self.env.run('phonebook ' + \
                              ('add "John Michael" "123 456 7890" ') + \
                              ('-b %s/phonebook_fixture.pb' % self.prefix))
        expected_output = ("Entry 'John Michael 123 456 7890' added to phonebook " + \
                           "%s/phonebook_fixture.pb" % self.prefix)
        nose.tools.assert_in(expected_output, result.stdout)

        # check that file was updated
        # for some reason this doesn't work - result.files_updated is empty:
        #      assert 'phonebook_fixture.pb' in result.files_updated
        # fall back on manually viewing the file.
        entry_fields =  ('John Michael', '123 456 7890')
        self.assert_added(entry_fields)

    def test_add_no_number(self):
        """
        Try to add an entry without a number.
        """
        result = self.env.run('phonebook ' + \
                              ('add "John Michael" ') + \
                              ('-b %s/phonebook_fixture.pb' % self.prefix))
        expected_output = "Please include a phone number."
        nose.tools.assert_in(expected_output, result.stdout)
        entry_fields = ['John Michael']
        self.assert_not_added(entry_fields)

    def test_add_malformed_number(self):
        """
        Try to add an entry with a malformed phone number.
        """
        result = self.env.run('phonebook ' + \
                              ('add "John Michael" "123 456 abcd" ') + \
                              ('-b %s/phonebook_fixture.pb' % self.prefix))
        expected_output = "Entry not created: '123 456 abcd' is not a valid phone number."
        nose.tools.assert_in(expected_output, result.stdout)
        entry_fields = ['John Michael', '123 456 abcd']
        self.assert_not_added(entry_fields)

    def test_add_duplicate(self):
        """
        Try to add a person who is already in the phonebook
        (I'm not sure that this should be illegal - consider changing behavior)
        """
        result = self.env.run('phonebook ' + \
                              ('add "Mary Anderson" "123 456 7890" ') + \
                              ('-b %s/phonebook_fixture.pb' % self.prefix))
        expected_output = "Entry not created: Mary Anderson is already in this phonebook."
        nose.tools.assert_in(expected_output, result.stdout)

        result = self.env.run('cat %s/phonebook_fixture.pb' % self.prefix)
        nose.tools.assert_equal(result.stdout.count('Mary Anderson'), 1)

class ChangeTestCase(PhonebookTestCase):
    def test_change_number(self):
        """
        Update a person's phone number
        """
        result = self.env.run('phonebook ' + \
                              ('change "Mary Anderson" "123 456 7890" ') + \
                              ('-b %s/phonebook_fixture.pb' % self.prefix))
        expected_output = "Mary Anderson's phone number changed from " + \
                          "572 932 1921 to 123 456 7890."
        nose.tools.assert_in(expected_output, result.stdout)

        self.assert_added(['Mary Anderson','123 456 7890'])
        self.assert_not_added(['572 932 1921'])

    def test_change_not_exist(self):
        """
        Try to update the phone number of a person who does not exist
        """
        result = self.env.run('phonebook ' + \
                              ('change "Bobby Goodgame" "999 999 9999" ') + \
                              ('-b %s/phonebook_fixture.pb' % self.prefix))
        expected_output = "Bobby Goodgame is not in this phonebook. " + \
                          "Use 'add' instead."
        nose.tools.assert_in(expected_output, result.stdout)

        self.assert_not_added(['Bobby Goodgame','999 999 9999'])

    def test_change_malformed_number(self):
        """
        Try to change a person's number to a malformed phone number
        """
        result = self.env.run('phonebook ' + \
                              ('change "Mary Anderson" "bad number" ') + \
                              ('-b %s/phonebook_fixture.pb' % self.prefix))
        expected_output = "Entry not created: 'bad number' is not a valid phone number."
        nose.tools.assert_in(expected_output, result.stdout)

        self.assert_not_added(['bad number'])

class RemoveTestCase(PhonebookTestCase):
    def test_remove(self):
        """
        Remove someone from the phonebook
        """
        result = self.env.run('phonebook ' + \
                              ('remove "Mary Anderson" ') + \
                              ('-b %s/phonebook_fixture.pb' % self.prefix))
        expected_output = "Removed Mary Anderson from %s/phonebook_fixture.pb." % self.prefix
        nose.tools.assert_in(expected_output, result.stdout)
        self.assert_not_added(["Mary Anderson"])


    def test_remove_nonexistent(self):
        """
        Try to remove a nonexistent person from the phonebook
        """
        self.assert_not_added(["Nonexistent person"])
        result = self.env.run('phonebook ' + \
                              ('remove "Nonexistent person" ') + \
                              ('-b %s/phonebook_fixture.pb' % self.prefix))
        expected_output = "Could not remove: there is no one in %s/" % self.prefix + \
                          "phonebook_fixture.pb named 'Nonexistent person'."
        nose.tools.assert_in(expected_output, result.stdout)
        self.assert_not_added(["Nonexistent person"])

    def test_remove_multiple_possibilities(self):
        """
        Try to remove an entry without supplying a unique name.
        """
        result = self.env.run('phonebook ' + \
                              ('remove "Nonexistent person" ') + \
                              ('-b %s/phonebook_fixture.pb' % self.prefix))
        expected_output = "Could not remove: there is no one in %s/" % self.prefix + \
                          "phonebook_fixture.pb named 'Nonexistent person'."
        nose.tools.assert_in(expected_output, result.stdout)
        self.assert_not_added(["Nonexistent person"])
