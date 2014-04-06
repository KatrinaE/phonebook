import re
import sys

def clean_number(formatted_number):
    """
    Pattern is from Dive into Python
    http://www.diveintopython.net/regular_expressions/numbers.html
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
        print "Entry not created: '%s' is not a valid phone number." % formatted_number
        sys.exit()
    return clean_number
