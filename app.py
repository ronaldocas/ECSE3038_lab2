
#620108554_lab_2
from flask import Flask, request, jsonify
from datetime import datetime
app = Flask(__name__)
# datetime object containing current date and time
date_time = datetime.now()#gets day and time
datetime_string = date_time.strftime("%d/%m/%Y, %H:%M:%S")#formats day and time

FAKE_DATABASE = {} # data base for user objects 
FAKE_DATABASE2 = [] #DATA BASE FOR USER DATA 
id_count = 0
count = 0
#CRUD

#CREATE PROFILE
@app.route("/profile", methods=["POST"])
def post():
    username = request.json["username"] #recieves username from server
    role = request.json["role"] #reciever user role
    color = request.json["color"] #recieves user fav colour
    #global id_count
    #id_count=1
   # print(username)
    #print(role)
    #print(favcolour)
    user_profile = {
        "data":{
            "role": role,
            "color":color,
            "username": username,
            "last_updated":datetime_string,
        },
        
    }
    global FAKE_DATABASE    
    FAKE_DATABASE = user_profile
    
    return jsonify(FAKE_DATABASE)

#CREATE DATA
@app.route("/data",methods=["POST"])
def postdata():
    location = request.json["location"] #recieves tank location from server
    lat = request.json["lat"] #recieves tank latitude from server
    long = request.json["long"] #recieves tank longtitude from server
    percenatge_full = request.json["percentage_full"] # recieves tank percentage
    global id_count
    id_count+=1
    tank_data = {
        "id": id_count,
        "location":location,
        "lat": lat,
        "long":long,
        "percentage_full":percenatge_full,
        }
    global FAKE_DATABASE2
    #keys = list(tank_data)
    #index = keys [0]
    #print(keys)
    FAKE_DATABASE2.append(tank_data) #gives tank data to the data base array
    return jsonify(FAKE_DATABASE2) #makes the database arrany a returnable json

#READ PROFILE
@app.route("/profile",methods = ["GET"])
def getuser():
    return jsonify(FAKE_DATABASE)

#READ DATA
@app.route("/data",methods = ["GET"])
def getdata():
    return jsonify(FAKE_DATABASE2)

#UPDATE PROFILE 
@app.route("/profile",methods = ["PATCH"])
def patchuser():
    new_date_time = datetime.now()#gets day and time
    new_datetime_string = new_date_time.strftime("%d/%m/%Y, %H:%M:%S")#formats day and time
    if "username" in  request.json:
        FAKE_DATABASE["data"]["username"] = request.json["username"]
    if "color" in request.json:
        FAKE_DATABASE["data"]["color"] = request.json["color"]
    if  "role" in request.json:
        FAKE_DATABASE["data"]["role"] = request.json["role"]
        # IF THE TIME STORE IN LAST UPDATED TIME IS NOT EQUAL TO THE CURRENT TIME WHEN WE PATCH THEN UPDATE THE TIME 
    if "last_updated" in (FAKE_DATABASE["data"]) != datetime_string: 
        FAKE_DATABASE["data"]["last_updated"] = new_datetime_string
    return jsonify(FAKE_DATABASE)

#UPDATE TANK 
@app.route("/data/<int:id>",methods = ["PATCH"])
def patchdata(id):
    #global FAKE_DATABASE2
    for tank_id in FAKE_DATABASE2: 
            if tank_id["id"] == id:
                if "location" in request.json:
                    FAKE_DATABASE2[id-1]["location"] = request.json["location"]# array starts at 0 so if the id's in the data base math what we are looking for -1 to access the first one and change the location
                if "lat" in request.json:
                    FAKE_DATABASE2[id-1]["lat"] = request.json["lat"]   
                if "long" in request.json:              
                    FAKE_DATABASE2[id-1]["long"] = request.json["long"] 
                if "percentage_full" in request.json:
                    FAKE_DATABASE2[id-1]["percentage_full"] = request.json["percentage_full"]
    return jsonify(FAKE_DATABASE2)

#DELETE TANK 
@app.route("/data/<int:id>",methods = ["DELETE"])
def deleteuser(id):
    
        for tank_id in FAKE_DATABASE2: 
            if tank_id["id"] == id:
                FAKE_DATABASE2.remove(tank_id) 
        return {
            "success": True
        }

if __name__ == '__main__':
    app.run(debug=True, port=3000, host="0.0.0.0") 