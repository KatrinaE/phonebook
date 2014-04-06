from number_regex import clean_number
import sys


class Person(object):
    def __init__(self, name, number):
        self.name = name
        self.number = clean_number(number)

    @classmethod
    def from_dict(cls, person_dict):
        name = person_dict['name']
        number = clean_number(person_dict['number'])
        return cls(name, number)
