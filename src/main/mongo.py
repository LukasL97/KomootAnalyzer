import os

import pymongo
from pymongo.database import Database

MONGO_URI = os.environ['MONGO_URI'] or 'localhost:27017'

client = pymongo.MongoClient(MONGO_URI)
db: Database = client.get_database('KomootAnalyzer')
