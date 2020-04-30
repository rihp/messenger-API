from flask import Flask, request
from pymongo import MongoClient
from datetime import datetime
import mongohandler
import ast

DBURL = 'mongodb://localhost:27017'
client = MongoClient(DBURL)
print(f"Connected to MongoClient at: {DBURL}")
db = client.messenger

app = Flask(__name__)

@app.route("/")
def landing_page():
    return 'Hello, world! Welcome to my Messenger API.'

@app.route("/user/create/<username>")
def create_user(username):
    # Optimization ♠: 
    # Confirm if that username is taken, before creating it.
    if not mongohandler.get_user_id(username): 
        user_id = db.user.insert_one(
                                {  'username':f'{username}',
                                   'join_date': datetime.today(),
                                   'chats_joined': {},                                 
                                   'messages_sent':{},                                   
                                }).inserted_id
        return f"""
        <b>User has been created </b>       <br>
        <b>The new username: </b>{username}  <br>        
        <b>user_id:</b> {user_id}"""
    else: 
        return f"<b>Sorry. That username, '{username}' is already taken.</b> <br>Please choose a different username."

@app.route("/chat/create")
def create_chat():
    title = request.args.get("title")
    users = ast.literal_eval(request.args.get("users"))
    # Check if that chat_title is available. 
    # If it's NOT created yet, crate it in the MongoDB Collection. 
    # Else, return an error message, and do nothing.
    if not mongohandler.get_chat_id(title):
        # ♠Optimization: Turn this format to something more
        #participants = [ {username : {'_id':mongohandler.get_user_id(username)}} for username in users]
        participants = [ mongohandler.get_user_id(username) for username in users]

        chat_id = db.chat.insert_one(
                                {  'title':f'{title}',
                                   'creation_date': datetime.today(),
                                   'participants': participants,  
                                   #'participants': users,  
                                   'messages': f"Welcome! This group was created with the following users: {', '.join(users)}",                                   
                                }).inserted_id
        return f"A new chat room has been created! <br> <b>Title</b>:{title} <br> <b>Users</b>:{users} <br> <b>Chat_id</b>: {chat_id} "
    else:
        return f"Error: A public chatroom already exists with the name <b>{title}</b>.<br> Please try using a different chat_title."

@app.route(("/chat/<chat_title>/adduser"))
def add_user(chat_title):
    username = request.args.get("username")
    user_id = mongohandler.get_user_id(username)
    chat_id = mongohandler.get_chat_id(chat_title)
    if chat_id != None:
        # ♠ Optimization: Try to check if the user is already a member of the group.
        db.chat.update(
            {'_id':chat_id},
            {'$addToSet': {
                    'participants': user_id
                        }
            }
        )
    else:
        raise Exception('The chat_id was not be found in the current database.')
    # mongohandler.add_user_to_chat(user_id, chat_id)
    return f'{username} has been added to {chat_title}. <br> chat_id:{chat_id} <br>user_id:{user_id}'

@app.route("/chat/<chat_title>/addmessage")
def add_message(chat_title):
    username = request.args.get("username")
    text = request.args.get("text")
    chat_id = mongohandler.get_chat_id(chat_title)
    user_in_chat = mongohandler.check_user_in_chat(username, chat_title)
    print(f"Is {username} in the chat {chat_title}? {user_in_chat}")
    if chat_id != None:
        if user_in_chat:
            
            message_id = db.messages.insert_one({ 'chat_title':chat_title,
                                          'username':username,
                                          'time_sent':datetime.today(),
                                          'text':text}
                                          ).inserted_id
        #record message_id at user document
        #record message_id at chat document
            return f"Message sent to <b>{chat_title}</b>!  <br><p><i>{text}</i><br>chat_id: {chat_id}<br> message_id: {message_id}</p>"
        else: return f"{username} is not a participant in the public chat {chat_title}."
    else: return f"The public chat '{chat_title}' does not exist. <br> You could create it using the `/chat/create?title={chat_title}` API end-point."

app.run(host="0.0.0.0", port=5007, debug=True)