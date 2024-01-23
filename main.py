import RPi.GPIO as GPIO
import csv
from time import sleep
from datetime import datetime
from modules.Buzzer import Buzzer
#from modules.Camera import Camera
from modules.GY91 import GY91
from modules.GPS import GPS
from modules.BME280 import BME280
import os
from modules.LoRa.lora import LoRa

class OctaSat:
  def __init__(self):
        self.BUZZER_PIN = 12
        self.I2C_ADDRESS = 0x68
        self.GPS_PORT = '/dev/ttyAMA0'
        self.BUTTON_GPIO = 5  
        self.data = {}
        self.setup_button()

  def setup_button(self):
        GPIO.setup(self.BUTTON_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)  


  def init(self):
    self.gy91 = GY91(self.I2C_ADDRESS)
    self.gps = GPS(port=self.GPS_PORT)
    self.bme280 = BME280()
    self.lora = LoRa()
    # self.camera = Camera()
    # self.e32 = E32()

    self.buzzer = Buzzer(self.BUZZER_PIN)
    self.buzzer.init()

  def safe_float(self, value):
    if value is None or value.lower() == 'none':
      return None
    else:
        return float(value)

  def save_data(self):
    data = self.lora.receive_packet_radio()
    headers = ['timestamp', 'latitude', 'longitude', 'altitude', 'temperature', 'humidity', 'pressure']
        
    # Obtener los valores específicos de la estructura data
    lines = data.split('\n')  # Divide la cadena en líneas
    latitude = self.safe_float(lines[0].split(': ')[1]) if 'Latitude' in data else None
    longitude = self.safe_float(lines[1].split(': ')[1]) if 'Longitude' in data else None
    altitude = self.safe_float(lines[5].split(': ')[1]) if 'Altitude' in data else None
    temperature = self.safe_float(lines[2].split(': ')[1]) if 'Temperature' in data else None
    humidity = self.safe_float(lines[3].split(': ')[1]) if 'Humidity' in data else None
    pressure = self.safe_float(lines[4].split(': ')[1]) if 'Pressure' in data else None

    values = [datetime.now(), latitude, longitude, altitude, temperature, humidity, pressure]
    rows = [values]

    if not os.path.exists('data.csv'):
      rows.insert(0, headers)

    with open('data.csv', 'a', newline='') as file:
      writer = csv.writer(file)
      writer.writerows(rows)


  def receive_data(self):
    data = self.lora.receive_packet_radio()
    print(f'[!] Packet received >> {data}') #uncomment to see what's the data 
   

  def kill(self):
    self.buzzer.destroy()

if __name__ == "__main__":
    device = OctaSat()
    device.init()


    try:
        while True:
            if GPIO.wait_for_edge(device.BUTTON_GPIO, GPIO.RISING):
               while True:
                device.receive_data()
                device.save_data()
                sleep(0.5)

    except KeyboardInterrupt:
        print(f'\n[!] Process interrupted')
        device.kill()

#Uncomment if you don't want to run the program with the button
"""""
    try:
        while True:
            device.read_data()
            device.save_data()
            sleep(0.5)
    except KeyboardInterrupt:
        print(f'\n[!] Process interrupted')
        device.kill()
"""""
