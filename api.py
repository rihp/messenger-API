from flask import Flask, request
from pymongo import MongoClient
from datetime import datetime
from src.config import *
#from src.config import flask_api, db
from src.mongohandler import *
from src import recommender
import ast

import pandas as pd
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

nltk.download('vader_lexicon')

#DBURL = 'mongodb://localhost:27017'
#client = MongoClient(DBURL)
#print(f"Connected to MongoClient at: {DBURL}")
#db = client.messenger

app = Flask(__name__)

@app.route("/")
def landing_page():
    return 'Hello, world! Welcome to my Messenger API.'

@app.route("/user/create/<username>")
def create_user(username):
    # Optimization ♠: 
    # Confirm if that username is taken, before trying to create it.
    username = no_spaces(username).lower()
    
    if not get_user_id(username): 
        user_id = db.user.insert_one(
                                {  'username':f'{username}',
                                   'join_date': datetime.today(),
                                   'chats_joined': ['sorry, this field should be added when creating each new chat'],                                 
                                   'messages_sent':[],                                   
                                }).inserted_id
        return f"""
        <b>User has been created </b>       <br>
        <b>The new username: </b>{username}  <br>        
        <b>user_id:</b> {user_id}"""
    else: 
        return f"<b>Sorry. That username, '{username}' is already taken.</b> <br>Please choose a different username."

@app.route("/chat/create")
def create_chat():
    title =  no_spaces(request.args.get("title")).lower()
    users = ast.literal_eval(request.args.get("users"))
    # Check if that chat_title is available. 
    # If it's NOT created yet, crate it in the MongoDB Collection. 
    # Else, return an error message, and do nothing.
    for user in users: # Check if all the users exist
        user_id = get_user_id(user)
        if user_id == None: return f'Sorry. The chat was not created because the <b>user_id</b> does not exist for the username <b> {user}</b>.'
    if get_chat_id(title) == None:      
        chat_id = db.chat.insert_one(
            {  'title':f'{title}',
                'creation_date': datetime.today(),
                # ♠Optimization: Use this format to organize the 'messages' attribute of the chat documents and the user documents
                'participants': [ get_user_id(username) for username in users],  
                #'messages': f"Welcome! This group was created with the following users: {', '.join(users)}",                                   
                'messages': [],                                   
            }).inserted_id
        return f"A new chat room has been created! <br> <b>Title</b>:{title} <br> <b>Users</b>:{users} <br> <b>Chat_id</b>: {chat_id} "
    else:
        return f"Error: A public chatroom already exists with the name <b>{title}</b>.<br> Please try using a different chat_title."

@app.route(("/chat/<chat_title>/adduser"))
def add_user(chat_title):
    username = request.args.get("username")
    user_id = get_user_id(username)
    chat_id = get_chat_id(chat_title)
    if chat_id != None:
        if user_id == None: return f'Sorry. The chat was not created because the <b>user_id</b> does not exist for the username <b> {username}</b>.'
        if check_user_in_chat(username, chat_title): return f'<b>{username}</b> is already a member of the chat named <b>{chat_title}</b>.'
        # ♠ Optimization: Try to check if the user is already a member of the group.
        db.chat.update(
            {'_id':chat_id},
            {'$addToSet': {
                    'participants': user_id
                        }
            }
        )
    else:
        raise Exception('The chat_id was not found in the current database.')
    # add_user_to_chat(user_id, chat_id)
    return f'<b>{username}</b> has been added to <b>{chat_title}</b>. <br> chat_id:{chat_id} <br>user_id:{user_id}'

@app.route("/chat/<chat_title>/addmessage")
def add_message(chat_title):
    username = request.args.get("username")
    text = request.args.get("text")
    chat_id = get_chat_id(chat_title)
    user_id = get_user_id(username)
    user_in_chat = check_user_in_chat(username, chat_title)
    print(f"Is {username} in the chat {chat_title}? {user_in_chat}")
    if chat_id != None:
        if user_id != None:
            if user_in_chat:
                message_id = db.messages.insert_one(
                    {
                        'chat_id':chat_id,
                        'user_id':user_id,
                        'time_sent':datetime.today(),
                        'text':text}
                    ).inserted_id
                #record message_id at user document                                        
                db.user.update(
                    {'_id':user_id},
                    {'$addToSet': {
                        'messages_sent': message_id
                        }
                    }
                )
                db.chat.update(
                    {'_id':chat_id},
                    {'$addToSet': {
                        'messages': message_id
                        }
                    }
                )        
                #record message_id at chat document
                return f"Message sent to <b>{chat_title}</b>!  <br><p><i>{text}</i><br>chat_id: {chat_id}<br> message_id: {message_id}<br> user_id: {user_id}</p>"
            else: return f"<b>{username}</b> is not a participant in the public chat <b>{chat_title}</b>."
        else: return f"The user <b>{username} </b>does not exist. You can register a new user with the `/user/create/{username}` API end-point."
    else: return f"The public chat <b>'{chat_title}'</b> does not exist. <br> You could create it using the `/chat/create?title={chat_title}` API end-point."


@app.route("/chat/<chat_title>/sentiment")
def chat_sentiment(chat_title):
    sia = SentimentIntensityAnalyzer()
    chat_title = no_spaces(chat_title).lower()
    CHATSquery = get_CHATSquery()

    chat_messages = list(get_chat_doc(chat_title, CHATSquery))[0]['messages']

    def analyze_chat_sentiment(chat_messages):
        for i in range(len(chat_messages)):
            text = chat_messages[i]['text']
            yield sia.polarity_scores(text)
    sentiment = pd.DataFrame(list(analyze_chat_sentiment(chat_messages)))

    return sentiment.to_json()


# MAKE THE COMPUTATION WHEN LOADING THE MODULE TO AVOID UNNECESSARY RE-CALCUTALIONS

similatiry_matrix = "Not calculated yet. `/user/update/similaritymatrix`"

@app.route("/user/<username>/recommend")
def recommend_friends(username):
    if type(similarity_matrix) == str: return similarity_matrix
    print(type(similarity_matrix))
    return recommender.most_similar_users(username, similatiry_matrix, top=3)


@app.route("/user/update/similaritymatrix")
def similarity_matrix():
    print("Calculating User Similarity Matrix... \n  This might take a while. \n  Running from api.py")
    global similatiry_matrix
    similatiry_matrix = recommender.user_similarity_matrix()
    print(' SIM MATRIX CALCULATED')
    return f'SIM MATRIX CALCULATED <br> Check out the new endpoint`/user/<username>/recommend`'

app.run(host="0.0.0.0", port=PORT, debug=True)

