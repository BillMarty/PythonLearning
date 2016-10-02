# Python learning project:
#   Build a Contacts management program that reads in my contacts (from a .csv file to start).
#   In this file: The base class containing and manipulating my list of contacts.

from contact import Contact 

contacts_file_path = '/Users/billmarty/PythonLearning/CB_contacts.csv'

class MyContacts():
    """A class to contain a list of my contacts."""

    def __init__(self, in_file):
        """init: Don't know what goes here yet."""
        assert 'csv' in in_file, '!File is not *.csv!'
        self.read_from_csv_file(in_file)

    def read_from_csv_file(self, in_file):
        """Import a csv file that was exported from the Apple Contacts application.
                file: path specification for the csv file"""

        with open(in_file) as file:
            lines = file.readlines()
            print('Read ' + str(len(lines)) + ' lines from ' + in_file)

        # Verify that I'm reading all the lines correctly.
        # index = 1
        # for line in lines:
        #     print(str(index) + ')  ' + line.rstrip())
        #     index += 1
        # print()
        # print()


        # The first line in the file is the header, that maps all the field names.
        header = lines[0].rstrip()
        print('The header is: ' + header)
        del lines[0]

        #Separate out the fields in header
        header_fields = str.split(header, ',')
        print(header_fields)
        print('\nThere are ' + str(len(lines)) + ' contact records in the list.')

        # Create one contact object for each line in the file.
        contacts = []
        difficult_lines = []
        is_multi_line_record = False
        for line in lines:
            line = line.rstrip()
            if '"' in line and not is_multi_line_record:
                difficult_lines.append(line)
                print('Adding to difficult lines: ' + line)
                is_multi_line_record = True
            elif is_multi_line_record and '"' not in line:
                difficult_lines.append(line)
                print('Adding to difficult lines: ' + line)
            elif is_multi_line_record and '"' in line:
                difficult_lines.append(line)
                print('Adding to difficult lines: ' + line)
                is_multi_line_record = False
            else:
                contacts.append(Contact(header_fields, line))


my_contacts = MyContacts(contacts_file_path)
