from flask import Flask, request
from pymongo import MongoClient
from datetime import datetime

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
    chat_id = db.chat.insert_one({ 'title':f'{title}',
                                   'creation_date': datetime.today(),
                                   'participants': users,                                 
                                   'messages': f"Welcome! This group was created with the following users: {', '.join(users)}",                                   
                                }).inserted_id
    return f"title:{title} <br> users:{users} <br> chat_id: {chat_id} "

@app.route("/chat/<chat_id>/addmessage")
def add_message(chat_id):
    username = request.args.get("username")
    text = request.args.get("text")
    #message_id = db.messages.insert_one({ 'title':f'{title}'})
    #record message_id at user document
    #record message_id at chat document
    return f"Message sent to <b>{chat_id}</b>! <br><p><i>{text}</i></p>"

app.run(host="0.0.0.0", port=5007, debug=True)
