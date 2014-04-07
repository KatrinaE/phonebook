#Phonebook
Phonebook is an basic command-line phonebook application implementing the
[Hacker School phonebook specification](https://hackpad.com/Manage-those-phone-books-wK1MycZ5ATb).
It stores names and phone numbers in comma-separated text files
(though it could be easily extended to use a more robust backend).

##Installation
Download Phonebook:

    git clone https://github.com/KatrinaE/phonebook.git phonebook

Make Phonebook executable:

    cd path-to-phonebook
    chmod u+x phonebook

Add Phonebook to your path, e.g.:

    ln -s path-to-phonebook/phonebook /usr/local/bin/phonebook

##Usage

Available commands are:

* `create`: Create a new phonebook with the given filename

        phonebook create phonebook.txt

* `set-default`: Set the given phonebook to be the default

        phonebook set-default phonebook.txt

    (To use a non-default phonebook, use the `-b` option)

        phonebook create different-phonebook.txt
        phonebook lookup 'John Smith' -b different-phonebook.txt

* `add`: Add a person to the phonebook

        phonebook add 'John Smith' '(987) 654-3210'

    A person may only be in the phonebook once - you
    cannot store e.g. one entry containing 
    a person's home phone number
    and another entry with his cell phone number.

* `remove`: Remove a person from the phonebook

        phonebook remove 'John Smith'

* `lookup`: Look up a person by name

        phonebook lookup 'John'

    Lookup matches all entries containing the lookup string
    and prints them to the console.

* `reverse-lookup`: Look up a person by phone number

        phonebook reverse-lookup '(987) 654-3210'

    Reverse-lookup may return more than one person if both
    of them have the same phone number.

    Phone numbers are validated using the 
    [parser implemented in 'Dive into Python'](http://www.diveintopython.net/regular_expressions/phone_numbers.html). It supports US phone numbers entered in any format. 
    The numbers are stored and displayed in the format 'XXX XXX XXXX'.


## To-Dos
'Default phonebook' behavior is currently untested.