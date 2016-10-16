# Python learning project:
#   Build a Contacts management program that reads in my contacts (from a .csv file to start).
#   In this file: The base class containing and manipulating my list of contacts.

from contact import Contact
import platform
import sys

# Detect OS, so that I can do work on Mac at home and Windows at work.
macos_contacts_file_path = '/Users/billmarty/PythonLearning/CB_contacts.csv'
windows_contacts_file_path = "C:/Users/bmarty/Documents/PyCharmProjects/PythonLearning/CB_Contacts.csv"
if 'Windows' in platform.system():
    contacts_file_path = windows_contacts_file_path
else:
    contacts_file_path = macos_contacts_file_path

class MyContacts():
    """A class to contain a list of my contacts."""

    def __init__(self, in_file):
        """init: Don't know what goes here yet."""
        assert 'csv' in in_file, '!File is not *.csv!'
        self.read_from_csv_file(in_file)
        self.remove_empty_contacts()
        self.handle_difficult_lines()

    def read_from_csv_file(self, in_file):
        """Import a csv file that was exported from the Apple Contacts application.
                file: path specification for the csv file"""

        try:
            with open(in_file) as file:
                lines = file.readlines()
        except FileNotFoundError:
            print('!!File not found: ' + str(in_file) + '!!')
            sys.exit('Aborting...')

        print('Read ' + str(len(lines)) + ' lines from ' + in_file)

        # The first line in the file is the header, that maps all the field names.
        header = lines[0].rstrip()
        print('The header is: ' + header)
        del lines[0]

        #Separate out the fields in header
        header_fields = str.split(header, ',')
        print(header_fields)
        print('\nThere are ' + str(len(lines)) + ' contact records in the list.')

        # Create one contact object for each line in the file.
        self.contacts = []
        self.difficult_lines = []
        # When a contact includes multi-line text in the Notes field, the csv file contains lines that
        #   aren't "records".  Set these difficult lines apart for right now.
        is_multi_line_record = False
        for line in lines:
            line = line.rstrip()
            if '"' in line and not is_multi_line_record:
                self.difficult_lines.append(line)
                print('Adding to difficult lines: ' + line)
                is_multi_line_record = True
            elif is_multi_line_record and '"' not in line:
                self.difficult_lines.append(line)
                print('Adding to difficult lines: ' + line)
            elif is_multi_line_record and '"' in line:
                self.difficult_lines.append(line)
                print('Adding to difficult lines: ' + line)
                is_multi_line_record = False
            else:
                self.contacts.append(Contact(header_fields, line))

    def remove_empty_contacts(self):
        """My csv file seems to include a certain number of empty contact records at the end of the file.
            This function removes them."""
        starting_count = len(self.contacts)
        empties = []
        for index, contact in enumerate(self.contacts):
            if not contact.info:
                empties.append(index)

        empties.reverse()
        for index in empties:
            del self.contacts[index]

        ending_count = len(self.contacts)
        print("Removed " + str(starting_count - ending_count) + " empty contacts.\n")

    def handle_difficult_lines(self):
        """The csv file includes 'difficult' records.  This function cleans them and adds them to contacts.
            1) Records with multi-line entries in the Notes field."""
        is_multi_line_record = False
        for line in self.difficult_lines:
            print(line)
            if '"' in line and not is_multi_line_record:
                building_line = line
                #Let's wrap the multi-line-notes field in triple quotes.
                #First, replace the double quote character with tripple double quotes.
                index = building_line.find('"')
                building_line = building_line[:index] + '""' + building_line[index:] + "\n"
                print("\tReplaced opening quote at " + str(index))
                print("\t" + building_line)
                is_multi_line_record = True
            elif is_multi_line_record and '"' not in line:
                building_line = building_line + line + "\n"
                print("\tAdding:" + building_line)
            elif is_multi_line_record and '"' in line:
                #Finally, replace closing double quote with tripple quote.
                index = building_line.find('"')
                building_line = building_line[:index] + '""' + building_line[index:] + "\n"
                print("\tFinally: " + building_line)
                is_multi_line_record = False
                #Add to contacts...
                self.contacts.append(Contact(header_fields, line))
            else:
                print("Why are we here?")

        print()


my_contacts = MyContacts(contacts_file_path)
