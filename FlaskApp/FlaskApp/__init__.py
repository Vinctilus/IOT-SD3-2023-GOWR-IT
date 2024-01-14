#with the help of chat gpt
import os
import pathlib
from pickle import FALSE
import threading
#from tkinter import N, NO
import requests
from flask import Flask, session, abort, redirect, request, render_template
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests
from datetime import datetime
import json 
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from pubnub.callbacks import SubscribeCallback
from . import database as DB
from .env import env
from . import pubnubprivat as PNprivat
from . import pubnubpublic as PNpublic
from flask_sqlalchemy import SQLAlchemy
import pygal
from pygal.style import Style
import random
import secrets

#Loadconfig
# script_path = os.path.abspath(__file__)
# env_file_path = os.path.join(os.path.dirname(script_path), "env.json")
# with open(env_file_path, 'r') as json_file:
#     env = json.load(json_file)


app = Flask(__name__)
app.secret_key = env["APP_SECRER_KEY"]
app.config['SQLALCHEMY_DATABASE_URI'] = env["DATABASE_URI"]
db=DB.db
db.init_app(app)
with app.app_context():
        db.create_all()



#googel login Createt with tutorial https://www.youtube.com/watch?v=FKgJEfrhU1E
GOOGLE_CLIENT_ID = env["GOOGLE_CLIENT_ID"]

flow = Flow.from_client_secrets_file(
    client_secrets_file=os.path.join(pathlib.Path(__file__).parent, "client_secret.json"),
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="http://vinctilus.de/callback"
)


pnconfigPublic = PNConfiguration()
pnconfigPublic.publish_key = env["USER_PUBNUB_PUBLISH_KEY"]
pnconfigPublic.subscribe_key = env["USER_PUBNUB_SUBSCRIBE_KEY"]
pnconfigPublic.secret_key = env["USER_SECRET_KEY"]
pnconfigPublic.uuid = "Server"
pubnubPublic = PubNub(pnconfigPublic)

pnconfigPivat = PNConfiguration()
pnconfigPivat.publish_key = env["PI_PUBNUB_PUBLISH_KEY"]
pnconfigPivat.subscribe_key = env["PI_PUBNUB_SUBSCRIBE_KEY"]
pnconfigPivat.secret_key = env["PI_SECRET_KEY"]
pnconfigPivat.uuid = "Server"
pubnubPivat = PubNub(pnconfigPivat)



def valueFilter(Value,bool):
     if bool:
          return Value
     else:
          return None


def my_publish_callback(envelope, status):
    if not status.is_error():
        #print("Nachricht erfolgreich gesendet")
        pass
    else:
        print(f"Fehler beim Senden der Nachricht: {status.error_data}")
class PrivatSubscribeCallback(SubscribeCallback):
  
     
    def message(self, pubnub, message):
        with app.app_context():
            data = message.message
            
            if data:
                    tempartur = data['tempartur']
                    humity = data['humity']
                    light = data['light']
                    soil = data['soil']
                    if tempartur not in [True,False] or humity not in [True,False] or tempartur is None or humity is None:
                        deviceid = data['deviceid']
                        connectToken = data['connectToken']
                        
                        
                        
                        measuredtime = data['measuredtime']
                        if DB.findPi(deviceid):
                            device = DB.getPi(deviceid)
                            if device.connectToken == connectToken:
                                device = DB.getPi(deviceid)
                                print("Hallo")
                                if device.tempartur or device.humity or device.light or device.soil:
                                    device = DB.getPi(deviceid)
                                    DB.storeSenseorData(deviceid,measuredtime,valueFilter(tempartur,device.tempartur),valueFilter(humity,device.humity),valueFilter(light,device.light),valueFilter(soil,device.soil))
                                
                                device = DB.getPi(deviceid)
                                send = {"tempartur":device.tempartur,"humity":device.humity,"light":device.light,"soil":device.soil}
                                pubnubPivat.publish().channel(env["PIRVAT_PN_CHANNEL"]+str(deviceid)).message(send).pn_async(my_publish_callback)
                                users = DB.findallUsertoPiby(deviceid)
                                for user in users:
                                    print(str(user))     
                                    dataset = DB.get_latest_data_for_device(deviceid)
                                    send= json.dumps(dataset)
                                    pubnubPublic.set_token(PNpublic.grant_read_write_access("Server",user))
                                    pubnubPublic.publish().channel(str(user)).message(send).pn_async(my_publish_callback)



    def presence(self, pubnub, presence):
        pass  

    def status(self, pubnub, status):
        pass  

#Flask login check 
def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401)  # Authorization required
        else:
                if DB.isUser(session["google_id"]):
                    data = DB.findUser(session["google_id"])
                    if data.logedin:
                        if data.useremail == session["email"]:
                            return function(*args, **kwargs)  # Übergebe die Argumente an die Funktion
                
            
                return redirect('/logout')


    # Setze einen benutzerdefinierten Endpunkt basierend auf dem ursprünglichen Endpunkt der Funktion
    wrapper.__name__ = f"{function.__name__}_wrapped"
    return wrapper

def admin_is_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401)  # Authorization required
        else:
            if DB.isUser(session["google_id"]):
                data = DB.findUser(session["google_id"])
                if data.logedin:
                    if data.useremail == session["email"]:
                        if session["email"] == env["ADMINEMAIL"]:
                            return function(*args, **kwargs)  # Übergebe die Argumente an die Funktion
                
            
            return redirect('/logout')

    # Setze einen benutzerdefinierten Endpunkt basierend auf dem ursprünglichen Endpunkt der Funktion
    wrapper.__name__ = f"{function.__name__}_wrapped"
    return wrapper

def isadnim(id):
        if DB.isUser(session["google_id"]):
            data = DB.findUser(session["google_id"])
            if data.logedin:
                if data.useremail == session["email"]:
                    if session["email"] == env["ADMINEMAIL"]:
                         return True
        return False

@app.route("/login")
def login():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)

@app.route("/callback")
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)  # State does not match!

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )

    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")
    session["email"] = id_info.get("email")
    if DB.isUser(session["google_id"]) is False:
            DB.setup_user(session["email"], session["name"], session["google_id"])
    else:
        DB.logInUserStatus(session["google_id"],True)
        
    return redirect("/home")

@app.route('/logout')
def logout():
    DB.logInUserStatus(session["google_id"],False)
    session.clear()
    return redirect("/")

#flask App
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
@login_is_required
def home():
     
    #personal pubnub contion to  server 
    chennal = session["google_id"]
    #end denten bank data
    token = PNpublic.grant_read_access(chennal)
    device_ids = DB.findallPibytoUser(session["google_id"])
    piData = []
    for device_id in device_ids:
        piData.append(DB.get_latest_data_for_device(int(device_id)))
        print(DB.get_latest_data_for_device(int(device_id)))

    
    return render_template('home.html',chennal=chennal, piData=piData, token=token )

@app.route('/adddevice', methods=['POST'])
@login_is_required
def adddevice():
    piId = request.form.get('adddevice')
    if DB.findPi(piId) and DB.isUser(session["google_id"]):
        if not DB.isUsertoDevice(session['google_id'],piId):
            DB.adddevice(session["google_id"],piId)
    return redirect('/home')

@app.route('/device/<id>')
@login_is_required
def device(id):
    
    if DB.findPi(id) and DB.isUsertoDevice(session['google_id'],id) or isadnim(session['google_id']):
        devicedata = DB.getPi(id)
        chennal = session["google_id"]
        token = PNpublic.grant_read_access(chennal)
        return render_template('devicepage.html', deviceid=id ,devicedata=devicedata,chennal=chennal, token=token )

@app.route('/change_device_settings', methods=['POST'])
@login_is_required
def change_device_settings():
    deviceid = request.form.get('deviceid')
    tempartur = NonetoFalse(request.form.get('tempartur'))
    humity = NonetoFalse(request.form.get('humity'))
    light = NonetoFalse(request.form.get('light'))
    soil = NonetoFalse(request.form.get('soil'))
    devicename = request.form.get('devicename')
    if DB.findPi(deviceid) and DB.isUsertoDevice(session['google_id'],deviceid) or isadnim(session['google_id']):
            DB.setPi(deviceid, devicename, tempartur, humity, light, soil)
            
    return redirect(f'/device/{int(deviceid)}')
def NonetoFalse(x):
    if x is None:
        return False
    return True

@app.route('/deconect_device', methods=['POST'])
@login_is_required
def deconect_device():
    deviceid = request.form.get('deviceid')
    devicename = request.form.get('name')
    if DB.findPi(deviceid) and DB.isUsertoDevice(session['google_id'],deviceid):
            data= DB.getPi(deviceid)
            if data.devicename == devicename:
                DB.removedevice(session['google_id'],deviceid)
                return redirect('/home')
    return redirect(f'/device/{int(deviceid)}')

@app.route('/graph/<name>/<id>')
@login_is_required
def graph(name,id):
    if DB.findPi(id) and DB.isUsertoDevice(session['google_id'],id) or isadnim(session['google_id']):
        sensordata= DB.get_data_for_device(id)[:72][::-1]
        
        if name == "tempartur":
            customestyle = Style(colors=('#347585', '#000000', '#000000','#000000'))
            graph = pygal.Line(legend_at_bottom=True, interpolate='hermite', interpolation_parameters={'type': 'cardinal', 'c': .75}, style=customestyle,height=300, width=1500,x_label_rotation=270)
            graph.title = "Tempartur"
            Time =[]
            Tempra=[]
            for data in sensordata:
               Time.append(str(data.measuredtime)[-8:-3])
               Tempra.append(data.tempartur)
            graph.range = (-20, 100)
            graph.x_labels = Time
            graph.add("°c", Tempra)

            return graph.render_response()
        
        elif name == "humity":
            customestyle = Style(colors=('#46711c', '#000000', '#000000','#000000'))
            graph = pygal.Line(legend_at_bottom=True, interpolate='hermite', interpolation_parameters={'type': 'cardinal', 'c': .75}, style=customestyle,height=300, width=1500,x_label_rotation=270)
            graph.title = "Humity"
            
            Time =[]
            Humi=[]
            for data in sensordata:
               Time.append(str(data.measuredtime)[-8:-3])
               Humi.append(data.humity)

            graph.range = (0, 100)
            graph.x_labels = Time
            graph.add("in %", Humi)
            return graph.render_response()
    
    return abort(404) 


@app.route('/plank/<name>/<id>')
@login_is_required
def plank(name,id):
    if DB.findPi(id) and DB.isUsertoDevice(session['google_id'],id)or isadnim(session['google_id']):
            sensordata= DB.get_data_for_device(id)[:72][::-1]
            titel=""
            discription=""
            Time =[]
            DAta=[]
            customestyle = Style(colors=('#000000', '#000000', '#000000','#000000'))

            if name=="light":
                titel="Light"
                discription="Enough light for photosynthesis"
                customestyle = Style(colors=('#dfbc12', '#00aa00', '#00aa00','#0000FF'))
                for data in sensordata:
                    Time.append(str(data.measuredtime)[-8:-3])
                    DAta.append(data.light)

            elif name=="soil":
                titel="Soil"
                discription="Soil is moist enough"
                customestyle = Style(colors=('#9a7932', '#00aa00', '#00aa00','#0000FF'))
                for data in sensordata:
                    Time.append(str(data.measuredtime)[-8:-3])
                    DAta.append(data.soil)
            else:
                return abort(404)      
                 
            graph = pygal.Bar(legend_at_bottom=True, style=customestyle,height=300, width=1500,x_label_rotation=270,min_scale=1,show_y_labels=False)
            graph.title = titel
            graph.x_labels = Time
            graph.range = (0, 1)
            graph.add(discription, DAta)
            return graph.render_response()
    
    return abort(404) 


#todo
# @app.route('/table/<id>', methods=['POST'])
# @login_is_required
# def table():
#     #chennal = request.form['chennal']
#     #print(chennal)
#     #daten bank :
#     lastmessages = []
    
#     #personal pubnub contion to  server 
#     chennal = "my_channel"
#     publishKey = 'pub-c-276e37f0-07ec-4f6c-a8e4-93de5538b16d'
#     subscribeKey ='sub-c-16fec276-b0ed-41c0-9227-5a5234508196'
#     #end daten bank 
#     setup_propertys = {chennal:{"publishKey": publishKey, "subscribeKey": subscribeKey,"data":lastmessages}}
#     #send
#     setup=json.dumps(setup_propertys)
#     return render_template('table.html', setup=setup,name="VinPI")

@app.route('/admin')
@admin_is_required
def admin():

    userData= DB.findallUser()
    device_ids = DB.findallPi()
    piData = []
    for device_id in device_ids:
        piData.append(DB.get_latest_data_for_device(int(device_id)))

    return render_template('admin.html',piData=piData,userData=userData)


@app.route('/user/<id>')
@admin_is_required
def user(id):
    user=DB.findUser(id)
    device_ids = DB.findallPibytoUser(id)
    piData = []
    for device_id in device_ids:
        piData.append(DB.get_latest_data_for_device(int(device_id)))


    return render_template('user.html', user=user, piData=piData)

@app.route('/mergeuserto', methods=['POST'])
@admin_is_required
def edituser():
    googelid = request.form.get('googelid1')
    useremail = request.form.get('useremail1')
    oldgoogelid = request.form.get('oldgoogelid1')
    if oldgoogelid != googelid:
        if DB.isUser(oldgoogelid):
                if DB.isUser(googelid):
                    data= DB.findUser(oldgoogelid)
                    if data.useremail == useremail:
                        
                        DB.mergePItonewUser(oldgoogelid,googelid)
                        DB.removeuser(oldgoogelid)
                        return redirect(f'/user/{int(googelid)}')            
    return redirect(f'/user/{int(oldgoogelid)}')

@app.route('/deleateuser', methods=['POST'])
@admin_is_required
def deleateuser():
    googelid = request.form.get('oldgoogelid')
    useremail = request.form.get('email')
    if DB.isUser(googelid):
            data= DB.findUser(googelid)
            if data.useremail == useremail:
                DB.removeuser(googelid)
                return redirect('/admin')
    return redirect(f'/user/{int(googelid)}')


@app.route('/creatdevice', methods=['POST'])
@admin_is_required
def creatdevice():
    random_token = secrets.token_bytes(128)
    random_id = secrets.token_bytes(9)
    deviceid = int.from_bytes(random_id, "big")
    devicename = request.form.get('Cratedevice')
    connectToken = random_token.hex()

    while DB.findPi(deviceid):
        random_id = secrets.token_bytes(9)
        deviceid = int.from_bytes(random_id, "big")
        

    DB.addPi(deviceid,devicename,connectToken)
    

    return f'<p>"deviceid":{deviceid},"connectToken":{connectToken}"</p><a href="/admin">Back</a>'


@app.route('/deleatdevice', methods=['POST'])
@admin_is_required
def deleatdevice():
    deviceid = request.form.get('Deleatedevice')
    if DB.findPi(deviceid):
        DB.removePi(deviceid)
    return redirect(f'/admin')

#
# API 
#

@app.route('/api/pubnub', methods=['POST'])
def api_pubnub():
    data = request.get_json()  
    deviceid = data.get('deviceid')
    if DB.findPi(deviceid):
          #Classe CODE
                token = PNprivat.grant_read_write_access(deviceid,deviceid)
                token_response = {'token':token,'Channel':f'Channel{deviceid}'}
                pn_start_lissener(pubnubPivat, f'Channel{deviceid}')
                
                return json.dumps(token_response)
        
    
    return abort(404) 

def pn_is_subscribed(pubnub, channel_name):
    result = pubnub.get_subscribed_channels()
    return channel_name in result

def pn_start_lissener(pubnub, channel_name):
        if not pn_is_subscribed(pubnub,channel_name):
                        pubnub.set_token(PNprivat.grant_read_write_access("Server",channel_name))
                        pubnub.add_listener(PrivatSubscribeCallback())  
                        pubnub.subscribe().channels(channel_name).execute()

             




if __name__ == '__main__':
        
    app.run(debug=True)
    
    
