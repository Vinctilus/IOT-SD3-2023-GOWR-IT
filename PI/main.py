""" 
    GrwoIT PI 

    This is the main document the funktions and objektes will bei in an Folder them selsfe 
    Hear your find all importen data to set up the Pi.

    Wenn creat the contaion with an Pubnub server with for the comuniaction between PI and Server 

""" 
import os
import json
import time
from datetime import datetime
from parts.DHT22 import DHT22
from parts.GPIOIN import GPIOIN
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub








def load_configuration():
    current_directory = os.path.dirname(__file__)
    file_path = os.path.join(current_directory, "config.json")

    try:
        with open(file_path, 'r') as file:
            configuration = json.load(file)
        return configuration
    except FileNotFoundError:
        raise SystemExit("Error: The file config.json was not found.")
    except json.JSONDecodeError:
        raise SystemExit("Error: The file config.json does not contain valid JSON.")

#pubnub code 
def publishing_error(result, status):
    if status.is_error():
        print("Pubnub does not receive Message")

if __name__ == "__main__":
    global config 
    config = load_configuration()

    #Pubnub
    pnconfig = PNConfiguration()
    pnconfig.subscribe_key = 'sub-c-e250ef25-e0e5-4906-9c1d-535f98fa496e'
    pnconfig.publish_key = 'pub-c-2baba0e7-4c29-40ca-966f-2132fb6d60bb'
    pnconfig.user_id = "Sender"
    pubnub = PubNub(pnconfig)
    
    #sensor setup
    TH_Senseor = DHT22(config["Tempartur_and_Humity_Sensor"]["GPIO_pin"]) #T-empatur H-umity Senseor DHT22 Standert= 4
    L_Sensor = GPIOIN(23)
    S_Sensor = GPIOIN(17,True)
    while True:
        
        TH_Senseordata = TH_Senseor.get_data()
        L_Senseordata = L_Sensor.get_data()
        S_Senseordata = S_Sensor.get_data()

        #a={"id":"VinPI","tempartur":round(TH_Senseordata["temperature"],2),"humity":round(TH_Senseordata["humidity"],2),"light":L_Senseordata,"soil":S_Senseordata,"time":datetime.now()}
        #print(a)
        gettime = datetime.now()
        #year, month, day[, hour[, minute[, second
        timearry=[gettime.year,gettime.month,gettime.day,gettime.hour,gettime.minute,gettime.second]
        a={"id":"VinPI","tempartur":round(TH_Senseordata["temperature"],2),"humity":round(TH_Senseordata["humidity"],2),"light":L_Senseordata,"soil":S_Senseordata,"time":timearry}
        print(a)
        pubnub.publish().channel('abc').message(a).pn_async(publishing_error)
        time.sleep(2)




    
