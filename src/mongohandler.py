import ast
from pymongo import MongoClient
from .config import *

#DBURL = 'mongodb://localhost:27017'
#client = MongoClient(DBURL)
#print(f"Connected to MongoClient at: {DBURL}")
#db = client.messenger

def no_spaces(string):
    return string.replace(' ', '_')

def get_chat_id(chat_title):
    # ♠ Optimization: Turn this repeated line into a decorator
    chat_title = no_spaces(chat_title).lower() 

    chat_doc = db.chat.find_one({'title':chat_title})
   # print(chat_doc)
    if chat_doc == None:
        #raise Exception("Error!! That `chat_title` does not exist")
        return None
    else:
        return chat_doc['_id']

def get_user_id(username):
    username = no_spaces(username)
    user_doc = db.user.find_one({'username':username.lower()})
    if user_doc == None:
        return None
    else:
        return user_doc['_id']

def check_user_in_chat(username, chat_title):
    user_id = get_user_id(username.lower())
    chat_id = get_chat_id(chat_title.lower())
    status = db.chat.find_one(
                        {'_id':chat_id, 
                         'participants': user_id
                        })
    if status: 
        return True
    else: 
        return False     
        
def add_user_to_chat(user_id, chat_id):
    # Update chat_id, in the participants field, add the specified user_id 
    pass


#### DOCUMENT PIPELINE ####

def get_CHATSquery():
    cur = db.chat.aggregate([{'$lookup': {
                                'from': 'messages',             # Use the messages collection
                                'localField': 'messages',   
                                'foreignField': '_id',     
                                'as': 'messages'}
                            }, 
                            {'$project': {
                                '_id': 1, 
                                'title': 1, 
                                'participants': 1, 
                                'messages': {
                                    'text': 1, 
                                    'username': 1}
                            }}])
    CHATSquery = list(cur)
    return CHATSquery

def get_USERSquery():
    cur = db.user.aggregate([{'$lookup': {
                                'from': 'messages',             
                                'localField': 'messages_sent', 
                                'foreignField': '_id', 
                                'as': 'all_messages'}
                            },
                            {'$project': {
                                'username': 1,
                                'all_messages': {
                                    'text': 1}}}])
    USERSquery = list(cur)
    return USERSquery

def get_chat_doc(chat_title, query):
    # This function takes in a pymongo CHATSquery cursor
    # which has already been turned into a list
    # and looks for an specific chat title.
    for i in range(len(query)):
        if query[i]['title'] == chat_title:
            yield query[i]

def iter_messages_from_user(query, username):
    for user_doc in query:                               # Exploring the query
        if user_doc['_id'] == get_user_id(username):     # Finding an specific user id   
            for message in user_doc['all_messages']:     # Looping through the messages
                yield message['text']                    # Analyze these raw strings

def get_doc_from_array(query, chat_title):
    for doc in query:
        if doc['_id'] == get_chat_id(chat_title.lower()): return doc