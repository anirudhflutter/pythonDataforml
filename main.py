from flask import jsonify,Flask
from flask import request
import json
import os
import pymongo
from opencage.geocoder import OpenCageGeocode
from geopy.distance import geodesic

app = Flask(__name__)

FinalDataSentToUser=[]

from datetime import date

MandiListForAll = []


def GetMandiForAll(mandiname,path):
    MandiListForAll.clear()
    directory = os.path.join(path)
    for root, dirs, files in os.walk(directory):
        for file in files:
            MandiListForAll.append(file)
    # GetMandiDataForAll(MandiListForAll,mandiname)
    return MandiListForAll

def GetData (enteredmandi,crop,mandipath):
    Data = GetMandiForAll(crop,mandipath)
    for i in range(0,len(Data)):
        if Data[i] == enteredmandi:
            f = open("finaljsonfiles/{}/{}".format(crop,enteredmandi))
            data = json.load(f)
            print(data["MandiId"])
            print(data["CropId"])
            # print(currentdate)
            # todaysprice = GetPrice.getprice(str(data["MandiId"]), str(data["CropId"]), currentdate)
            # yesterdayprice = GetPrice.getprice(str(data["MandiId"]), str(data["CropId"]), yesterdaydate)
            FinalDataSentToUser.append(data)
            # FinalDataSentToUser.append({
            #     "Todaysprice" : todaysprice,
            #     "Yesterdaysprice":yesterdayprice
            # })
            break

cropname1 = 'data/BAJRA/'
cropname2 = 'data/CORRIANDER LEAVES'
cropname3 = 'data/cotton'
cropname4 = 'data/Ginger/'
cropname5 = 'data/Green Chilli'
cropname6 = 'data/Jowar'
cropname7 = 'data/Maize/'
cropname8 = 'data/Onion'
cropname9 = 'data/Soybean'
cropname10 = 'data/Tomato/'
cropname11 = 'data/Wheat'

@app.route('/getuserselectedmandi')
def getuserselectedmandi():
    MandiName = request.args.get('MandiName')
    if MandiName == "":
        return jsonify({"Message" : "Please provide MandiName"})
    else:
        EnteredMandi = MandiName+".csv"
        FinalDataSentToUser.clear()
        GetData(EnteredMandi,"BAJRA",cropname1)
        GetData(EnteredMandi, "CORRIANDER LEAVES",cropname2)
        GetData(EnteredMandi, "cotton",cropname3)
        GetData(EnteredMandi, "Ginger",cropname4)
        GetData(EnteredMandi, "Green Chilli",cropname5)
        GetData(EnteredMandi, "Jowar",cropname6)
        GetData(EnteredMandi, "Maize",cropname7)
        GetData(EnteredMandi, "Onion",cropname8)
        GetData(EnteredMandi, "Soybean",cropname9)
        GetData(EnteredMandi, "Tomato",cropname10)
        GetData(EnteredMandi, "Wheat",cropname11)

        return jsonify({
                "data" : FinalDataSentToUser
    })

GetAllMandis = []


key = "4af24b047562473cba60c07d6f9ff9ff"


def getLat(place,state):
    geocoder = OpenCageGeocode(key)

    query = place + ", " + state

    results = geocoder.geocode(query)

    lat = results[0]['geometry']['lat']

    return lat


def getLong(place, state):
    geocoder = OpenCageGeocode(key)

    query = place + ", " + state

    results = geocoder.geocode(query)

    lng = results[0]['geometry']['lng']

    return lng

def getAllMandis():
    client = pymongo.MongoClient("mongodb+srv://root:root@cluster0.s73xs.mongodb.net/test")

    # Database Name
    db = client["Bhav"]

    # Collection Name
    col = db["mandis"]

    x = col.find()

    for data in x:
        mandiname = str(data["MandiName"]).replace(".csv", "")
        mandiid = str(data["_id"])
        if mandiname not in GetAllMandis:
            GetAllMandis.append({
                "mandiname":mandiname,
                "id":mandiid,
            })
    return mandiname


@app.route('/getAllMandis')
def AllMandis():
    getAllMandis()
    return jsonify({"Data": GetAllMandis})


def CalculateDistance(CurrentLat,CurrentLong,mandilat,mandilng):
    return geodesic((float(CurrentLat),float(CurrentLong)),(float(mandilat),float(mandilng))).km


@app.route('/getLatLongOfMandiAndDistance')
def getLatLongOfMandiAndDistance():
    MandiName = request.args.get('MandiName')
    CurrentLat = request.args.get('Currentlat')
    CurrentLong = request.args.get('CurrentLong')
    mandilat = getLat(MandiName,"Maharashtra")
    mandilng = getLong(MandiName,"Maharashtra")
    return jsonify({
        "Lat":mandilat,
                "Lng":mandilng,
        "Distance" : str(CalculateDistance(CurrentLat,CurrentLong,mandilat,mandilng)) + "km"
    })


port = int(os.environ.get("PORT", 5000))


if __name__ == '__main__':
    # today = date.today()
    # date = str(today).split("-")
    # currentdate = date[2] + "/" + date[1] + "/" + date[0]
    # yesterdaydate = str(int(date[2]) - 1) + "/" + date[1] + "/" + date[0]
    app.run(debug=True, host="0.0.0.0",port=port)
