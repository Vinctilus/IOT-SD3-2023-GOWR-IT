import Adafruit_DHT

# Setze den GPIO-Pin, an dem der Sensor angeschlossen ist
sensor_pin = 4  # Hier den tatsächlichen Pin anpassen

# Wähle den Sensor-Typ aus (DHT22)
sensor = Adafruit_DHT.DHT22

# Versuche, Daten vom Sensor abzurufen
humidity, temperature = Adafruit_DHT.read_retry(sensor, sensor_pin)

# Überprüfe, ob die Daten erfolgreich abgerufen wurden
if humidity is not None and temperature is not None:
    # Drucke die Temperatur und Luftfeuchtigkeit
    print(f'Temperatur: {temperature:.2f}°C')
    print(f'Luftfeuchtigkeit: {humidity:.2f}%')
else:
    print('Fehler beim Lesen des Sensors. Bitte erneut versuchen.')
