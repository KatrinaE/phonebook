#!/usr/bin/env python

import argparse
import csv
import sys
from phonebook_class import Phonebook
from person import Person

def make_dicts(phonebook_file):
    reader = csv.DictReader(phonebook_file)
    person_dicts = [row for row in reader]
    return person_dicts

def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", action='store')
    parser.add_argument("params", action='store', nargs='*')
    parser.add_argument("-b", "--book", action="store")
    return parser

def load_phonebook(filename):
    if not filename:
        print "Please include a phonebook filename."
        phonebook = False
    else:
        try:
            f = open(filename)
            try:
                person_dicts = make_dicts(f)
                phonebook = Phonebook(filename, person_dicts)
            finally:
                f.close()
        except IOError:
            print ('No file named %s found.' % filename)
            phonebook = False
                
    return phonebook

def make_new_phonebook(args):
    try:
        filename = args.params[0]
    except IndexError:
        print "'create' requires a filename."
    phonebook = Phonebook(filename, [])
    return phonebook

def instantiate_phonebook(args):
    if args.command == 'create':
        phonebook = make_new_phonebook(args)
    else:
        phonebook = load_phonebook(args.book)
    return phonebook

def perform_phonebook_action(args):
    phonebook = instantiate_phonebook(args)
    if phonebook:
        output = getattr(phonebook, args.command)(*args.params)
        return output

if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args()
    output = perform_phonebook_action(args)
    if output:
        print output
