from ..config import github_profile, repo_url

NAVBAR=f"""<br> <a href="/">HOME</a> | <a href="{repo_url}">Checkout the Github Repo</a><br>"""

HEADER ="""\
<h1>Messenger API</h1>
<h3>Recommender System and Sentiment Analysis</h3>
"""+NAVBAR

FOOTER=f"<h3><br><br>&emsp;A weekend project by <b><a href='{github_profile}''>RIHP<a></b><h3>"

home_html=HEADER+"""\
<p>To use the API, use your browser to access one of the following <b>endpoints</b>:</p>

<p>
    <h4>`/`</h4>
        <p>&emsp;&emsp;API landing page.</p>

    <h4>`/users`</h4>
        <p>&emsp;&emsp;A list of all the users in the API</p>
        
    <h4>`/user/create/{username}`</h4>
        <p>&emsp;&emsp;Create a new user with the {username}</p>

    <h4>`/user/{username}/recommend`</h4>
        <p>&emsp;&emsp;Generate friend suggestions from the messages that {username} has sent to the chats</p>

    <h4>`/chats`</h4>
        <p>&emsp;&emsp;A list of all the {chat_titles}</p>

    <h4>`/chat/create?title={ct}&usernames={arr}`</h4>
        <p>&emsp;&emsp;Where {ct} is the Chat Title, and {arr} is an array of format `['username_one', 'username_two', ... , 'username_nth']`
        Generate friend suggestions from the messages that {username} has sent to the chats</p>
 
    <h4>`/chat/{chat_title}/adduser`</h4>
        <p>&emsp;&emsp;A list of all the messages.</p>

    <h4>`/chat/{chat_title}/addmessage`</h4>
        <p>&emsp;&emsp;A list of all the messages.</p>

    <h4>`/chat/{chat_title}/sentiment`</h4>
        <p>&emsp;&emsp;A list of all the messages.</p>

    <h4>`/messages`</h4>
        <p>&emsp;&emsp;A list of all the messages.</p>

    <h4>`/user/update/similaritymatrix`</h4>
        <p>&emsp;&emsp;A list of all the users in the API</p>
</p>
"""+FOOTER

