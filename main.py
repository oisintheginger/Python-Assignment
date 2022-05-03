'''
This project is a Library System that uses a visual GUI for users to sign up for a library membership, borrow books,
and make reservations for other library facilities such as study spaces and projector rooms.

----------------LIBRARY MANAGEMENT SYSTEM:---------------------
You are asked to develop an application to manage library services, such as borrowing and
returns activities. You should be able to borrow/return a book, an article in a journal, or
digital media. All the library information should be stored in four external files:
library.txt, items.txt, members.txt, and borrowing.txt. It is up to you to define
the structure of each file, but each member, item or transaction should have an unique ID.
Use Python classes to implement the library. Some of the functionality your system should
provide includes:
● At least the following classes: Library, Items, Books, Articles, Digital Media, Members
● Books, Articles, Digital Media should be a subclass of Items.
● Each class should have an __init__ and __str__ methods. For each __str__ method,
think what information each class should provide when you print their instances.
● Persistent memory: when you start your system it should read the files library.txt,
items.txt, members.txt, and borrowing.txt in the same folder as the python
code and create all the necessary instances.
● Provide a command line interface for the user to:
    ○ Add/edit/delete instances belonging to each class,
    ○ Members browse library items and select items to borrow.
    ○ Members returning borrowed items.
    ○ Make sure to update the external files after any information is modified
'''
import datetime as date
import json
import random
import string
import os.path

class Address:
    def __init__(self, AddressLine1, AddressLine2, Town, County, Province, Country, Postcode):
        self.AddressLine1 = AddressLine1
        self.AddressLine2 = AddressLine2
        self.Town = Town
        self.County = County
        self.Province = Province
        self.Country = Country
        self.Postcode = Postcode



class Member():
    def __init__(self, Name: str, address: Address, DOB: date.datetime):
        self.Name = Name
        self.Address = address
        self.DOB = DOB
        self.MemberID = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        bookingsList = list()
        loanslist = list()




datastream = {
}

def memberformatter(member: Member):
    memberdetails = {}
    memberdetails['name'] = member.Name
    memberdetails['address'] = [member.Address.AddressLine1, member.Address.AddressLine2, member.Address.Town, member.Address.County, member.Address.Province, member.Address.Country, member.Address.Postcode]
    memberdetails['dob'] = str(member.DOB)
    return memberdetails

def main():
    while True:
        inp = input('q to quit')
        if inp == 'q':
            break

if __name__ == '__main__':
    if os.path.exists('members.json'):
        with open('members.json') as json_file:
            datastream = json.load(json_file)
            #stringggg = json.dumps(datastream)
            print(datastream)

    add = Address('no','no','yare yare','no','no','no','no')
    mem = Member('Philip', add, date.datetime.now())
    datastream[mem.MemberID] = memberformatter(mem)
    print(datastream)
    with open('members.json', 'w') as outfile:
        json.dump(datastream, outfile)
    #file1 = open("MembersFile.json", "a+")
