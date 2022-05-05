import datetime as date
import random
import string
import os
import json

membersdirectory = './members.json'
loansdirectory = './loans.json'
itemdirectory = './items.json'

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
    def __init__(self, title: str, description: str):
        '''description: str'''
        self.ItemNum = ''.join(random.choices(string.ascii_letters, k=3)) +'-'+''.join(random.choices(string.digits, k=3)) +'-'+ type(self).__name__
        self.description = description
        self.title = title


class Book(Item):
    def __init__(self, ISBN: str, publisher: str, listofauthors: list, *args, **kwargs):
        '''title: str, isbn:str , publisher:str , list of authors: list, description: str'''
        super(Book, self).__init__(*args, **kwargs)
        self.ISBN = ISBN
        self.publisher = publisher
        self.authors = listofauthors


class Journal(Book):
    def __init__(self, volume: str, articlelist: list, *args, **kwargs):
        super(Book, self).__init__(*args, **kwargs)
        self.volume = volume
        self.articlelist = articlelist


class Article(Item):
    def __init__(self,articletitle, journal: Journal, volume: str, listofauthors: list, *args, **kwargs):
        super(Article, self).__init__(*args, **kwargs)
        self.articletitle = articletitle
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


