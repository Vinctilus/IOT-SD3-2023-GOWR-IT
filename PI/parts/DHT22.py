"""
    This subs system include the the part to make the contation tu the DHT22/AM2302

"""
import Adafruit_DHT


class DHT22:
    _instance = None
    
    def __new__(cls, GPIO_pin):
        if cls._instance is None:
            cls._instance = super(DHT22, cls).__new__(cls)
            cls._instance.sensor_pin = GPIO_pin
        return cls._instance

    def get_data(self):
        humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, self.sensor_pin)
        return {"humidity": humidity, "temperature": temperature}
    
             
"""
    Test Subsystem
    singel run

"""

if __name__ =="__main__":
    import time

    config = {"Tempartur_and_Humity_Sensor":{"GPIO_pin":4}}
    
    TH_Senseor = DHT22(4) #T-empatur H-umity Senseor 
    
    while True:
        data = TH_Senseor.get_data()
        print(data)
        time.sleep(1)
