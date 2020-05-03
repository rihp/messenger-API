import os
from dotenv import load_dotenv
from pymongo import MongoClient


load_dotenv()

MA = os.getenv("MA")
MAU = os.getenv("MAU")
MSERVER= os.getenv("MSERVER")

flask_api = 'http://localhost:5007'    

DBURL = os.getenv("DBURL")


DBURL = f"mongodb+srv://{MAU}:{MA}@{MSERVER}/test?retryWrites=true&w=majority"


client = MongoClient(DBURL)
db = client.messenger
print(f"Connected to MongoClient...  ")
