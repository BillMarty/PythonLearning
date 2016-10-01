# Working through Chapter 10 on Files and Exceptions
# My own project: open and read a file containing my contacts (in csv to start).

file_path = '/Users/billmarty/PythonLearning/CB_contacts.csv'

with open(file_path) as file:
    lines = file.readlines()
    print('Read ' + str(len(lines)) + ' lines from ' + file_path)

print('The header is: ' + lines[0])
header = lines[0]

#Separate out the filds in header
fields = str.split(header, ',')
print(fields)

