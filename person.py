"""
Person is a struct for holding a phonebook entry that has been loaded
into memory.
"""
from number_regex import clean_number

class Person(object):
    def __init__(self, name, number):
        """
        Initialize a person by providing a name and phone number
        """
        self.name = name
        self.number = clean_number(number)

    @classmethod
    def from_dict(cls, person_dict):
        """
        Initialize a person by providing a dict containing the fields
        'name' and 'number'
        """
        name = person_dict['name']
        number = clean_number(person_dict['number'])
        return cls(name, number)
