from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from app.core.config import MONGO_URI, DATABASE_NAME

client = None

def get_mongo_client():
    global client

    if client is None:
        try:
            client = MongoClient(MONGO_URI)

            client.admin.command('ping')  
        except ConnectionFailure as e:
            raise Exception("Falha na conexão com MongoDB")
        
    return client

def get_database():
    client = get_mongo_client()
    return client[DATABASE_NAME]