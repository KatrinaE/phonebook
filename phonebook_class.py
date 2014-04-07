import csv
import sys
import ConfigParser
from person import Person
from number_regex import clean_number

class Phonebook(object):
    """
    A phonebook holds loaded phonebook data and has methods for:
    - adding entries
    - removing entries
    - looking up a person by name
    - looking up a person by phone number
    """
    def __init__(self, args):
        """
        Initialize a phone book from a filename. Attempt to use
        'args.book'; if not supplied, use default phonebook from
        config file.
        """
        self.people = []
        if args.book is not None:
            self.filename = args.book
        else:
            parser = ConfigParser.SafeConfigParser()
            parser.read('config.cfg')
            self.filename = parser.get('phonebook', 'default_phonebook')
        if args.command != 'create':
            self.load_data()

    def create(self, params):
        """
        Creates a new, empty phonebook file
        """
        filename = params[0]
        if file_exists(filename):
            print "Not created: file named %s already exists" % filename
        else:
            self.filename = filename
            success_msg = ("Created phonebook named %s " % filename) + \
                          ("in the current directory.")
            failure_msg = ("System error: failed to create phonebook ") + \
                          ("named %s." % filename)
            self.save(success_msg, failure_msg)

    def set_default(self, params):
        """
        Make the current phonebook the default phonebook.
        """
        self.filename = params[0]
        self.load_data()
        try:
            parser = ConfigParser.SafeConfigParser()
            parser.read('config.cfg')
            parser.set('phonebook', 'default_phonebook', self.filename)
            parser.write(open('config.cfg', 'w'))
            print "Set default phonebook to %s." % self.filename
        except:
            print "Unable to set the default phonebook to %s." % self.filename
            sys.exit()

    def lookup(self, params):
        """
        Look up a person by name
        """
        search_name = params[0]
        output = ''
        for person in self.people:
            if search_name in person.name:
                person_string = person.name + " " + str(person.number)
                print person_string
                output = '\n'.join([output, person_string])
        if output == '':
            print "No entries found."

    def reverse_lookup(self, params):
        """
        Look up a person by phone number
        """
        search_number = clean_number(params[0])
        output = ''
        for person in self.people:
            if search_number in person.number:
                person_string = person.name + " " + str(person.number)
                print person_string
                output = '\n'.join([output, person_string])
        if output == '':
            print "No entries found."

    def add(self, params):
        """
        Add an entry (person + phone number)
        """
        name = params[0]
        number = extract_number(params)
        person = Person(name, number)

        # make sure this won't be a duplicate
        if is_duplicate(person.name, self.people):
            print ("Entry not created: %s " % name) + \
                "is already in this phonebook."
            sys.exit()

        self.people.append(person)
        person_string = person.name + " " + str(person.number)
        success_msg = ("Entry '%s' added to " % person_string) + \
                      ("phonebook %s" % self.filename)
        failure_msg = "System error: failed to add person to phonebook."
        self.save(success_msg, failure_msg)


    def change(self, params):
        """
        Change an existing person's phone number
        """
        name = params[0]
        number = extract_number(params)

        if not is_duplicate(name, self.people):
            print ("%s is not in this phonebook. " % name) + \
                "Use 'add' instead."
            sys.exit()

        people_to_change = [p for p in self.people if p.name == name]
        person_to_change = people_to_change[0]
        if len(people_to_change) > 1:
            print ("There are multiple people named %s " % name) + \
                   ("in %s" % self.filename)
            sys.exit()

        old_number = person_to_change.number
        person_to_change.number = number
        success_msg = "%s's phone number changed " % person_to_change.name + \
                      "from %s to %s." % (old_number, person_to_change.number)
        failure_msg = "System failure: failed to update number."
        self.save(success_msg, failure_msg)


    def remove(self, params):
        """
        Remove a person
        """
        # Name requires an exact match, i.e. 'John' will not find 'John Smith'
        name = params[0]
        try:
            people_to_remove = [p for p in self.people if p.name == name]
            person_to_remove = people_to_remove[0]
        except IndexError:
            print "Could not remove: there is no one in %s " % self.filename + \
                "named '%s'." % name
            sys.exit()
        self.people.remove(person_to_remove)
        success_msg = "Removed %s from %s." % (name, self.filename)
        failure_msg = ("System failure: failed to remove %s " % name) + \
                      ("from %s." % self.filename)
        self.save(success_msg, failure_msg)

    def save(self, success_msg, failure_msg):
        """
        Save the phonebook. Implementation details are hidden in execute_save()
        """
        try:
            self.execute_save()
            print success_msg
        except:
            print failure_msg
            sys.exit()

    def execute_save(self):
        """
        Save the phonebook. Currently, saving means
        re-writing the text file storing the current phonebook's data.
        (Do not call this method, call save() instead)
        """
        # possible optimization: if adding a person,
        # just append to the file rather than rewriting
        # the entire thing
        with open(self.filename, 'wb') as f:
            fieldnames = ['name', 'number']
            csvwriter = csv.DictWriter(f, fieldnames)
            csvwriter.writerow(dict((fn, fn) for fn in fieldnames))
            for p in self.people:
                csvwriter.writerow(p.__dict__)

    def load_data(self):
        """
        Load phonebook data into memory
        """
        if not self.filename:
            print "Please include a phonebook filename."
            sys.exit()

        if file_exists(filename):
            with open(self.filename, 'r') as f:
                reader = csv.DictReader(f)
                person_dicts = [row for row in reader]
            if person_dicts is not []:
                for person in person_dicts:
                    p = Person.from_dict(person)
                    self.people.append(p)
        else:
            print 'No file named %s found.' % self.filename
            sys.exit()

def file_exists(filename):
    """
    Check if a file already exists
    """
    try:
        f = open(filename)
        file_exists = True
    except IOError:
        file_exists = False
    return file_exists

def extract_number(params):
    """
    Get number from input args. Fails if number was not included.
    """
    try:
        number = clean_number(params[1])
    except IndexError:
        print "Please include a phone number."
        sys.exit()
    return number

def is_duplicate(name, people_list):
    """
    Check to see if a person is already in the phonebook
    """
    already_in_book = [p.name for p in people_list]
    if name in already_in_book:
        return True
