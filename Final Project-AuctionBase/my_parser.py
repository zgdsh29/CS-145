
"""
FILE: skeleton_parser.py
------------------
Author: Firas Abuzaid (fabuzaid@stanford.edu)
Author: Perth Charernwattanagul (puch@stanford.edu)
Modified: 04/21/2014

Skeleton parser for CS145 programming project 1. Has useful imports and
functions for parsing, including:

1) Directory handling -- the parser takes a list of eBay json files
and opens each file inside of a loop. You just need to fill in the rest.
2) Dollar value conversions -- the json files store dollar value amounts in
a string like $3,453.23 -- we provide a function to convert it to a string
like XXXXX.xx.
3) Date/time conversions -- the json files store dates/ times in the form
Mon-DD-YY HH:MM:SS -- we wrote a function (transformDttm) that converts to the
for YYYY-MM-DD HH:MM:SS, which will sort chronologically in SQL.

Your job is to implement the parseJson function, which is invoked on each file by
the main function. We create the initial Python dictionary object of items for
you; the rest is up to you!
Happy parsing!
"""

import sys
from json import loads
from re import sub

columnSeparator = "|"

# Dictionary of months used for date transformation
MONTHS = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06',\
        'Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}

"""
Returns true if a file ends in .json
"""
def isJson(f):
    return len(f) > 5 and f[-5:] == '.json'

"""
Converts month to a number, e.g. 'Dec' to '12'
"""
def transformMonth(mon):
    if mon in MONTHS:
        return MONTHS[mon]
    else:
        return mon

"""
Transforms a timestamp from Mon-DD-YY HH:MM:SS to YYYY-MM-DD HH:MM:SS
"""
def transformDttm(dttm):
    dttm = dttm.strip().split(' ')
    dt = dttm[0].split('-')
    date = '20' + dt[2] + '-'
    date += transformMonth(dt[0]) + '-' + dt[1]
    return date + ' ' + dttm[1]

"""
Transform a dollar value amount from a string like $3,453.23 to XXXXX.xx
"""

def transformDollar(money):
    if money == None or len(money) == 0:
        return money
    return sub(r'[^\d.]', '', money)

def escapeQuote(string):
    return '"' + sub(r'"','""',string) + '"'

"""
Parses a single json file. Currently, there's a loop that iterates over each
item in the data set. Your job is to extend this functionality to create all
of the necessary SQL tables for your database.
"""
def parseItem (item,file):
        f=[]
        f.append(item['ItemID'])
        f.append("|")
        f.append(escapeQuote(item['Name']))
        f.append("|")
        f.append(transformDollar(item['Currently']))
        f.append("|")
        if "Buy_Price" in item:
            f.append(transformDollar(item['Buy_Price']))
        else:
            f.append("NULL")
        f.append("|")
        f.append(transformDollar(item['First_Bid']))
        f.append("|")
        f.append(transformDttm(item['Started']))
        f.append("|")
        f.append(transformDttm(item['Ends']))
        f.append("|")
        f.append(item['Seller']['UserID'])
        f.append("|")
        f.append(item['Number_of_Bids'])
        f.append("|")
        if item['Description']==None:
            f.append("NULL")
        else:
            f.append(escapeQuote(item['Description']))
        f.append("\n")
        for i in f :
            file.write(str(i))

def parseCategory(item,f):
        it=[]
        for i in item['Category']:
            it.append(item['ItemID'])
            it.append("|")
            it.append(i)
            it.append("\n")
        for j in it:
            f.write(str(j))


def parseUser(item,f):
         user_id=set()
         user=[]
         if item.get("Bids")!= None:
             for b in item.get("Bids"):
                 bidder = b['Bid']['Bidder']
                 user.append(bidder['UserID'])
                 user.append("|")
                 user_id.add(bidder['UserID'])
                 user.append(bidder['Rating'])
                 user.append("|")
                 if "Location" in bidder:
                     user.append(escapeQuote(bidder['Location']))
                 else:
                     user.append("NULL")
                 user.append("|")
                 if "Country" in bidder:
                     user.append(escapeQuote(bidder['Country']))
                 else:
                     user.append("NULL")
                 user.append("\n")
         if not item['Seller']['UserID'] in user_id:
             user.append(item['Seller']['UserID'])
             user.append("|")
             user.append(item['Seller']['Rating'])
             user.append("|")
             user.append(escapeQuote(item['Location']))
             user.append("|")
             user.append(escapeQuote(item['Country']))

         for u in user:
               f.write(str(u))
         f.write("\n")

def parseBids(item,f):
   
        b =[]
        if item.get('Bids')!= None:
            for bid in item.get('Bids'):
                b.append(item['ItemID'])
                b.append("|")
                b.append(bid['Bid']['Bidder']['UserID'])
                b.append("|")
                b.append(transformDttm(bid['Bid']['Time']))
                b.append("|")
                b.append(transformDollar(bid['Bid']['Amount']))
                b.append("\n")
        for i in b:
            f.write(str(i))





def parseJson(json_file):
    c = open("bids.dat","a")
    d = open("users.dat","a")
    e = open("category.dat","a")
    q = open("items.dat","a")
    with open(json_file, 'r') as f:
         items = loads(f.read())['Items'] # creates a Python dictionary of Items for the supplied json file
         for item in items:
             parseItem(item,q)
             parseCategory(item,e)
             parseUser(item,d)
             parseBids(item,c)


"""
Loops through each json files provided on the command line and passes each file
to the parser
"""
def main(argv):
    if len(argv) < 2:
        print >> sys.stderr, 'Usage: python skeleton_json_parser.py <path to json files>'
        sys.exit(1)
    # loops over all .json files in the argument
    for f in argv[1:]:
        if isJson(f):
            parseJson(f)
            print "Success parsing " + f

if __name__ == '__main__':
    main(sys.argv)
