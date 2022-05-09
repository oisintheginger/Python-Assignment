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
import webbrowser

'''
TO DO:
-> Create Fine Functionality for late returns

'''


def setup(lib: Library):
    """
        An automated function that creates an instance of an application,
        which holds the sign-in information and an instance of a library.
        Also creates a selection of starter members and starter items, writing them to json files.
        Args:
            lib (Library): instance of a Library to set up
    """
    if os.path.exists(membersdirectory):
        os.remove(membersdirectory)
    if os.path.exists(loansdirectory):
        os.remove(loansdirectory)
    if os.path.exists(itemdirectory):
        os.remove(itemdirectory)

    #Creating Starting Members and Addresses
    PhilipAdd = Address('8024', 'Doyle Avenue', 'Roscommon Town', 'Roscommon', 'Munster', 'Ireland', 'A73MX91')
    Philip = Member('Philip', PhilipAdd, date.datetime.now())

    MaryAdd = Address('79', 'Cliff Road', 'Galway City', 'Galway', 'Connaught', 'Ireland', 'E94XM23')
    Mary = Member('Mary', MaryAdd, date.datetime.now())

    JimAdd = Address('100', 'Skid Row', 'Chicago', 'Chicago', 'Illinois', 'United States of America', 'M90TU32')
    Jim = Member('Jim', JimAdd, date.datetime.now())

    ChloeAdd = Address('27', 'Mill Lane', 'Trim', 'Meath', 'Leinster', 'Ireland', 'P92VI65')
    Chloe = Member('Mary', ChloeAdd, date.datetime.now())

    #creating a dictionary of members. Members are formatted using the memberformatter function
    datastream = dict()
    datastream[Philip.MemberID] = memberformatter(Philip)
    datastream[Mary.MemberID] = memberformatter(Mary)
    datastream[Jim.MemberID] = memberformatter(Jim)
    datastream[Chloe.MemberID] = memberformatter(Chloe)

    #writing the datastream dictionary to the membersdirectory file
    with open(membersdirectory, 'w') as outfile:
        json.dump(datastream, outfile, indent = 4)

    #repeating previous steps to create library inventory
    datastream = dict()
    newItem = Book('X49932-18839', 'Penguin', ['Author of the Book'], 'The Wind and the Willows','An old story that I do not know the plot of.')

    newjournal = Journal(1, ['article1'],'XHSHBF-BGHBG', 'Elsevier', ['Compiled By'], 'New England Journal of Medicine', 'A journal that is about medicine')

    newarticle = Article('XHSHBF-BGHBG',['Article Author 1', 'Article Author 2', 'Article Author 3'], 'Funny Article Title','Describing the funny article')

    datastream[newItem.ItemNum] = itemformatter(newItem)
    datastream[newjournal.ItemNum] = itemformatter(newjournal)
    datastream[newarticle.ItemNum] = itemformatter(newarticle)
    with open(itemdirectory, 'w') as outfile:
        json.dump(datastream, outfile, indent = 4)

    #setting the refreshing the library data dictionaries, by reading the files just saved to
    if os.path.exists(membersdirectory):
        with open(membersdirectory, 'r') as json_file:
            try:
                lib.Members = json.loads(json_file.read())
            except ValueError:
                lib.Members = {}
    if os.path.exists(loansdirectory):
        with open(loansdirectory, 'r') as json_file:
            try:
                lib.Loans = json.loads(json_file.read())
            except ValueError:
                lib.Loans = {}
    if os.path.exists(itemdirectory):
        with open(itemdirectory, 'r') as json_file:
            try:
                lib.Items = json.loads(json_file.read())
            except ValueError:
                lib.Items = {}


def search_by_item_category(app: Application):
    """
    A buffer method that acts as a menu to display items by type. Uses an app as a parameter,
    so to access its library to use its display_items_of_type method
    Args:
        app (Application): instance of an application that holds the current library
    """
    while True:
        print('Display By: \n 1. Book \n 2. Journal\n 3. Article \n 4. Digital Media \n q. Return')
        inp = input()
        if inp =='1':
            app.lib.display_items_of_type(Book)
        elif inp =='2':
            app.lib.display_items_of_type(Journal)
        elif inp =='3':
            app.lib.display_items_of_type(Article)
        elif inp == '4':
            app.lib.display_items_of_type(Digital)
        elif inp == 'q':
            break


def sign_in_menu(app: Application):
    """
    Buffer method to sign in as a library member
    Args:
        app (Application): instance of an application that will hold sign-in information
    """
    inp = input('Please enter a valid member ID number or name')
    inp = inp.lower()
    return app.sign_in(inp)


def borrow_menu(app: Application, memberid: str):
    """
    The borrow menu both displays available items and creates the loan entries in the library's
    loans directory. It cancels if there are no available items.
    Args:
        app (Application): instance of an application
        memberid (str): member ID string for use in the borrowing function.

    """
    #creates a list of available items and prints them in a menu
    item_list_display = list()
    unavailable_list = list()
    for l in app.lib.Loans:
        unavailable_list.append(app.lib.Loans[l]['item'])
    for a in app.lib.Items:
        if a not in unavailable_list:
            item_list_display.append((app.lib.Items[a]['title'], a))
    if len(item_list_display)<1:
        print('No Items Available. Returning.')
        return
    for i in range(0,len(item_list_display)):
        print('{0}. '.format(i+1),item_list_display[i][0],'------------', item_list_display[i][1],'\n')
    inp = request_num_input('Please select the item you would like to borrow (another number to quit)', True)
    if inp < 1 or inp >= len(item_list_display):
        print('Cancelling')
        return
    if inp in list(range(1, len(item_list_display)+1)):
        print(item_list_display[inp-1])
    con = request_num_input('Please confirm this loan request\n 1. Yes \n 2. No', True)
    if con == 1:
        app.lib.create_loan(memberid, item_list_display[inp-1][1], date.datetime.today() + date.timedelta(weeks=2))


def return_item_menu(app: Application, memberID:str):
    """
    Accesses the library's return_loan method, passing in the currently signed in member as a parameter.
    Args:
        app (Application): instance of an application
        memberid (str): member ID string for use in the return item function.
    """
    app.lib.return_loan(memberID)


def staff_functions_menu(app: Application):
    """
    The staff functions are locked away in a separate menu. If there were to be a full implementation,
    this would be locked with a password. However, due to the scale of this project, this would make it slower
    to test.
    Functions include the creation/destruction of members and items within the library files.
    Args:
        app (Application): instance of an application
    """
    print('Choose an option:')
    options = ['Create Member','Create Item','Delete Member', 'Delete Item', 'Return']
    c = numbered_menu(options)
    if c == 0:
        app.lib.new_member()
    if c == 1:
        app.lib.add_item()
    if c == 2:
        app.lib.delete_member()
    if c == 3:
        app.lib.delete_item()
    else:
        return



def main():
    """
    Entry point to the application. Displays the options available to the user.
    """
    app = Application()
    signed_in_member = ''
    while True:
        if signed_in_member in app.lib.Members:
            print(('Signed in as {0}, {1}'.format(app.lib.Members[signed_in_member]['name'], signed_in_member))*app.signed_in)
        print('Options \n 1. Setup \n 2. Sign In '
              '\n 3. Search Library \n 4. Staff Functions '
              '\n 5. Display Items \n 6. Loan an Item'
              '\n 7. Return an Item \n 8. Modify Item \n *. Quit')
        inp = request_num_input('', True)
        if inp ==1:
            setup(app.lib)
        elif inp == 2:
            signed_in_member = sign_in_menu(app)
        elif inp == 3:
            app.lib.searchlibraryitems()
        elif inp ==4:
            staff_functions_menu(app)
        elif inp == 5:
            search_by_item_category(app)
        elif inp == 6:
            if not app.signed_in:
                print('Must Be Signed in to borrow a book')
                continue
            borrow_menu(app, signed_in_member)
        elif inp == 7:
            if not app.signed_in:
                print('Must Be Signed in to Return a book')
                continue
            return_item_menu(app, signed_in_member)
        elif inp == 8:
            app.lib.modify_items()
        else:
            break


if __name__ == '__main__':
    main()
