from datetime import datetime

import requests
from bson.objectid import ObjectId
import pymongo
price = 0

MandisList=[]

def getprice(selectedmandiId,selectedcropId):
    todaysprice = 0
    yesterdayprice = 0
    url = 'http://13.234.119.95/api/mandi/getMandiProductPrice'
    myobj = {
        "mandiId": str(selectedmandiId),
    }
    x = requests.post(url, data=myobj)
    print(len(x.json()["Data"]))
    for i in (x.json()["Data"]):
        if selectedcropId == i["productId"]["_id"] :
            todaysprice = i["highestPrice"]
            yesterdayprice =i["yesterDayHigh"]
        break

    return {
        "todayprice" : todaysprice,
        "yesterdayprice" : yesterdayprice
    }

if __name__ == '__main__':
    getprice("5fddf5a07e446273391d34f3","5fdc9fed13b7130025988e8c")

