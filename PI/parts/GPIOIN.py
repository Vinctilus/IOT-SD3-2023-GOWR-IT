import RPi.GPIO as GPIO
class GPIOIN:

    def __init__(self,GPIO_Pin,invert=False):
        self.invert =invert
        self.sensor_pin =GPIO_Pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.sensor_pin, GPIO.IN)

    def get_data(self):
        temp = GPIO.input(self.sensor_pin)==1
        
        if self.invert:
            temp = not temp 
        
        return temp
    
             
"""
    Test Subsystem
    singel run

"""

if __name__ =="__main__":
    import time

    config = {"Tempartur_and_Humity_Sensor":{"GPIO_pin":4}}
    
    Light = GPIOIN(23) #ligth sensor
    Soil = GPIOIN(17,True)   #soil 
    
    while True:
        data = Soil.get_data()
        print(data)
        time.sleep(1)