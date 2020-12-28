from flask import jsonify, Flask
from flask import request
import json
import requests
import os
import pymongo
from opencage.geocoder import OpenCageGeocode
from geopy.distance import geodesic
from translate import Translator
from googletrans import Translator

import mandinameandidinmarathi

translator = Translator()
import GetPrice

app = Flask(__name__)

FinalDataSentToUser = []

from datetime import date

MandiListForAll = []


def GetMandiForAll(mandiname, path):
    MandiListForAll.clear()
    directory = os.path.join(path)
    for root, dirs, files in os.walk(directory):
        for file in files:
            MandiListForAll.append(file)
    # GetMandiDataForAll(MandiListForAll,mandiname)
    return MandiListForAll


def GetData(enteredmandi, crop, mandipath):
    Data = GetMandiForAll(crop, mandipath)
    for i in range(0, len(Data)):
        if Data[i] == enteredmandi:
            f = open("finaljsonfiles/{}/{}".format(crop, enteredmandi))
            data = json.load(f)
            FinalDataSentToUser.append(data)



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
dict = {}
newList = []
mandiforcroplist = []


@app.route('/getuserselectedmandi')
def getuserselectedmandi():
    MandiName = request.args.get('MandiName')
    if MandiName == "":
        return jsonify({"Message": "Please provide MandiName"})
    else:
        enteredmandi = MandiName + ".csv"
        FinalDataSentToUser.clear()
        GetData(enteredmandi,"BAJRA",cropname1)
        GetData(enteredmandi, "CORRIANDER LEAVES", cropname2)
        GetData(enteredmandi, "cotton", cropname3)
        GetData(enteredmandi, "Ginger", cropname4)
        GetData(enteredmandi, "Green Chilli", cropname5)
        GetData(enteredmandi, "Jowar", cropname6)
        GetData(enteredmandi, "Maize", cropname7)
        GetData(enteredmandi, "Onion", cropname8)
        GetData(enteredmandi, "Soybean", cropname9)
        GetData(enteredmandi, "Tomato", cropname10)
        GetData(enteredmandi, "Wheat", cropname11)

        return jsonify({
            "data" : FinalDataSentToUser
        })


GetAllMandis = []

key = "4af24b047562473cba60c07d6f9ff9ff"


def getLat(place, state):
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

    GetAllMandis.clear()
    for data in x:
        mandiname = str(data["MandiName"]).replace(".csv", "")
        mandiid = str(data["_id"])
        if mandiname not in GetAllMandis:
            GetAllMandis.append({
                "mandiname": mandiname,
                "id": mandiid,
            })
    return mandiname

mandiname=[]

@app.route('/mandinames')
def mandinames():
    url = 'http://13.234.119.95/api/mandi/getAllMandi'
    x = requests.post(url)
    for i in range(0,len(x.json()["Data"])):
        mandiname.append(str(x.json()["Data"][i]["MandiName"]).replace(".csv",""))
    # if language=="Marathi":
    #   # return jsonify({
    #   #     "Data" : wholedata
    #   # })
    # else:
    return jsonify({"Data" : mandiname})


def CalculateDistance(CurrentLat, CurrentLong, mandilat, mandilng):
    return geodesic((float(CurrentLat), float(CurrentLong)), (float(mandilat), float(mandilng))).km


@app.route('/mandisForSingleCrop')
def mandisForSingleCrop():
    productId = request.args.get('productId')
    language = request.args.get('language')
    if productId == "":
        return jsonify({"Message": "Please provide productId"})
    else:
        url = 'http://13.234.119.95/api/admin/getCropPriceInAllMandi'
        myobj = {
            "productId": str(productId),
        }
        x = requests.post(url, data=myobj)
        mandiforcroplist.clear()
        if language == 'Marathi':
            print("yes marathi")
            for i in range(0, x.json()["Count"]):
                word = str(x.json()["Data"][i]["mandiId"]["MandiName"])
                print(word)
                word = translator.translate(word, src='English', dest='Marathi')
                newword = word.text
                print(newword)
                dict = x.json()["Data"][i]
                dict["mandiId"]["MandiName"] = newword
                mandiforcroplist.append(dict)
                break
            return jsonify({
                "IsSuccess": True,
                "Count": x.json()["Count"],
                "Data": mandiforcroplist,
                "Message": "Data Found"
            })
        return x.json()

mandiandcropinmarathi=[]
croplist=[]
@app.route('/getmandisandcropinmarathi')
def getmandisandcropinmarathi():
    url = 'http://13.234.119.95/api/mandi/getAllMandi'

    x = requests.post(url)
    for i in range(0,len(x.json()["Data"])):
        mandi = str(x.json()["Data"][i]["MandiName"])
        word = translator.translate(mandi, src='English', dest='Marathi')
        mandiinmarathi = word.text
        crops = x.json()["Data"][i]["productId"]
        for j in range(0,len(crops)):
            cropname = x.json()["Data"][i]["productId"][j]["productName"]
            word = translator.translate(cropname, src='English', dest='Marathi')
            newword = word.text
            print(newword)
            croplist.append({
                "_id" : x.json()["Data"][i]["productId"][j]["_id"],
                "productName" : newword
            })
        mandiandcropinmarathi.append({
            "MandiName" : mandiinmarathi,
            "products" : croplist
        })
        break
    return jsonify({
        "Data" : mandiandcropinmarathi
    })

port = int(os.environ.get("PORT", 80))

if __name__ == '__main__':
    getAllMandis()

    app.run(debug=True, host="0.0.0.0", port=port)
