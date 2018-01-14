import web
import sys
db = web.database(dbn='sqlite',
        db='AuctionBase.db' #TODO: add your SQLite database filename
    )

######################BEGIN HELPER METHODS######################

# Enforce foreign key constraints
# WARNING: DO NOT REMOVE THIS!
def enforceForeignKey():
    db.query('PRAGMA foreign_keys = ON')

# initiates a transaction on the database
def transaction():
    return db.transaction()
# Sample usage (in auctionbase.py):
#
# t = sqlitedb.transaction()
# try:
#     sqlitedb.query('[FIRST QUERY STATEMENT]')
#     sqlitedb.query('[SECOND QUERY STATEMENT]')
# except Exception as e:
#     t.rollback()
#     print str(e)
# else:
#     t.commit()
#
# check out http://webpy.org/cookbook/transactions for examples

# returns the current time from your database
def getTime():
    # TODO: update the query string to match
    # the correct column and table name in your database
    query_string = 'select time from CurrentTime'
    results = query(query_string)
    # alternatively: return results[0]['currenttime']
    return results[0].time # TODO: update this as well to match the
                                  # column name
    # returns a single item specified by the Item's ID in the database
    # Note: if the `result' list is empty (i.e. there are no items for a
    # a given ID), this will throw an Exception!

def getItemById(itemID):
    # TODO: rewrite this method to catch the Exception in case `result' is empty
    query_string = 'select * from Items where item_ID = $itemID'
    result = query(query_string, {'itemID': itemID})
    if result !=[]:
        return result
    else:
        raise Exception('Item not found')
        return None

def selectTime(time):
        query_string = 'update CurrentTime set time = $time'
        results= db.query(query_string, {'time': time})
        return results


def enterBid(itemID, userID, price):
    query_string = 'insert into Bids (item_id, user_id, amount) values ($itemID, $userID, $price)'
    bid=db.query(query_string, {'itemID': itemID, 'userID': userID,'price': price})
    if bid !=[]:
        return bid
    else:
        raise Exception('fail to enter the bid, please check the provided information.')
        return None

def bids_of_auction(itemID):
    query_string = 'select b.user_id, b.time, b.amount from Items i, Bids b where i.item_id = b.item_id and i.item_id = $itemID'
    bids = query(query_string, {'itemID': itemID})
    return bids

def status_of_auction(itemID):
    current_time = getTime()
    query_string1 = 'select * from Items where item_id = $itemID and started> $current_time '
    query_string2 = 'select * from Items where item_id = $itemID and started <= $current_time and ends >= $current_time'
    query_string3 = 'select * from Items where item_id = $itemID and (ends < $current_time or currently >= buy_Price)'
    result1 = query(query_string1, {'itemID': itemID,'current_time': current_time})
    result2 = query(query_string2, {'itemID': itemID,'current_time': current_time})
    result3 = query(query_string3, {'itemID': itemID,'current_time': current_time})
    if result1 !=[]:
        status = ' NOT STARTED'
    elif result2 !=[]:
        status = ' OPEN'
    elif result3 !=[]:
        status = ' CLOSED'
    else:
        raise Exception('Illegal status.')
    return status

def winner_of_auction(itemID):
    current_time = getTime()
    query_string= 'select b.user_id from (select * from Items where item_id = $itemID and (ends < $current_time or currently >= buy_Price)) i, Bids b where b.item_id = i.item_id and b.amount = i.currently'
    winner = query(query_string, {'itemID': itemID,'current_time': current_time})
    return winner

def categories_of_item(itemID):
    query_string = 'select c.category from Items i, Categories c where i.item_id = $itemID and c.item_id = i.item_id'
    categories = query(query_string, {'itemID': itemID})
    return categories


def browse(itemID, userID, category, description, minPrice, maxPrice, status):
    current_time = getTime()
    query_string='select * from Items i,Categories c where i.item_id = c.item_id'
    if itemID !='':
        query_string = query_string + ' and i.item_id =$itemID'
    if userID !='':
        query_string = query_string+ ' and i.seller_id= $userID'
    if category !='':
        query_string = query_string+ ' and c.category = $category'
    if description !='':
        query_string = query_string+' and  description like $description'
    if minPrice !='':
        query_string = query_string+' and  i.currently >= $minPrice'
    if maxPrice !='':
        query_string = query_string+ ' and  i.currently <= $maxPrice'
    if status == 'open':
        query_string = query_string+ ' and i.started <= $current_time and i.ends >= $current_time '
    if status == 'close':
        query_string = query_string+ ' and i.ends < $current_time'
    if status == 'notStarted':
        query_string =query_string+' and i.started > $current_time'
    if status =='all':
        query_string = query_string
    query_string= query_string+' group by i.item_id'

    results = query(query_string, {'itemID': itemID, 'userID': userID,'category': category,'description':'%'+description +'%', 'minPrice': minPrice, 'maxPrice':maxPrice, 'status':status, 'current_time': current_time })
    if results !=[]:
       return results
    else:
        raise Exception('Item not found')
        return None

def query(query_string, vars = {}):
    return list(db.query(query_string, vars))

#####################END HELPER METHODS#####################

#TODO: additional methods to interact with your database,
# e.g. to update the current time
