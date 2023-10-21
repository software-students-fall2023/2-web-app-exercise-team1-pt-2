from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv

load_dotenv()
uri=os.getenv('URI')

client = MongoClient(uri, server_api=ServerApi('1'))

try:
    client.admin.command('ping')
    print("successfully connected to mongo")
except Exception as e:
    print(e)