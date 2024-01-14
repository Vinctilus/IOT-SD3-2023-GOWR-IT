import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN)
GPIO.setup(27, GPIO.OUT)

GPIO.output(27, GPIO.HIGH)
while True:

    ldr_value = GPIO.input(23) 

    print(f"LDR Value: {ldr_value}")
    time.sleep(1)

