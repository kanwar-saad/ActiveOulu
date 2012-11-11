import csv, sys
from pymongo import Connection
from datetime import *
from decimal import *



#Create a MongoDB Connection and get collection
connection = Connection()
db = connection['active_oulu']
devices = db['web_app_btdevice']
# Clear previous device data before adding new one
devices.drop()
# Read CSV file for device data
cr = csv.reader(open("devices.csv","rb"))
for dev in cr:
    dev_id = dev[1]
    loc_lat = dev[4]
    loc_long = dev[3]
    name = ''
    if (dev[5]!='NULL'): 
        name = dev[5]
    
    if ((dev[2] != '1') or (loc_lat == 'NULL') or (loc_long == 'NULL')):
        if (dev_id == ''):
            print "Device is bluetooth but devID is NULL"
        else:
            continue
    else:
        dev_id = int(dev_id)
        
        device = {"devID" : dev_id, "scanTime" : datetime.utcnow() , "devName" : name, "devLocLat" : loc_lat, "devLocLong" : loc_long}
        devices.insert(device)


#Print "Done"
