import os

import pymongo
from pymongo.database import Database

try:
    MONGO_URI = os.environ['MONGO_URI']
except KeyError:
    MONGO_URI = 'localhost:27017'

client = pymongo.MongoClient(MONGO_URI)
db: Database = client.get_database('KomootAnalyzer')
