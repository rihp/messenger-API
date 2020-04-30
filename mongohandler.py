from pymongo import MongoClient

DBURL = 'mongodb://localhost:27017'
client = MongoClient(DBURL)
print(f"Connected to MongoClient at: {DBURL}")
db = client.messenger

def get_chat_id(chat_title):
    chat_doc = db.chat.find_one({'title':chat_title})
    if chat_doc == None:
        #raise Exception("Error!! That `chat_title` does not exist")
        return None
    else:
        return chat_doc['_id']

def get_user_id(username):
    user_doc = db.user.find_one({'username':username})
    if user_doc == None:
        return None
    else:
        return user_doc['_id']

def add_user_to_chat(user_id, chat_id):
    # Update chat_id, in the participants field, add the specified user_id 
    pass
