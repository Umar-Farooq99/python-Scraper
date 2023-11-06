import pymongo
from pymongo.errors import ConnectionFailure
from pymongo import MongoClient
def connect_to_mongodb():
    try:
        client = MongoClient("mongodb://localhost:27017",serverSelectionTimeoutMS=1000)  # long the driver will try to connect to a server. The default value is 30
        db = client['scraping']
        collection_2 = db['Companies_Raw']
        collection_1 = db['Companies']
        collection_3 = db['leads']
        client.server_info()     #tell us about mongodb server if error occur in connection
        print("Connected to the MongoDB database successfully!")
        return collection_1,collection_2,collection_3  # Return the collection object for use in the Flask app
    except ConnectionFailure as e:
        print(f"ERROR: MongoDB connection failed - {e}")
        return None
