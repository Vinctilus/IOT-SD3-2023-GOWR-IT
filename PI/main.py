""" 
    GrwoIT PI 

    This is the main document the funktions and objektes will bei in an Folder them selsfe 
    Hear your find all importen data to set up the Pi.

    Wenn creat the contaion with an Pubnub server with for the comuniaction between PI and Server 

""" 
import os
import json
import time
from parts.DHT22 import DHT22

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

if __name__ == "__main__":
    global config 
    config = load_configuration()

    TH_Senseor = DHT22(config["Tempartur_and_Humity_Sensor"]["GPIO_pin"]) #T-empatur H-umity Senseor DHT22 Standert= 4
    while True:
        data = TH_Senseor.get_data()
        print(data)
        time.sleep(1)




    
