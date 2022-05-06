from projectclasses import *


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