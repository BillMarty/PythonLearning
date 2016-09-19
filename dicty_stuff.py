# Some work with dictionaries :-)
#Changed file encoding from UTF-8 to ASCII

# First, let's create a dictionary with some interesting content.
# How about info from my contacts list?  A list of dictionaries, one per person.
cb_contacts = []
# Last Name,First Name,Organization,Phone : Mobile,Phone : Home,Phone : iPhone,Email : Home,Email : Other,Email : Work,Address : Home : Street,Address : Home : City,Address : Home : State,Address : Home : Country,Address : Home : ZIP,URL : HomePage,Note
# ,Okoth,Fr. Crispin,,(206)?794-7487,,,frcrispin@stjohnsea.org,,,,,,,,,
cb_contacts.append({'Last Name': 'Okoth', 'First Name': 'Fr. Crispin', 'Organization': '', 'Phone': '(206)?794-7487', 'Email': 'frcrispin@stjohnsea.org'})
# ,Kent,Lawrence,Gates Foundation,,,,,lawrence.kent@gatesfoundation.org,,,,,,,,
cb_contacts.append({'Last Name': 'Kent', 'First Name': 'Lawrence', 'Organization': 'Gates Foundation', 'Phone': '', 'Email': 'lawrence.kent@gatesfoundation.org'})
# ,Beberness,Soheila,,1?(503)?381-1122,,,soheilab@live.com,,,9013 Forest Hill Pl NW,Seattle,WA,,98177,,
cb_contacts.append({'Last Name': 'Beberness', 'First Name': 'Soheila', 'Organization': '', 'Phone': '1?(503)?381-1122', 'Email': 'soheilab@live.com'})
# ,Kent,Kristin,,,(206) 783-1949,(206)?852-0393,,dearkristink@yahoo.com,,,,,,,,
cb_contacts.append({'Last Name': 'Kent', 'First Name': 'Kristin', 'Organization': '', 'Phone': '(206) 783-1949', 'Email': 'dearkristink@yahoo.com'})
# ,Marty,Sheila,,,206 794-0992,,,,smarty@stjohnsea.org,334 N 83rd Street,Seattle,WA,United States,98103,,
cb_contacts.append({'Last Name': 'Marty', 'First Name': 'Sheila', 'Organization': '', 'Phone': '206 794-0992', 'Email': 'smarty@stjohnsea.org'})


print('You have ' + str(len(cb_contacts)) + ' contacts :-)')

for contact in cb_contacts:
    print(contact['First Name'] + ' ' + contact['Last Name'])
    if contact['Organization']:
        print(contact['Organization'])
    if contact['Phone']:
        print(contact['Phone'])
    print(contact['Email'])
    print()

# Try something fancy
# First, add a key to each contact dictionary telling whether it has been marked.
for contact in cb_contacts:
    contact['Marked'] = False
    #print(contact)
# Second, let's do some sorting  (We could combine these two steps later.)
last_names = []
for contact in cb_contacts:
    last_names.append(contact['Last Name'])
print(sorted(last_names))

sorted_cb_contacts = []
for last_name in sorted(last_names):
    for contact in cb_contacts:
        if (not contact['Marked']) and (contact['Last Name'] == last_name):
            # Add this contact to the sorted list
            sorted_cb_contacts.append(contact)
            # "Remove" this contact from cb_contacts[]
            contact['Marked'] = True
            # Progress report
            print('Moving contact: ' + last_name)

print('\nDone sorting contacts')

for contact in sorted_cb_contacts:
    print(contact['First Name'] + ' ' + contact['Last Name'])
    if contact['Organization']:
        print(contact['Organization'])
    if contact['Phone']:
        print(contact['Phone'])
    print(contact['Email'])
    print()
