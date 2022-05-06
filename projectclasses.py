import datetime as date
import random
import string
import os
import json





membersdirectory = './members.json'
loansdirectory = './loans.json'
itemdirectory = './items.json'

def request_num_input(inp: str, intorfloat = False):
    while True:
        response = input(inp)
        if intorfloat is False:
            try:
                response = float(response)
                break
            except ValueError:
                print("The value entered was not numeric")
        else:
            try:
                response =int(response)
                break
            except ValueError:
                print("The value entered was not numeric")
    return response



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

    def __str__(self):
        return '{0} lives in {1}, and were born on {2}. Their user ID is {3}'.format(self.Name, self.MemberAddress.Town, self.DOB, self.MemberID)


class Item():
    def __init__(self, title: str, description: str, itemnum = ' '):
        '''description: str'''
        if itemnum == ' ':
            self.ItemNum = ''.join(random.choices(string.ascii_letters, k=3)) +'-'+''.join(random.choices(string.digits, k=3)) +'-'+ type(self).__name__
        else:
            self.ItemNum = itemnum
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

class Loan():
    def __init__(self, MemberID:str, ItemNum:str):
        self.MemberID = MemberID
        self.ItemNumber = ItemNum
        self.LoanRef = ''.join(random.choices(string.ascii_letters + string.digits, k=8))


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
    itemdetails['title'] = item.title
    itemdetails['description'] = item.description
    itemdetails['type'] = type(item).__name__
    if type(item).__name__ == 'Book':
        itemdetails['isbn'] = item.ISBN
        itemdetails['publisher'] = item.publisher
        itemdetails['authors'] = item.authors
        if type(item).__name__ == 'Journal':
            itemdetails['volume'] = item.volume
            itemdetails['articlelist'] = item.articlelist

    return itemdetails


def jsontoitem(jsondict: dict):
    for i in jsondict:
        datadict = jsondict[i]
        print(datadict)


def loanformatter(loan: Loan):
    loandetails = {}
    loandetails['LoanRef'] = loan.LoanRef
    loandetails['MemberID'] = loan.MemberID
    loandetails['ItemNum'] = loan.ItemNumber





class Library():
    def __init__(self, name: str):
        self.Name = name
        self.Members = {}
        if os.path.exists(membersdirectory):
            with open(membersdirectory, 'r') as json_file:
                try:
                    self.Members = json.loads(json_file.read())
                except ValueError:
                    self.Members = {}
        self.Loans = {}
        if os.path.exists(loansdirectory):
            with open(loansdirectory, 'r') as json_file:
                try:
                    self.Loans = json.loads(json_file.read())
                except ValueError:
                    self.Loans = {}
        self.Items = {}
        if os.path.exists(itemdirectory):
            with open(itemdirectory, 'r') as json_file:
                try:
                    self.Items = json.loads(json_file.read())
                except ValueError:
                    self.Items = {}

    def savedata(self):
        with open(membersdirectory, 'w') as outfile:
            json.dump(self.Members, outfile, indent=4)
        with open(itemdirectory, 'w') as outfile:
            json.dump(self.Items, outfile, indent=4)
        with open(loansdirectory, 'w') as outfile:
            json.dump(self.Loans, outfile, indent=4)


    def new_member(self):
        name = input('Enter Name for Member')
        year = request_num_input('Please enter the year you were born', True)
        month = request_num_input('Please enter the month you were born', True)
        day = request_num_input('Please enter the day you were born', True)
        date_of_birth = date.datetime(year, month, day)
        addr1 = input('Enter Address Line 1')
        addr2 = input('Enter Address Line 2')
        town = input('Enter Town/City')
        county = input('Enter County')
        province = input('Enter Province')
        country = input('Enter state/country')
        postcode = input('Enter postcode')
        mem_add =Address(addr1,addr2,town,county,province,country,postcode)
        newmember = Member(name, mem_add, date_of_birth)
        self.Members[newmember.MemberID] = memberformatter(newmember)
        print(newmember)
        print('------------------')
        print(self.Members[newmember.MemberID])
        self.savedata()

    def searchlibraryitems(self):
        results_dic = {}
        search_results = list()
        search_results_string = list()
        search_term = input("Please enter keyword for search\n").lower()
        search_term = search_term.strip()

        inclusive = False
        match_all = input("Would you like an inclusive search or a contains-all search? ( i / c )")
        if match_all != 'c':
            print("defaulting to inclusive search")
            inclusive = True

        no_results_found = True  # assume that  there will be no search results
        while no_results_found == True:
            no_results_found = False
            for j in self.Items:
                keywords = set(search_term.split(' '))  # convert the user search into a SET of keywords
                for i in self.Items:
                    descset = set(self.Items[i]['description'].lower().split(' '))
                    # description match
                    if inclusive:  # If the search type is inclusive, results will contain all articles that contain each individual word
                        if len(keywords.intersection(descset)) > 0 and i not in search_results:
                            search_results.append(i)
                    else:
                        if keywords.issubset(descset) and i not in search_results:
                            search_results.append(i)
                    #title match
                    titleset = set(self.Items[i]['title'].lower().split(' '))
                    if inclusive:  # If the search type is inclusive, results will contain all articles that contain each individual word
                        if len(keywords.intersection(titleset)) > 0 and i not in search_results:
                            search_results.append(i)
                    else:
                        if keywords.issubset(titleset) and i not in search_results:
                            search_results.append(i)

            if len(search_results) < 1:
                no_results_found = True
                search_term = input("No Results found! Enter another keyword or (q) to return to main menu\n").lower()
                search_term.strip()
                if search_term == 'q':
                    return 0

        for i in range(0, len(search_results)):
            print(self.Items[search_results[i]]['title'])
        '''
        for i in range(0, len(search_results)):  # Essentially, every 4 results is grouped into a line and that line is added to the end string
            temp = ''
            if i > 0 and i % 4 == 0:
                temp = '----' + self.Items[search_results[i - 4]]['title'] + '----' + self.Items[search_results[i - 3]]['title'] + '----' + self.Items[search_results[
                    i - 2]]['title'] + '----' + self.Items[search_results[i - 1]]['title'] + '----'
                search_results_string.append(temp)
            if i == len(search_results) - 1 and len(search_results) % 4 != 0:
                temp = '----'
                remainder = (i + 1) % 4
                for r in range(0, remainder):
                    temp += self.Items[search_results[i - r]]['title'] + '----'
                search_results_string.append(temp)
        for s in search_results_string:  # Just printing out the rows of the string
            print(s + '\n')
        '''



'''
Reading
        if os.path.exists(membersdirectory):
            with open(membersdirectory, 'r') as json_file:
                try:
                    self.Members = json.loads(json_file.read())
                except ValueError:
                    self.Members = {}
                    
Writing 
        with open(membersdirectory, 'w') as outfile:
            json.dump(datastream, outfile, indent = 4)

                    
'''


class Application():
    def __init__(self):
        self.lib = Library('TUDublin Library')

    def CreateLoan(self, member: Member, item: Item):
            if item.ItemNum in self.Loans:
                print("Item already out on loan")
                return
            else:
                createdloan = Loan(member.MemberID, item.ItemNum)
                datastream = {}
                with open(loansdirectory, 'r') as json_file:
                    try:
                        datastream = json.loads(json_file.read())
                    except ValueError:
                        datastream = {}

                datastream[createdloan.LoanRef] = loanformatter(createdloan)
                with open(loansdirectory, 'w') as outfile:
                    json.dump(datastream, outfile, indent=4)