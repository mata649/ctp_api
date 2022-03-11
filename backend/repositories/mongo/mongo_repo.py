import os

from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()



class MongoRepo:
    def __init__(self):
        conn = os.getenv("MONGO_CONNECTION")

        client = MongoClient(conn)

        self.db = client.ctp_canas