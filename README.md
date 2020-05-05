# Messenger-AI
### Messenger API with sentiment analysis and recommender system.

Live demo: [Heroku](http://rihp.herokuapp.com/)

This project consisted on developing a messaging API that allows the interpretation of the sentiments within a public chat (Such as `Slack`), the idea is to meassure the level of happines of an specific group chat, using the `NLTK` network.

Applications for this software, could include business chat monitoring to measure happiness of employees, generating and automatically sending a report email to the Dept. of Human Resourses, for them to analyze when the happiness levels drops below a certain threshold (KPI).

We will also use a recommender system to predict which users who write about the same topics.

**Data used is dummy data. Lorem Ipsum.**

These are public chats and **Data Privacy must be considered when sending messages**.

# API Endpoints


## `/`

  API landing page. It uses some html strings defined at the `pages.py` file

## `/users`

  A list of all the users registered in the API. There cannot be two users with the same username.

## `/user/create/{username}`

  Create a new user with the {username}

## `/user/{username}/recommend`

  Generate friend suggestions from the messages that {username} has sent to the chats


## `/chats`

  A list of all the {chat_titles}


## `/chat/create?title={ct}&usernames={arr}`

  Where {ct} is the Chat Title, and {arr} is an array of format `['username_one', 'username_two', ... , 'username_nth']` Generate friend suggestions from the messages that {username} has sent to the chats

## `/chat/{chat_title}/adduser`

  description

## `/chat/{chat_title}/addmessage`

  description

## `/chat/{chat_title}/sentiment`

  description


## `/messages`

  cd inA list of all the messages.

## `/user/update/similaritymatrix`

   description

