import os
from dotenv import load_dotenv
from pymongo import MongoClient

# ======= dotenv
load_dotenv()
MA = os.getenv("MA")
MAU = os.getenv("MAU")
MSERVER= os.getenv("MSERVER")
PORT= os.getenv("PORT")
#DBURL = os.getenv("DBURL")

# =======     API
flask_api = 'http://localhost:5007'    
github_profile="https://github.com/rihp"
repo_url="https://github.com/rihp/messenger-API"
# ======= MONGODB ATLAS
DBURL = f"mongodb+srv://{MAU}:{MA}@{MSERVER}/test?retryWrites=true&w=majority"
client = MongoClient(DBURL)
db = client.messenger
print(f"Connected to MongoClient...  ")
