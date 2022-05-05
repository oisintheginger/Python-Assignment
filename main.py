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

membersdirectory = 'members.json'
loansdirectory = 'loans.json'

class Address():
    def __init__(self, AddressLine1:str, AddressLine2:str, Town:str, County:str, Province:str, Country:str, Postcode:str):
        self.AddressLine1 = AddressLine1
        self.AddressLine2 = AddressLine2
        self.Town = Town
        self.County = County
        self.Province = Province
        self.Country = Country
        self.Postcode = Postcode

    def __str__(self):
        return '\n{0}\n{1}\n{2}\n{3}\n{4}\n{5}\n{6}\n'.format(self.AddressLine1, self.AddressLine2, self.Town, self.County, self.Province, self.Country, self.Postcode)



class Member():
    def __init__(self, Name: str, address: Address, DOB: date.datetime, ID =''):
        self.Name = Name
        self.MemberAddress = address
        self.DOB = DOB
        if ID == '':
            self.MemberID = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        else:
            self.MemberID = ID
        bookingsList = list()
        loanslist = list()

    def __str__(self):
        return '{0} lives in {1}, and were born on {2}. Their user ID is {3}'.format(self.Name, self.MemberAddress.Town, self.DOB, self.MemberID)


class Item():
    def __init__(self, description: str):
        '''description: str'''
        self.ItemNum = ''.join(random.choices(string.ascii_letters, k=3)) +'-'+''.join(random.choices(string.digits, k=3)) +'-'+ type(self).__name__
        self.description = description


class Book(Item):
    def __init__(self,title, ISBN: str, publisher: str, listofauthors: list, *args, **kwargs):
        '''title: str, isbn:str , publisher:str , list of authors: list, description: str'''
        super(Book, self).__init__(*args, **kwargs)
        self.title = title
        self.ISBN = ISBN
        self.publisher = publisher


class Journal(Book):
    def __init__(self, volume: str, articlelist: list, *args, **kwargs):
        super(Book, self).__init__(*args, **kwargs)
        self.volume = volume
        self.articlelist = articlelist


class Article(Item):
    def __init__(self,title, journal: Journal, volume: str, listofauthors: list, *args, **kwargs):
        super(Article, self).__init__(*args, **kwargs)
        self.title = title
        self.JournalISBN = journal.ISBN
        self.authors = listofauthors
        self.volume = volume



class Library():
    def __init__(self, name: str):
        self.Name = name
        self.Members = dict
        if os.path.exists(membersdirectory):
            with open(membersdirectory, 'r') as json_file:
                try:
                    self.Members = json.loads(json_file.read())
                except ValueError:
                    self.Members = {}
        self.Loans = dict
        if os.path.exists(loansdirectory):
            with open(loansdirectory, 'r') as json_file:
                try:
                    self.Loans = json.loads(json_file.read())
                except ValueError:
                    self.Members = {}

datastream = {}


def memberformatter(member: Member):
    memberdetails = {}
    memberdetails['name'] = member.Name
    memberdetails['address'] = [member.MemberAddress.AddressLine1, member.MemberAddress.AddressLine2, member.MemberAddress.Town, member.MemberAddress.County, member.MemberAddress.Province, member.MemberAddress.Country, member.MemberAddress.Postcode]
    memberdetails['dob'] = str(member.DOB)
    return memberdetails


def jsontomember(jsondictionary: dict, memberID: str):
    memberdatadict = jsondictionary[memberID]
    dataname = memberdatadict['name']
    dataaddress = Address(memberdatadict['address'][0], memberdatadict['address'][1], memberdatadict['address'][2], memberdatadict['address'][3], memberdatadict['address'][4],memberdatadict['address'][5],memberdatadict['address'][6])
    dataDOB = memberdatadict['dob']
    returnable = Member(dataname,dataaddress,dataDOB, memberID)
    return returnable

def itemformatter(item: Item):
    itemdetails ={}
    itemdetails['itemnumber'] = item.ItemNum
    itemdetails['description'] = item.description
    if type(item).__name__ == 'Book':
        itemdetails['isbn'] = item.ISBN
        print('issa book!')



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

    newItem = Book('The Wind and the Willows', 'X49932-18839','Penguin', ['Author of the Book'], 'An old story that I do not know the plot of.')
    itemformatter(newItem)

    datastream = dict()

    print(datastream)
    with open(membersdirectory, 'w') as outfile:
        json.dump(datastream, outfile, indent = 4)






def main():
    setup()
    it = Item('This is a description')
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
