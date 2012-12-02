from pymongo import Connection
from datetime import *
from decimal import *


#Create a MongoDB Connection and get collection
connection = Connection()
db = connection['active_oulu']
act_collection = db['web_app_btactivity']

activity = act_collection.find({"devID":1811260036})

print activity[0]

