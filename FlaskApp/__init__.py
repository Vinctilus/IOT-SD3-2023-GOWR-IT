import os
import pathlib

import requests
from flask import Flask, session, abort, redirect, request, render_template
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests
from datetime import datetime
import json 

#from dotenv import load_dotenv
#from flask_sqlalchemy import SQLAlchemy
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from pubnub.callbacks import SubscribeCallback
FakeSenserdataBase=[]
#db = SQLAlchemy()
app = Flask(__name__)
app.secret_key = "SuperGeheim"
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:IZ"§npl7@localhost/growit'
#db.init_app(app)

#googel login Createt with tutorial https://www.youtube.com/watch?v=FKgJEfrhU1E
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
GOOGLE_CLIENT_ID = "656176659306-0uiltah92tr67ma5j7n5mc2o0sqbttf7.apps.googleusercontent.com"
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="http://www.vinctilus.de/callback"
)


def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401) 
        else:
            return function()

    # Set a custom endpoint based on the original function's endpoint
    wrapper.__name__ = f"{function.__name__}_wrapped"
    return wrapper



@app.route('/login')
def login():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)

@app.route('/logout')
def logout():
   
    session.clear()
    return redirect("/")

@app.route("/callback")
def callback():
    flow.fetch_token(authorization_response=request.url)

    #if not session["state"] == request.args["state"]:
    #    abort(500)  # State does not match!

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )

    #für die daten bank
    #email = id_info['email']
    #sub =  id_info['sub'] #eindeutige id
    #print(f"Login von {email}({sub})")
    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")
    return redirect("/home")

#flask App
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
@login_is_required
def home():
    #denten bank data:
    lastmessage = {"name":"VinPI","tempartur":12,"humity":46,"light":False,"soil":True,"time":datetime.now().strftime("%H:%M:%S %d.%m.%Y")}
    
    #personal pubnub contion to  server 
    chennal = "my_channel"
    publishKey = 'pub-c-276e37f0-07ec-4f6c-a8e4-93de5538b16d'
    subscribeKey ='sub-c-16fec276-b0ed-41c0-9227-5a5234508196'
    #end denten bank data

    #creat Dirct
    setup_propertys = {chennal:{"publishKey": publishKey, "subscribeKey": subscribeKey,"data":lastmessage}}
    
    #send
    setup=json.dumps(setup_propertys)

    return render_template('home.html',setup=setup )


@app.route('/table', methods=['POST'])
@login_is_required
def table():
    chennal = request.form['chennal']
    print(chennal)
    #daten bank :
    lastmessages = [{'id': 'VinPI', 'tempartur': 18.0, 'humity': 63.9, 'light': False, 'soil': False, 'time': [2023, 11, 26, 9, 16, 32]},
{'id': 'VinPI', 'tempartur': 18.0, 'humity': 63.9, 'light': True, 'soil': False, 'time': [2023, 11, 26, 9, 16, 37]},
{'id': 'VinPI', 'tempartur': 18.0, 'humity': 64.0, 'light': True, 'soil': False, 'time': [2023, 11, 26, 9, 16, 42]},
{'id': 'VinPI', 'tempartur': 18.0, 'humity': 63.9, 'light': False, 'soil': True, 'time': [2023, 11, 26, 9, 16, 47]},
{'id': 'VinPI', 'tempartur': 18.0, 'humity': 63.9, 'light': False, 'soil': False, 'time': [2023, 11, 26, 9, 16, 52]},
{'id': 'VinPI', 'tempartur': 18.0, 'humity': 64.0, 'light': True, 'soil': True, 'time': [2023, 11, 26, 9, 16, 57]},
{'id': 'VinPI', 'tempartur': 18.0, 'humity': 64.0, 'light': True, 'soil': False, 'time': [2023, 11, 26, 9, 17, 3]},
{'id': 'VinPI', 'tempartur': 18.0, 'humity': 63.9, 'light': False, 'soil': False, 'time': [2023, 11, 26, 9, 17, 8]},
{'id': 'VinPI', 'tempartur': 18.0, 'humity': 63.9, 'light': False, 'soil': True, 'time': [2023, 11, 26, 9, 17, 13]},
{'id': 'VinPI', 'tempartur': 18.0, 'humity': 63.9, 'light': True, 'soil': True, 'time': [2023, 11, 26, 9, 17, 15]},
{'id': 'VinPI', 'tempartur': 18.0, 'humity': 63.9, 'light': True, 'soil': False, 'time': [2023, 11, 26, 9, 17, 20]}]
    
    #personal pubnub contion to  server 
    chennal = "my_channel"
    publishKey = 'pub-c-276e37f0-07ec-4f6c-a8e4-93de5538b16d'
    subscribeKey ='sub-c-16fec276-b0ed-41c0-9227-5a5234508196'
    #end daten bank 
    setup_propertys = {chennal:{"publishKey": publishKey, "subscribeKey": subscribeKey,"data":lastmessages}}
    #send
    setup=json.dumps(setup_propertys)
    return render_template('table.html', setup=setup,name="VinPI")





FakeSenserdataBase=[]
if __name__ == '__main__':
 

    pnconfig = PNConfiguration()
    pnconfig.subscribe_key = 'sub-c-16fec276-b0ed-41c0-9227-5a5234508196'
    pnconfig.publish_key = 'pub-c-276e37f0-07ec-4f6c-a8e4-93de5538b16d'
    pnconfig.user_id = "Sender"
    pubnubPublic = PubNub(pnconfig)

    pnconfig2 = PNConfiguration()
    pnconfig2.subscribe_key = 'sub-c-e250ef25-e0e5-4906-9c1d-535f98fa496e'
    pnconfig2.publish_key = 'pub-c-2baba0e7-4c29-40ca-966f-2132fb6d60bb'
    pnconfig2.user_id = "Sender"
    pubnubPivat = PubNub(pnconfig2)


    # class SensorData(db.Model):
    #     id = db.Column(db.Integer, primary_key=True)
    #     vin_id = db.Column(db.String(20))
    #     temperature = db.Column(db.Float)
    #     humidity = db.Column(db.Float)
    #     light = db.Column(db.Boolean)  
    #     soil = db.Column(db.Boolean)   
    #     time = db.Column(db.DateTime)


    def my_publish_callback(envelope, status):
        if not status.is_error():
            #print("Nachricht erfolgreich gesendet")
            pass
        else:
            print(f"Fehler beim Senden der Nachricht: {status.error_data}")
    
    
    class MySubscribeCallback(SubscribeCallback):
        def message(self, pubnub, message):
             
            #print(f"Nachricht empfangen auf Kanal {message.channel}: {message.message}")
            data = message.message
            if data not in FakeSenserdataBase:
            #Database cant conekt in the moment
            # try:
            #     
            #     new_data = SensorData(
            #         vin_id=data['id'],
            #         temperature=data['tempartur'],
            #         humidity=data['humity'],
            #         light=data['light'],
            #         soil=data['soil'],
            #         time=data['time']
            #     )
            #     db.session.add(new_data)
            #     db.session.commit()
            #     print('Daten eingefügt')
            # except Exception as e:
            #     print(f"Fehler: {e}")
            #     db.session.rollback()
                data["name"]="VinPI"
                FakeSenserdataBase.append(data)
                if len(FakeSenserdataBase) > 100:
                    FakeSenserdataBase.pop(0)
            #print(FakeSenserdataBase)
                pubnubPublic.publish().channel('my_channel').message(data).pn_async(my_publish_callback)

            

        def presence(self, pubnub, presence):
            pass  

        def status(self, pubnub, status):
            pass  

    pubnubPivat.add_listener(MySubscribeCallback())  
    pubnubPivat.subscribe().channels('abc').execute()
    
        
    

    
    app.run(debug=True)
