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
        super(Journal, self).__init__(*args, **kwargs)
        self.volume = volume
        self.articlelist = articlelist


class Article(Item):
    def __init__(self, journalisbn: Journal, listofauthors: list, *args, **kwargs):
        super(Article, self).__init__(*args, **kwargs)
        self.JournalISBN = journalisbn
        self.authors = listofauthors

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
    itemdetails = {}
    itemdetails['itemnumber'] = item.ItemNum
    itemdetails['title'] = item.title
    itemdetails['description'] = item.description
    itemdetails['type'] = type(item).__name__
    if type(item).__name__ == 'Book':
        itemdetails['isbn'] = item.ISBN
        itemdetails['publisher'] = item.publisher
        itemdetails['authors'] = item.authors
    if type(item).__name__ == 'Journal':
        itemdetails['isbn'] = item.ISBN
        itemdetails['publisher'] = item.publisher
        itemdetails['authors'] = item.authors
        itemdetails['volume'] = item.volume
        itemdetails['articlelist'] = item.articlelist
    if type(item).__name__ == 'Article':
        itemdetails['journalisbn'] = item.JournalISBN
        itemdetails['authors'] = item.authors
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



def list_of_strings(message: str):
    newlist = list()
    while True:
        inp = input(message +' (q to quit)')
        if inp == 'q':
            break
        newlist.append(inp)
    return newlist

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
                    itemnumset = set(self.Items[i]['itemnumber'].lower().split(' '))
                    if inclusive:  # If the search type is inclusive, results will contain all articles that contain each individual word
                        if len(keywords.intersection(itemnumset)) > 0 and i not in search_results:
                            search_results.append(i)
                    else:
                        if keywords.issubset(itemnumset) and i not in search_results:
                            search_results.append(i)
                    if self.Items[i]['type'] == 'Book' or self.Items[i]['type'] == 'Journal':
                        isbnset = set(self.Items[i]['isbn'].lower().split(' '))
                        if inclusive:  # If the search type is inclusive, results will contain all articles that contain each individual word
                            if len(keywords.intersection(isbnset)) > 0 and i not in search_results:
                                search_results.append(i)
                        else:
                            if keywords.issubset(isbnset) and i not in search_results:
                                search_results.append(i)
                    elif self.Items[i]['type'] == 'Article':
                        isbnset = set(self.Items[i]['journalisbn'].lower().split(' '))
                        if inclusive:  # If the search type is inclusive, results will contain all articles that contain each individual word
                            if len(keywords.intersection(isbnset)) > 0 and i not in search_results:
                                search_results.append(i)
                        else:
                            if keywords.issubset(isbnset) and i not in search_results:
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

    def add_item(self):
        while True:
            print('Choose Item To Add \n 1. Book \n 2. Journal \n 3. Article \n q Quit')
            inp = input()
            if inp == '1':
                self.create_book()
            elif inp == '2':
                self.create_journal()
            elif inp == '3':
                self.create_article()
            elif inp == 'q':
                return
            else:
                print('Please enter a valid option')

    def create_book(self):
        title = input('Enter Name for Book')
        description = input('Enter Description for Book')
        authors = list_of_strings('Enter Author Name')
        publisher = input('Enter Publisher for Book')
        isbn = input('Enter ISBN for Book')

        newbook = Book(isbn, publisher, authors, title, description)
        self.Items[newbook.ItemNum] = itemformatter(newbook)
        print(newbook)
        print('------------------')
        print(self.Items[newbook.ItemNum])
        self.savedata()

    def create_journal(self):
        title = input('Enter Name for Journal')
        description = input('Enter Description for Journal')
        authors = list_of_strings('Enter Author Name')
        publisher = input('Enter Publisher for Journal')
        isbn = input('Enter ISBN for Journal')
        vol = str(request_num_input('Enter a Volume Number', True))
        articlelist = list_of_strings('Enter Article Item Number')
        newjournal = Journal(vol, articlelist,isbn, publisher, authors, title, description)
        self.Items[newjournal.ItemNum] = itemformatter(newjournal)
        print(newjournal)
        print('------------------')
        print(self.Items[newjournal.ItemNum])
        self.savedata()

    def create_article(self):
        title = input('Enter Name for Article')
        description = input('Enter Description for Article')
        authors = list_of_strings('Enter Author Name')
        isbn = input('Enter ISBN for Journal of Article')
        newarticle = Article(isbn, authors, title, description)

    def display_items_of_type(self, itemtype: Item):
        result_list = list()
        for a in self.Items:
            if self.key_val_match('type',itemtype.__name__,self.Items[a]) is True:
                result_list.append((a, self.Items[a]['title']))
        for r in result_list:
            print(r)

    def create_loan(self, member_id: str, item_id, return_date: date.datetime):
        loan_dic = dict()
        loan_dic['member'] = member_id
        loan_dic['item'] = item_id
        loan_dic['due'] = str(return_date)
        new_ref = ''.join(random.choices(string.ascii_lowercase, k=4)) + '-' + ''.join(random.choices(string.digits, k=4))

        loan_dic['reference'] = ''.join(random.choices(string.ascii_lowercase, k=4)) + '-' + ''.join(random.choices(string.digits, k=4))
        self.Loans[new_ref] = loan_dic
        self.savedata()

    def key_val_match(self, key: str, value: str, dic: dict()):
        return dic[key] == value




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

