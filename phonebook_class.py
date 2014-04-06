import csv
import sys
from person import Person

class Phonebook(object):
    def __init__(self, args):
        self.people = []
        self.filename = args.book
        if args.command != 'create':
            self.load_data()

    def create(self, params):
        filename = params[0]
        """
        Creates a new, empty phonebook file
        """
        # Check if file already exists to prevent accidental overwrites
        file_exists = True
        try:
            f = open(filename)
        except IOError:
            file_exists = False
        if file_exists:
            print ("Not created: file named %s already exists" % filename)
        else:
            self.filename = filename
            self.save()
            print("Created phonebook named %s in the current directory" % filename)
 
    def lookup(self, params):
        search_name = params[0]
        """
        Looks up a person by name in an existing phonebook
        """
        output = ''
        for person in self.people:
            if search_name in person.name:
                person_string = person.name + " " + str(person.phone_number)
                print person_string
                output = '\n'.join([output, person_string])
        if output == '':
            print "No entries found."

    def add(self, params):
        name = params[0]

        # make sure number was included
        try:
            number = params[1]
        except IndexError:
            print "Please include a phone number."
            sys.exit()

        # make sure this won't be a duplicate
        already_in_book = [person.name for person in self.people]
        if name in already_in_book:
            print "Entry not created: %s is already in this phonebook." % name
            sys.exit()

        person_dict = { 'name' : name,
                        'phone_number' : number
                        }
        person = Person(person_dict)

        # add to phonebook file
        try:
            self.people.append(person)
            self.save()
            person_string = person.name + " " + str(person.phone_number)
            print ("Entry '%s' added to phonebook phonebook_fixture.pb" % person_string)
        except:
            print "System error: failed to add person to phonebook."
            sys.exit()


    def save(self):
        # possible optimization: if adding a person,
        # just append to the file rather than rewriting
        # the entire thing
        with open(self.filename, 'wb') as f:
            fieldnames = ['name', 'phone_number']
            csvwriter = csv.DictWriter(f, fieldnames)
            csvwriter.writerow(dict((fn, fn) for fn in fieldnames))
            for p in self.people:
                csvwriter.writerow(p.__dict__)

    def load_data(self):
        if not self.filename:
            print "Please include a phonebook filename."
            sys.exit()
        try:
            with open(self.filename, 'r') as f:
                reader = csv.DictReader(f)
                person_dicts = [row for row in reader]
            if person_dicts is not []:
                for person in person_dicts: 
                    p = Person(person)
                    self.people.append(p)
        except IOError:
            print ('No file named %s found.' % self.filename)
            sys.exit()
