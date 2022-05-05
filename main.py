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
from projectclasses import *
from formatter import *




def setup():
    if os.path.exists(membersdirectory):
        os.remove(membersdirectory)
    if os.path.exists(loansdirectory):
        os.remove(loansdirectory)

    PhilipAdd = Address('8024', 'Doyle Avenue', 'Roscommon Town', 'Roscommon', 'Munster', 'Ireland', 'A73MX91')
    Philip = Member('Philip', PhilipAdd, date.datetime.now())

    MaryAdd = Address('79', 'Cliff Road', 'Galway City', 'Galway', 'Connaught', 'Ireland', 'E94XM23')
    Mary = Member('Mary', MaryAdd, date.datetime.now())

    JimAdd = Address('100', 'Skid Row', 'Chicago', 'Chicago', 'Illinois', 'United States of America', 'M90TU32')
    Jim = Member('Jim', JimAdd, date.datetime.now())

    ChloeAdd = Address('27', 'Mill Lane', 'Trim', 'Meath', 'Leinster', 'Ireland', 'P92VI65')
    Chloe = Member('Mary', ChloeAdd, date.datetime.now())

    datastream = dict()
    datastream[Philip.MemberID] = memberformatter(Philip)
    datastream[Mary.MemberID] = memberformatter(Mary)
    datastream[Jim.MemberID] = memberformatter(Jim)
    datastream[Chloe.MemberID] = memberformatter(Chloe)

    with open(membersdirectory, 'w') as outfile:
        json.dump(datastream, outfile, indent = 4)

    datastream = dict()
    newItem = Book( 'X49932-18839', 'Penguin', ['Author of the Book'], 'The Wind and the Willows','An old story that I do not know the plot of.')
    datastream[newItem.ItemNum] = itemformatter(newItem)

    with open(itemdirectory, 'w') as outfile:
        json.dump(datastream, outfile, indent = 4)


    print(datastream)







def main():
    setup()
    it = Item('This is a title', 'This is a description')
    lib = Library('New Library Bro')
    #LoggedIn = jsontomember(lib.Members, 'ww7vA3i2J99RMfIc')
   # print(LoggedIn)
    while True:
        inp = input('q to quit')
        if inp == 'q':
            break






if __name__ == '__main__':
    main()

    '''

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
    '''
