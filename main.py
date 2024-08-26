import os
import csv
from time import sleep
from datetime import datetime
import RPi.GPIO as GPIO
#
from db.index import DatabaseManager
from modules.Buzzer import Buzzer
# from modules.Camera import Camera
from modules.GY91 import GY91
from modules.GPS import GPS
from modules.BME280 import BME280
from modules.LoRa.lora import LoRa


class OctaSat:
    def __init__(self):
        self.BUZZER_PIN = 12
        self.I2C_ADDRESS = 0x68
        # self.GPS_PORT = '/dev/ttyAMA0'
        self.BUTTON_GPIO = 5
        self.data = {}
        self.setup_button()
        self.db = DatabaseManager(
            host="",
            user="",
            password="",
            database=""
        )
        self.db.connect()


    def setup_button(self):
        GPIO.setup(self.BUTTON_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def init(self):
        # self.gy91 = GY91(self.I2C_ADDRESS)
        # self.gps = GPS(port=self.GPS_PORT)
        self.bme280 = BME280()
        self.lora = LoRa()
        # self.camera = Camera()
        # self.e32 = E32()

        self.buzzer = Buzzer(self.BUZZER_PIN)
        self.buzzer.init()

    def read_data(self):
        temperature, humidity, pressure, altitude = self.bme280.get_packed_data()
        self.data = {
            'timestamp': datetime.now(),
            'latitude': -1,
            'longitude': -1,
            'altitude': altitude,
            'temperature': temperature,
            'humidity': humidity,
            'pressure': pressure,
            'accel_x': 0,
            'accel_y': 0,
            'accel_z': 0,
            'gyro_x': 0,
            'gyro_y': 0,
            'gyro_z': 0,
            'mag_x': 0,
            'mag_y': 0,
            'mag_z': 0
        }

    def save_data(self):
        self.db.insert_telemetry_data(self.data)

    def send_data(self):
        latitude, longitude = -1, -1
        temperature, humidity, pressure, altitude = self.bme280.get_packed_data()
        payload = f'Latitude: {latitude}\nLongitude: {longitude}\nTemperature: {temperature}\nHumidity: {humidity}\nPressure: {pressure}\nAltitude: {altitude}'
        self.lora.begin_packet_radio(payload)

    def kill(self):
        self.buzzer.destroy()

if __name__ == "__main__":
    device = OctaSat()
    device.init()

    try:
        while True:
            device.read_data()
            device.save_data()
            device.send_data()
            sleep(0.5)

    except KeyboardInterrupt:
        print(f'\n[!] Process interrupted')
        device.kill()
