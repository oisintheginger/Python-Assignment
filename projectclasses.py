import datetime as date
import random
import string
import os
import json

#Directories to avoid spelling errors.
membersdirectory = './members.json'
loansdirectory = './loans.json'
itemdirectory = './items.json'


def request_num_input(inp: str, intorfloat = False):
    """
    A utility function that returns an integer or float from a user input.
    Args:
        inp (str): This is the input message i.e 'Enter age'
        intorfloat (bool): Determines to return an integer or float. True for integer, defaults to false.
    """
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
    """A container class to help create addresses."""
    def __init__(self, AddressLine1:str, AddressLine2:str, Town:str, County:str, Province:str, Country:str, Postcode:str):
        """
        Args:
            AddressLine1 (str): first line of address
            AddressLine2 (str): second line of address
            Town (str): Town of address
            County (str): County of address
            Province (str): Province of address
            Country (str): Country of address
            Postcode (str): Postcode of address
        """
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
    """
    The defining class of a member, which makes it easier to convert into data via the memberformatter function.
    """
    def __init__(self, Name: str, address: Address, DOB: date.datetime, ID =''):
        """
        Args:
            Name (str): the name of the member.
            address (Address): the address of the member.
            DOB (date.datetime): the date of birth of the user.
            ID (str): this is the ID of the member, if no argument given, a random sequence will be used.
        """
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
    """
    The defining parent class of all types of items.

    Attributes:
    title : str
        This is the title of the item
    description : str
        This is the description of the item
    itemnum : str
        This is the unique identifier for the item
    """

    def __init__(self, title: str, description: str, itemnum = ' '):
        """
        Args:
            title (str): This is the title of the item
            description (str): This is the description of the item
            itemnum (str): This is the id number for the item within the system. If no argument is given, a randomised string sequence is generated.
        """
        if itemnum == ' ':
            self.ItemNum = ''.join(random.choices(string.ascii_letters, k=3)) +'-'+''.join(random.choices(string.digits, k=3)) +'-'+ type(self).__name__
        else:
            self.ItemNum = itemnum
        self.description = description
        self.title = title


class Book(Item):
    """
    Book class inherits from the parent Item class

    Attributes:
        isbn : str
            This is the ISBN (International Standard Book Number) of the book
        publisher : str
            This is the publisher of the book
        list of authors : list
            This is a list of authors of the book
        title : str
            This is the title of the item
        description : str
            This is the description of the item
        itemnum : str
            This is the unique identifier for the item
    """
    def __init__(self, ISBN: str, publisher: str, listofauthors: list, *args, **kwargs):
        """
        ISBN, publisher, listofauthors, title, description

        Args:
            ISBN (str): This is the ISBN (International Standard Book Number) of the book.
            publisher (str): This is the publisher of the book.
            listofauthors (list): This is a list of authors of the book.
            *args (str): Title-This is the title of the item, description - This is the description of the item, itemnum - This is the unique identifier for the item.
        """
        super(Book, self).__init__(*args, **kwargs)
        self.ISBN = ISBN
        self.publisher = publisher
        self.authors = listofauthors


class Journal(Book):
    """
        Journal class inherits from the parent Item class

        Attributes:
            volume : str
                This is the volume of the journal
            articlelist: list
                This is the list of articles that belong to the journal that can be found in the library inventory
            isbn : str
                This is the ISBN (International Standard Book Number) of the journal
            publisher : str
                This is the publisher of the journal
            list of authors : list
                This is a list of authors of the journal
            title : str
                This is the title of the journal
            description : str
                This is the description of the journal
            itemnum : str
                This is the unique identifier for the journal
    """
    def __init__(self, volume: str, articlelist: list, *args, **kwargs):
        """
            volume, article listISBN, publisher, listofauthors, title, description

            Args:
                volume (str): the volume number of the journal
                articlelist (list): This is the list of articles that belong to the journal that can be found in the library inventory
                *args (str):ISBN- This is the ISBN of the Journal, Publisher - this is the publisher of the journal, listofauthors- this is the list of authors Title-This is the title of the item, description - This is the description of the item, itemnum - This is the unique identifier for the item.
        """
        super(Journal, self).__init__(*args, **kwargs)
        self.volume = volume
        self.articlelist = articlelist


class Article(Item):
    """
        Article class inherits from the parent Item class

        Attributes:
            journalisbn : str
                This is the ISBN (International Standard Book Number) of the journal the article belongs to
            list of authors : list
                This is a list of authors of the article
            title : str
                This is the title of the article
            description : str
                This is the description of the article
            itemnum : str
                This is the unique identifier for the article
    """
    def __init__(self, journalisbn: Journal, listofauthors: list, *args, **kwargs):
        """
            Journal ISBN, listofauthors, title, description

            Args:
                journalisbn (str): This is the ISBN of the journal the article belongs to.
                listofauthors (list): This is a list of authors of the book.
                *args (str): Title-This is the title of the item, description - This is the description of the item, itemnum - This is the unique identifier for the item.
        """
        super(Article, self).__init__(*args, **kwargs)
        self.JournalISBN = journalisbn
        self.authors = listofauthors


class Digital(Item):
    """
        Digital class inherits from the parent Item class

        Attributes:
            file_type : str
                This is the file type of the digital media
            format : str
                This is the format of the digital media
            creator : str
                This is the creator of the digital media
            title : str
                This is the title of the digital media
            description : str
                This is the description of the digital media
            itemnum : str
                This is the unique identifier for the digital media
    """
    def __init__(self, file_type: str, format: str, creator: str, *args, **kwargs):
        """
            file_type, format, creator, listofauthors, title, description

            Args:
                file_type (str): This is the file extension of the digital media.
                format (list): This is the format of the digital media.
                creator (list): This is the creator of the digital media.
                *args (str): Title-This is the title of the item, description - This is the description of the item, itemnum - This is the unique identifier for the item.
        """
        super(Digital, self).__init__(*args, **kwargs)
        self.file_type = file_type
        self.format = format
        self.creator = creator


def memberformatter(member: Member):
    """
    Decodes an instance of the member class into a dictionary, so that it may be written into a json file. Returns a dictionary.
    Args:
        member (Member): This is the Member instance that is to be decoded into a json-legible dictionary.

    Returns:
        A dictionary representing member data
    """
    memberdetails = {}
    memberdetails['name'] = member.Name
    memberdetails['address'] = [member.MemberAddress.AddressLine1, member.MemberAddress.AddressLine2, member.MemberAddress.Town, member.MemberAddress.County, member.MemberAddress.Province, member.MemberAddress.Country, member.MemberAddress.Postcode]
    memberdetails['dob'] = str(member.DOB)
    return memberdetails


def jsontomember(jsondictionary: dict, memberID: str):
    """
    Decodes a dictionary to construct an instanceof the member class. Returns an instance of the member class.
    Args:
        jsondictionary (dict): This is the dictionary that represents the member to create an instance of
        memberID (str): The id of the member we wish to instantiate
    Returns:
        Instance of member class representative of saved member data
    """
    memberdatadict = jsondictionary[memberID]
    dataname = memberdatadict['name']
    dataaddress = Address(memberdatadict['address'][0], memberdatadict['address'][1], memberdatadict['address'][2], memberdatadict['address'][3], memberdatadict['address'][4],memberdatadict['address'][5],memberdatadict['address'][6])
    dataDOB = memberdatadict['dob']
    returnable = Member(dataname,dataaddress,dataDOB, memberID)
    return returnable

def itemformatter(item: Item):
    """
    Decodes an instance of the item class into a dictionary, so that it may be written into a json file. Returns a dictionary.
    Args:
        item (Item): This is the Item instance that is to be decoded into a json-legible dictionary.

    Returns:
        A dictionary representing item data
    """
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
    """
    [DEPRECATED]
    Decodes a dictionary to construct an instance of the item class. Returns an instance of the item class.
    Args:
        jsondict (dict): This is the dictionary that represents the item to create an instance of.
    """
    for i in jsondict:
        datadict = jsondict[i]
        print(datadict)


def numbered_menu(l: list):
    """
    Utility class that automatically generates a menu from a list of options, and guarantees user input reflects index within option range.
    Args:
        l (list): This is the list of options to create a menu from.
    Returns:
        user input -1, which can be used as a selection index.
    """
    for i in range(0, len(l)):
        print('{0}. {1}'.format(i+1, l[i]))

    inp = request_num_input('Please select an option (1 - {0})'.format(len(l)), True)
    while inp -1 <0 or inp-1>=len(l):
        inp = request_num_input('Invalid option. Please select an option (1 - {0})'.format(len(l)), True)
    return inp -1


def list_of_strings(message: str):
    """
    Utility class that asks for a non-specified number of string inputs. It is used for creating multiple authors.
    Args:
        message (str): This is the prompt that will be used for the user input.
    Returns:
        newlist, the list of strings the user has created.
    """
    newlist = list()
    while True:
        inp = input(message +' (q to quit)')
        if inp == 'q':
            break
        newlist.append(inp)
    return newlist


def print_dic(d: dict):
    """"
    Utility class that prints a dictionary in a slightly easier to read format.
    Args:
        d (dict): The dictionary to print out
    """
    for a in d:
        print('{0}:    {1}'.format(a, d[a]))


class Library:
    """
    The Library class, hosts the data of the library system i.e. Members, Items, and Loans directory.

    Attributes:
        Name (str): name of library
        Members (dict): dictionary of members
        Loans (dict): dictionary of loans
        Items (dict): dictionary of items
    """
    def __init__(self, name: str):
        """
        Creates instance of the library class. Populates the members,items, and loans directories by reading from disk.

        Args:
            name (str): the name of the library
        """
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
        """
        Utility function that allows for easier writing of data to disk.
        """
        with open(membersdirectory, 'w') as outfile:
            json.dump(self.Members, outfile, indent=4)
        with open(itemdirectory, 'w') as outfile:
            json.dump(self.Items, outfile, indent=4)
        with open(loansdirectory, 'w') as outfile:
            json.dump(self.Loans, outfile, indent=4)

    def new_member(self):
        """
        Method to creating and entering a new member into the library's files. Is accessed through the application.
        """
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
        """
        Method to removing a new member from the library's files. Is accessed through the application. Cancels if the member has outstanding loans.
        """
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
        """
        Searches through the items in the library using user input as search terms. Borrowed and adapted from my previous assigment.
        """
        search_results = list()
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
        """
        Method to creating and entering a new item into the library's files. Acts as a menu for other specialised functions. Is accessed through the application.
        """
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
        """
        Method to removing a new item from the library's files. Is accessed through the application. Cancels if the item has outstanding loans.
        """
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
        """
        Specialised Function for transforming user input into a book instance, and entry into the library's item directory.
        """
        title = input('Enter Name for Book')
        description = input('Enter Description for Book')
        authors = list_of_strings('Enter Author Name')
        publisher = input('Enter Publisher for Book')
        isbn = input('Enter ISBN for Book')

        newbook = Book(isbn, publisher, authors, title, description)
        self.Items[newbook.ItemNum] = itemformatter(newbook)
        self.savedata()

    def create_journal(self):
        """
        Specialised Function for transforming user input into a journal instance, and entry into the library's item directory.
        """
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
        """
        Specialised Function for transforming user input into an article instance, and entry into the library's item directory.
        """
        title = input('Enter Name for Article')
        description = input('Enter Description for Article')
        authors = list_of_strings('Enter Author Name')
        isbn = input('Enter ISBN for Journal of Article')
        newarticle = Article(isbn, authors, title, description)
        self.Items[newarticle.ItemNum] = itemformatter(newarticle)
        self.savedata()

    def create_digital(self):
        """
        Specialised Function for transforming user input into a digital media instance, and entry into the library's item directory.
        """
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
        """
        Utility function to create a list of items of a particular type in the library directory.

        Args:
            itemtype (Item): the type of item to display
        """
        result_list = list()
        for a in self.Items:
            if self.key_val_match('type',itemtype.__name__,self.Items[a]) is True:
                result_list.append((a, self.Items[a]['title']))
        for r in result_list:
            print(r)

    def create_loan(self, member_id: str, item_id, return_date: date.datetime):
        """
        Takes a member and an item and creates an entry in the library's loan directory to store the data. Used in lieu of a dedicated Loan class, as it is unnecessary for function.

        Args:
            member_id (str): ID of the member who is taking out the loan.
            item_id (str): ID of the member who is being loaned out.
            return_date (date.datetime): the date the Loan is due to be returned at.
        """
        loan_dic = dict()
        loan_dic['member'] = member_id
        loan_dic['item'] = item_id
        loan_dic['due'] = str(return_date)
        new_ref = ''.join(random.choices(string.ascii_lowercase, k=4)) + '-' + ''.join(random.choices(string.digits, k=4))
        loan_dic['reference'] = new_ref
        self.Loans[new_ref] = loan_dic
        self.savedata()

    def return_loan(self, member: str):
        """
        Takes a member and displays their outstanding loans. User can then choose to return a loaned item.

        Args:
            member (str): ID of the member who is returning the item.
        """
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
        """
        Similar to the display_items_of_type method, however, this method returns a list of those items.

        Args:
            itemtype (Item): The type of item to be returned.

        Returns:
            result_list of all items of given type.
        """
        result_list = list()
        for a in self.Items:
            if self.key_val_match('type', itemtype.__name__, self.Items[a]) is True:
                result_list.append((a,self.Items[a]['title']))
        return result_list

    def modify_items(self):
        """
        Method for modifying items within the library.
        """
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
        """
        Method for modify the items, broken from modify_item to increase readability, although, it may be compacted into one method without issue.
        Args:
            itemtype (Item): the type of item to modify.
        """
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
        """
        Method for modifying an individual article. Displays all relevant details, and presents the user with options to modify.

        Args:
            item_num (str): The item number of the article to modify.
        """
        print_dic(self.Items[item_num])
        print('Choose an Option')
        options = ["Modify Article's Journal ISBN", 'Modify Article Authors', 'Modify Title', 'Modify Description','Cancel']
        c = numbered_menu(options)
        if c == 0:
            new_ISBN = input('Enter new ISBN').lower()
            self.Items[item_num]['journalisbn'] = new_ISBN
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
            return
        if c == 3:
            desc = input('Enter new Description')
            self.Items[item_num]['description'] = desc
            self.savedata()
            return
        else:
            return

    def mod_journal(self, item_num: str):
        """
        Method for modifying an individual journal. Displays all relevant details, and presents the user with options to modify.

        Args:
            item_num (str): The item number of the journal to modify.
        """
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
        """
        Method for modifying an individual book. Displays all relevant details, and presents the user with options to modify.

        Args:
            item_num (str): The item number of the book to modify.
        """
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
        """
        Method for modifying an individual digital media. Displays all relevant details, and presents the user with options to modify.

        Args:
            item_num (str): The item number of the digital media to modify.
        """
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
        """
        Utility function to check if the a dictionary value is equal to a given value

        Args:
            key (str): key to access value within dic dictionary.
            value (str): value we wish to compare against the dictionary's value.
            dic (dict): the dictionary we wish to compare against.
        """
        return dic[key] == value



class Application():
    """
    The Application class, hosts an instance of the library class, and manages the currently signed in member.

    Attributes:
        lib (Library): instance of the library
        signed_in_member (str): Member ID of the currently signed in member
        signed_in (bool): indicator to whether a member is 'signed-in'
    """
    def __init__(self):
        self.lib = Library('TUDublin Library')
        self.signed_in_member = ''
        self.signed_in = False

    def sign_in(self, inp_id: str):
        """
        Method for signing in. Uses two methodologies. Searches both through names and member ID's within the Library's members directory.
        In the case where there are two people of the same name, those results are appended to a list. The user can then choose to pick a member to sign in as.

        Args:
            inp_id (str): The input string which can be a member ID or a member name.
        Returns:
            member id as a string, or if none found, returns an empty string.
        """
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

