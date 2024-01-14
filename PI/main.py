from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from pubnub.callbacks import SubscribeCallback
import requests
from datetime import datetime, timezone
import time
import json
import os
from env import env
from parts.DHT22 import DHT22
from parts.GPIOIN import GPIOIN





class PNCallback(SubscribeCallback):
    def message(self, pubnub, message):
        data=message.message
        global gotmessage
        gotmessage = True
        try:
            if data:
                tempartur = data['tempartur']
                humity = data['humity']
                light = data['light']
                soil = data['soil']
               
                json_file_path = os.path.join(os.path.dirname(__file__), 'config.json')
                with open(json_file_path, 'r') as json_file:
                     config = json.load(json_file)
                if config != data:
                     with open(json_file_path, 'w') as json_file:
                         json.dump(data, json_file, indent=2)
        except:
            pass


    def presence(self, pubnub, presence):
        pass  

    def status(self, pubnub, status):
        pass  

def server_communication():
    print("reloade connection")
    url = 'https://vinctilus.de/api/pubnub'
    data = {'deviceid': env["DEVICEID"]} 
    try:
        response = requests.post(url, json=data)
        pubnub.set_token(response.json().get("token", ""))
        pubnub.add_listener(PNCallback())  
        pubnub.subscribe().channels(env["CHENNEL"]+env["DEVICEID"]).execute()
    except:
        pass




def publish_callback(result, status):
    if status.is_error():
        pass
    else:
        print("Send")
        

def checkifsend(value,bool):
    if bool:
        return value
    else:
        return None

gotmessage = False
if __name__ == "__main__":
    print("Start Aplication")
    # PubNub-Konfiguration erstellen
    pn_config = PNConfiguration()
    pn_config.publish_key = env["PUB"]
    pn_config.subscribe_key = env["SUB"]
    pn_config.uuid = env["DEVICEID"]  # Setze dies auf eine eindeutige ID für deinen Client
    pubnub = PubNub(pn_config)

    #sensor setup
    TH_Senseor = DHT22(env["Tempartur_and_Humity_Sensor"]) #T-empatur H-umity Senseor DHT22 Standert= 4
    L_Sensor = GPIOIN(env["Light_Sensor"])
    S_Sensor = GPIOIN(env["Soil_Sensor"],True)


    while True:
        #chek if got message back
        if not gotmessage:
            #if not get reativat comunication tunnel
            server_communication()

        #get sensero data
        TH_Senseordata = TH_Senseor.get_data()
        L_Senseordata = L_Sensor.get_data()
        S_Senseordata = S_Sensor.get_data()
        #get config
        json_file_path = os.path.join(os.path.dirname(__file__), 'config.json')
        with open(json_file_path, 'r') as json_file:
                     config = json.load(json_file)

        data = {
        "deviceid": env["DEVICEID"],
        "connectToken": env["CONNECTTOKEN"],
        "measuredtime": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
        "tempartur": round(TH_Senseordata["temperature"],2),
        "humity": round(TH_Senseordata["humidity"],2),
        "light": L_Senseordata,
        "soil": S_Senseordata
        }

        
        text = json.dumps(data)
        try:
            pubnub.publish().channel(env["CHENNEL"]+env["DEVICEID"]).message(data).pn_async(publish_callback)
        except:
            pass
        gotmessage = False
        time.sleep(5)

