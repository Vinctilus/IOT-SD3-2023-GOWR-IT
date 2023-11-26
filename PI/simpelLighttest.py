import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN)

while True:
    ldr_value = GPIO.input(23)  # Lese den Zustand des GPIO-Pins
    print(f"LDR Value: {ldr_value}")
    time.sleep(1)
