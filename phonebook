#!/usr/bin/env python
import argparse
import csv
import sys
from phonebook_class import Phonebook
from person import Person

def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", action='store')
    parser.add_argument("params", action='store', nargs='*')
    parser.add_argument("-b", "--book", action="store")
    return parser

if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args()
    phonebook = Phonebook(args)
    args.command = args.command.replace('-','_')
    if phonebook:
        getattr(phonebook, args.command)(args.params)
