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
            self.MemberID = ''.join(random.choices(string.ascii_lowercase + string.digits, k=16))
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


class Digital(Item):
    def __init__(self, file_type: str, format: str, creator: str, *args, **kwargs):
        super(Digital, self).__init__(*args, **kwargs)
        self.file_type = file_type
        self.format = format
        self.creator = creator


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
    if type(item).__name__ == 'Digital':
        itemdetails['format'] = item.format
        itemdetails['file_type'] = item.file_type
        itemdetails['creator'] = item.creator

    return itemdetails


def jsontoitem(jsondict: dict):
    for i in jsondict:
        datadict = jsondict[i]
        print(datadict)


def numbered_menu(l: list):
    for i in range(0, len(l)):
        print('{0}. {1}'.format(i+1, l[i]))

    inp = request_num_input('Please select an option (1 - {0})'.format(len(l)), True)
    while inp -1 <0 or inp-1>=len(l):
        inp = request_num_input('Invalid option. Please select an option (1 - {0})'.format(len(l)), True)
    return inp -1


def list_of_strings(message: str):
    newlist = list()
    while True:
        inp = input(message +' (q to quit)')
        if inp == 'q':
            break
        newlist.append(inp)
    return newlist


def print_dic(d : dict):
    for a in d:
        print('{0}:    {1}'.format(a, d[a]))

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
        mem_add = Address(addr1,addr2,town,county,province,country,postcode)
        newmember = Member(name, mem_add, date_of_birth)
        self.Members[newmember.MemberID] = memberformatter(newmember)
        self.savedata()

    def delete_member(self):
        if len(self.Members) <1:
            print("Library Doesn't have any members yet!")
            return
        options_list = list()
        for m in self.Members:
            options_list.append((m, self.Members[m]['name']))
        options_list.append('Cancel')
        c = numbered_menu(options_list)
        if c == len(options_list)-1:
            print('Cancelled Deletion')
        else:
            for l in self.Loans:
                if self.key_val_match('member', options_list[c][0], self.Loans[l]):
                    print('Cannot delete a member with outstanding loans. Cancelling')
                    return
            print('Please Confirm Deletion of: {0}'.format(self.Members[options_list[c][0]]['name']))
            confirm = ['Yes', 'No']
            f = numbered_menu(confirm)
            if f == 0:
                del self.Members[options_list[c][0]]
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
                    elif self.Items[i]['type'] == 'Digital':
                        formatset = set(self.Items[i]['format'].lower().split('_'))
                        if inclusive:  # If the search type is inclusive, results will contain all articles that contain each individual word
                            if len(keywords.intersection(formatset)) > 0 and i not in search_results:
                                search_results.append(i)
                        else:
                            if keywords.issubset(formatset) and i not in search_results:
                                search_results.append(i)

            if len(search_results) < 1:
                no_results_found = True
                search_term = input("No Results found! Enter another keyword or (q) to return to main menu\n").lower()
                search_term.strip()
                if search_term == 'q':
                    return 0


        for i in range(0, len(search_results)):
            print(self.Items[search_results[i]]['title'])

        print('Would you like to display an items details?')
        options = ['Yes', 'No']
        choice = numbered_menu(options)
        if choice == 0:
            options = list()
            print('Choose by number.')
            for i in search_results:
                options.append(self.Items[i]['title'])
            choice = numbered_menu(options)
            todisplay = search_results[choice]
            print_dic(self.Items[todisplay])

    def add_item(self):
        while True:
            print('Choose Item To Add \n 1. Book \n 2. Journal \n 3. Article \n 4. Digital Media \n q Quit')
            inp = input()
            if inp == '1':
                self.create_book()
            elif inp == '2':
                self.create_journal()
            elif inp == '3':
                self.create_article()
            elif inp == '4':
                self.create_digital()
            elif inp == 'q':
                return
            else:
                print('Please enter a valid option')

    def delete_item(self):
        if len(self.Items) <1:
            print("Library Doesn't have any items yet!")
            return
        options_list = list()
        for m in self.Items:
            options_list.append((m, self.Items[m]['title']))
        options_list.append('Cancel')
        c = numbered_menu(options_list)
        if c == len(options_list) - 1:
            print('Cancelled Deletion')
        else:
            for l in self.Loans:
                if self.key_val_match('item', options_list[c][0], self.Loans[l]):
                    print('Cannot delete an item with outstanding loans. Cancelling')
                    return
            print('Please Confirm Deletion of: {0}'.format(self.Items[options_list[c][0]]['title']))
            confirm = ['Yes', 'No']
            f = numbered_menu(confirm)
            if f == 0:
                del self.Items[options_list[c][0]]
                self.savedata()

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
        self.savedata()

    def create_article(self):
        title = input('Enter Name for Article')
        description = input('Enter Description for Article')
        authors = list_of_strings('Enter Author Name')
        isbn = input('Enter ISBN for Journal of Article')
        newarticle = Article(isbn, authors, title, description)
        self.Items[newarticle.ItemNum] = itemformatter(newarticle)
        self.savedata()

    def create_digital(self):
        title = input('Enter Name for Digital Media')
        description = input('Enter Description for Digital Media')
        creator = input('Enter Creator for Digital Media')
        formats = ['VIDEO_FILE', 'IMAGE_FILE','AUDIO_FILE','OTHER_FILE']
        f = numbered_menu(formats)
        format = formats[f]
        filetypes = ['MP4', 'JPG', 'MP3', 'unknown file extension']
        ft = numbered_menu(filetypes)
        filetype = filetypes[ft]
        newdigital = Digital(filetype, format, creator,title, description)
        self.Items[newdigital.ItemNum] = itemformatter(newdigital)
        self.savedata()

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
        loan_dic['reference'] = new_ref
        self.Loans[new_ref] = loan_dic
        self.savedata()

    def return_loan(self, member: str):
        results = list()
        for l in self.Loans:
            if self.key_val_match('member', member, self.Loans[l]):
                results.append((l,self.Loans[l]['item'],self.Loans[l]['due']))
        print("{0}'s Loans Are:".format(self.Members[member]['name']))
        for i in range(0,len(results)):
            print('{0}.'.format(i+1), self.Items[results[i][1]]['title'])
        if len(results)<1:
            print(self.Members[member]['name'], 'has no loans. Returning.')
            return
        inp = request_num_input('Please select the item you wish to return (1 - {0}) ({1} to cancel)'.format(str(len(results)),str(len(results)+1)), True)
        while inp < 1 or inp > len(results)+1:
            inp = request_num_input('Invalid selection! Please select the item you wish to return (1 - {0}) ({1} to return)'.format(str(len(results)),str(len(results)+1)), True)
        if inp == len(results)+1:
            return
        else:
            del self.Loans[results[inp-1][0]]
            self.savedata()

    def get_items_of_type(self, itemtype: Item):
        result_list = list()
        for a in self.Items:
            if self.key_val_match('type', itemtype.__name__, self.Items[a]) is True:
                result_list.append((a,self.Items[a]['title']))
        return result_list

    def modify_items(self):
        print('Choose an Option')
        options= ['Modify Article','Modify Journal','Modify Book','Modify Digital Media', 'Return']
        c = numbered_menu(options)
        if c == 0:
            self.modify_item_type(Article)
        if c == 1:
            self.modify_item_type(Journal)
        if c == 2:
            self.modify_item_type(Book)
        if c == 3:
            self.modify_item_type(Digital)
        else:
            return

    def modify_item_type(self, itemtype: Item):
        items = self.get_items_of_type(itemtype)
        if len(items) < 1:
            print('No Items of Type to Modify')
            return
        item_names = list()
        for i in items:
            item_names.append(i[1])
        print('Choose an item to modify')
        c = numbered_menu(item_names)
        if c == 0 or c >= len(items):
            if itemtype == Article:
                self.mod_article(items[c][0])
            if itemtype == Journal:
                self.mod_journal(items[c][0])
            if itemtype == Book:
                self.mod_book(items[c][0])
            if itemtype == Digital:
                self.mod_digital(items[c][0])
        else:
            return

    def mod_article(self, item_num: str):
        print_dic(self.Items[item_num])
        print('Choose an Option')
        options = ["Modify Article's Journal ISBN", 'Modify Article Authors', 'Modify Title', 'Modify Description','Cancel']
        c = numbered_menu(options)
        if c == 0:
            new_ISBN = input('Enter new ISBN').lower()
            self.Items[item_num]['journalisbn'] = new_ISBN
            self.savedata()
        if c == 1:
            new_authors = list_of_strings('Enter New List of Authors')
            self.Items[item_num]['authors'] = new_authors
            self.savedata()
        if c == 2:
            new_title = input('Enter new title')
            self.Items[item_num]['title'] = new_title
            self.savedata()
            return
        if c == 3:
            desc = input('Enter new Description')
            self.Items[item_num]['description'] = desc
            self.savedata()
            return
        else:
            return

    def mod_journal(self, item_num: str):
        print_dic(self.Items[item_num])
        print('Choose an Option')
        options = ["Modify Journal ISBN", 'Modify Journal Authors', 'Populate Article List from Library Inventory','Modify Title', 'Modify Description','Cancel']
        c = numbered_menu(options)
        if c == 0:
            new_ISBN = input('Enter new ISBN').lower()
            self.Items[item_num]['isbn'] = new_ISBN
            self.savedata()
            return
        if c == 1:
            new_authors = list_of_strings('Enter New List of Authors')
            self.Items[item_num]['authors'] = new_authors
            self.savedata()
            return
        if c == 2:
            all_articles = self.get_items_of_type(Article)
            list_to_add = list()
            for aa in all_articles:
                if self.key_val_match('journalisbn', self.Items[item_num]['isbn'], self.Items[aa[0]])\
                        and aa not in self.Items[item_num]['articlelist']:
                    list_to_add.append(aa)
            if len(list_to_add)> 0:
                self.Items[item_num]['articlelist'] = list_to_add
            self.savedata()
            return
        if c == 3:
            new_title = input('Enter new title')
            self.Items[item_num]['title'] = new_title
            self.savedata()
            return
        if c == 4:
            desc = input('Enter new Description')
            self.Items[item_num]['description'] = desc
            self.savedata()
            return
        else:
            return

    def mod_book(self, item_num:str):
        print_dic(self.Items[item_num])
        print('Choose an Option')
        options = ["Modify Book ISBN", 'Modify Book Authors','Modify Title', 'Modify Description','Cancel']
        c = numbered_menu(options)
        if c == 0:
            new_ISBN = input('Enter new ISBN').lower()
            self.Items[item_num]['isbn'] = new_ISBN
            self.savedata()
            return
        if c == 1:
            new_authors = list_of_strings('Enter New List of Authors')
            self.Items[item_num]['authors'] = new_authors
            self.savedata()
            return
        if c == 2:
            new_title = input('Enter new title')
            self.Items[item_num]['title'] = new_title
            self.savedata()
        if c == 3:
            desc = input('Enter new Description')
            self.Items[item_num]['description'] = desc
            self.savedata()
            return
        else:
            return

    def mod_digital(self, item_num:str):
        print_dic(self.Items[item_num])
        print('Choose an Option')
        options = ["Modify Title", 'Modify Description', 'Cancel']
        c = numbered_menu(options)
        if c == 0:
            title = input('Enter new Title')
            self.Items[item_num]['title'] = title
            self.savedata()
            return
        if c == 1:
            desc = input('Enter new Description')
            self.Items[item_num]['description'] = desc
            self.savedata()
            return
        else:
            return

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
        self.signed_in_member = ''
        self.signed_in = False

    def sign_in(self, inp_id: str):
        names_list = list()
        for m in self.lib.Members:
            if m in inp_id:
                self.signed_in = True
                self.signed_in_member = m
                return m
            elif inp_id == self.lib.Members[m]['name'].lower():
                names_list.append((m, inp_id))
        if len(names_list) == 1:
            self.signed_in_member = names_list[0][0]
            self.signed_in = True
            return names_list[0][0]
        elif len(names_list)>1:
            for n in range(0,len(names_list)):
                print(n+1, names_list[n])
            selection = request_num_input('Please select member to sign in as. ')
            if selection <1 or selection > len(names_list):
                print('Invalid selection. Returning')
                return ''
            else:
                self.signed_in_member = names_list[int(selection)-1][0]
                self.signed_in = True
                return names_list[int(selection)-1][0]
        return ''

