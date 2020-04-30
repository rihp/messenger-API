from flask import Flask, request
from pymongo import MongoClient
from datetime import datetime
import mongohandler

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
    user_id = db.user.insert_one({ 'username':f'{username}',
                                   'join_date': datetime.today(),
                                   'chats_joined': {},                                 
                                   'messages_sent':{},                                   
                                }).inserted_id
    return f"""
        <h1>User has been created </h1>       <br>
        <b>The new username: </b>{username}  <br>        
        <b>user_id:</b> {user_id}"""

@app.route("/chat/create")
def create_chat():
    title = request.args.get("title")
    users = request.args.get("users")
    if not mongohandler.get_chat_id(title):
        chat_id = db.chat.insert_one(
                                {  'title':f'{title}',
                                   'creation_date': datetime.today(),
                                   'participants': users,                                 
                                   'messages': f"Welcome! This group was created with the following users: {', '.join(users)}",                                   
                                }).inserted_id
    
        return f"A new chat room has been created! <br> Title:{title} <br> Users:{users} <br> Chat_id: {chat_id} "
    else:
        return f"Error: A public chatroom already exists with the name <b>{title}</b>.<br> Please try using a different chat_title."

@app.route("/chat/<chat_title>/addmessage")
def add_message(chat_title):
    username = request.args.get("username")
    text = request.args.get("text")
    chat_id = mongohandler.get_chat_id(chat_title)
    #return chat_id
    message_id = db.messages.insert_one({ 'chat_title':chat_title,
                                          'username':username,
                                          'time_sent':datetime.today(),
                                          'text':text}).inserted_id
    #record message_id at user document
    #record message_id at chat document
    return f"Message sent to <b>{chat_title}</b>!  <br><p><i>{text}</i><br>chat_id: {chat_id}<br> message_id: {message_id}</p>"

app.run(host="0.0.0.0", port=5007, debug=True)
