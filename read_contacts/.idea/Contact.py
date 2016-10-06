# Python learning project:
#   Build a Contacts management program that reads in my contacts (from a .csv file to start).
#   In this file: The class that holds each contact.

class Contact():
    """Contact holds one contact as a dictionary, likely multi-level dictionary."""

    def __init__(self, header, contact_data):
        """Contact constructor - parse contact_data according to header, to fill a dictionary of information."""
        self.contact_info = {}
        self.parse_csv_fields(header, contact_data)

    def parse_csv_fields(self, header, contact_data):
        field_data = str.split(contact_data, ',')
        #print(header)
        #print(field_data)
        #print('Lengths of header, field_data: ' + str(len(header)) + ', ' + str(len(field_data)))

        # Match up the lists to create a dictionary.  Include only fields with non-empty data
        for index in range(len(header)):
            assert len(header) == len(field_data), print('!!Length mismatch!! \n' + str(field_data))
            if field_data[index]:
                self.contact_info[header[index]] = field_data[index]

        print(self.contact_info)



    def print_contact(self):
        """Print the important fields in a contact"""

