
#620108554_lab_2
from flask import Flask, request, jsonify
from datetime import datetime
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
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
    user_profile = { #dictionary containing user profile data 
        "data":{
            "role": role,
            "color":color,
            "username": username,
            "last_updated":datetime_string,
        },
        
    }
    global FAKE_DATABASE    # makes fakedatabase a global variable
    FAKE_DATABASE = user_profile  #assigns the user profile dictionary to the fake database
    
    return jsonify(FAKE_DATABASE) # for the fake database to be return we have to jsonify it 

#CREATE DATA
@app.route("/data",methods=["POST"])
def postdata():
    location = request.json["location"] #recieves tank location from server
    lat = request.json["lat"] #recieves tank latitude from server
    long = request.json["long"] #recieves tank longtitude from server
    percenatge_full = request.json["percentage_full"] # recieves tank percentage
    global id_count # makes id_count a global variable
    id_count+=1 # increments te id count by 1 
    tank_data = { #dictionary containing tank data
        "id": id_count,
        "location":location,
        "lat": lat,
        "long":long,
        "percentage_full":percenatge_full,
        }
    global FAKE_DATABASE2  #makes fake database 2 a global variable 
    FAKE_DATABASE2.append(tank_data) #gives tank data to the data base array
    return jsonify(FAKE_DATABASE2) #makes the database arrany a returnable json

#READ PROFILE
@app.route("/profile",methods = ["GET"])
def getuser(): # the read profile http get request returns the profile information from our fake database 
    return jsonify(FAKE_DATABASE)

#READ DATA
@app.route("/data",methods = ["GET"])
def getdata(): # the read data http get request returns the data information from our fake database
    return jsonify(FAKE_DATABASE2)

#UPDATE PROFILE 
@app.route("/profile",methods = ["PATCH"]) # patch request to update user profile info 
def patchuser():
    new_date_time = datetime.now()#gets day and time
    new_datetime_string = new_date_time.strftime("%d/%m/%Y, %H:%M:%S")#formats day and time
    if "username" in  request.json: # if the json request from the client which in this case is our postman web app is a username 
        FAKE_DATABASE["data"]["username"] = request.json["username"] # store the json request from the client into the location in our dictionary that correspends to where usernames are stored 
    if "color" in request.json: # if the json request from the client which in this case is our postman web app is a color
        FAKE_DATABASE["data"]["color"] = request.json["color"]# store the json request from the client into the location in our dictionary that correspends to where colors are stored 
    if  "role" in request.json: # if the json request from the client which in this case is our postman web app is a role 
        FAKE_DATABASE["data"]["role"] = request.json["role"] # store the json request from the client into the location in our dictionary that correspends to where roles are stored 
       
    if "last_updated" in (FAKE_DATABASE["data"]) != datetime_string:  # IF THE TIME STORED IN LAST UPDATED TIME IS NOT EQUAL TO THE CURRENT TIME WHEN WE PATCH THEN UPDATE THE TIME 
        FAKE_DATABASE["data"]["last_updated"] = new_datetime_string 
    return jsonify(FAKE_DATABASE)

#UPDATE TANK 
@app.route("/data/<int:id>",methods = ["PATCH"])
def patchdata(id):
    #global FAKE_DATABASE2
    for t in FAKE_DATABASE2: # SCROLLS THE THE FAKE DATABASE 
        if t ["id"] == id: # AS WE ARE SCROLLING THROUGH THE DATA BASE IF THE TANK ID  IS EQUAL TO THE TANK ID FROM THE URL INPUTTED IN OUR FUNCTION MOVE TO THE NEXT IF STATEMENT
            if "location" in request.json:# AFTER FINDING THE CORRESPONING TANK ID, IF THE INFORMATION FROM THE POSTMAN CLIENT IS A LOCATION THEN STORE THE INFORMATION FROM THE CLIENT IN THE POSITION FOR A LOCATION IN OUR DATABASE
                t["location"] = request.json["location"]
            if "lat" in request.json:
                t["lat"] = request.json["lat"]   
            if "long" in request.json:              
                t["long"] = request.json["long"] 
            if "percentage_full" in request.json:
                t["percentage_full"] = request.json["percentage_full"] #LINE 92-97 CORRESPOND WITH THE COMMENT FOR LINE 90
    for t in FAKE_DATABASE2: #SCROLL THROUGH THE UPDATE INFO IN OUR FAKE DATABASE
        if t ["id"] == id: # IF THE ID INPUTED FROM THE CLIENT IS EQUAL TO THE ID IN OUR FAKE DARABE 
            return jsonify(t) # RETURN UPDATED INFO FROM FAKE DATABSE 

#DELETE TANK 
@app.route("/data/<int:id>",methods = ["DELETE"])
def deleteuser(id):
    
        for tank_id in FAKE_DATABASE2:  #SCROLL THROUGH THE FAKE DATABASE AND IF THE ID INPUTTED FROM POSTMAN CLIENT MATCHES AN ID IN THE FAKE DATABASE THEN DELETE THAT TANK WITH THAT ID (LINE 105-108)
            if tank_id["id"] == id:
                FAKE_DATABASE2.remove(tank_id) 
        return {
            "success": True # IF THE TANK IS SUCCESFULLY DELETED RETURN " SUCCES: TRUE(BOOLEAN)"
        }

if __name__ == '__main__':
    app.run(debug=True, port=3000, host="0.0.0.0") # OUR SERVER RUNS ON PORT 3OOO AND USES LOCAL HOST 