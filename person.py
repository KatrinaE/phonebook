import re


def clean_phone_number(formatted_number):
    """
    Pattern is from Dive into Python
    http://www.diveintopython.net/regular_expressions/phone_numbers.html
    """
    phonePattern = re.compile(r'''
    # don't match beginning of string, number can start anywhere
    (\d{3})     # area code is 3 digits (e.g. '800')
    \D*         # optional separator is any number of non-digits
    (\d{3})     # trunk is 3 digits (e.g. '555')
    \D*         # optional separator
    (\d{4})     # rest of number is 4 digits (e.g. '1212')
    \D*         # optional separator
    (\d*)       # extension is optional and can be any number of digits
    $           # end of string
    ''', re.VERBOSE)
    try:
        clean_number = ' '.join(phonePattern.search(formatted_number).groups()).rstrip()
    except AttributeError:
        print "Error: Invalid phone number."
        # TODO: what to return??
    return clean_number

class Person(object):
    def __init__(self, person_dict):
        self.name = person_dict['name']
        self.phone_number = clean_phone_number(person_dict['phone_number'])
