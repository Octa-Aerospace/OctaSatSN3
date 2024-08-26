import RPi.GPIO as GPIO
import csv
from time import sleep
from datetime import datetime
from modules.Buzzer import Buzzer
# from modules.Camera import Camera
from modules.GY91 import GY91
from modules.GPS import GPS
from modules.BME280 import BME280
from modules.LoRa.lora import LoRa
import os


class OctaSat:
    def __init__(self):
        self.BUZZER_PIN = 12
        self.I2C_ADDRESS = 0x68
        # self.GPS_PORT = '/dev/ttyAMA0'
        self.BUTTON_GPIO = 5
        self.data = {}
        self.setup_button()

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
        # accel = self.gy91.get_accel()
        # gyro = self.gy91.get_gyro()
        # mag = self.gy91.get_mag()
        # latitude, longitude = self.gps.read_data()
        temperature, humidity, pressure, altitude = self.bme280.get_packed_data()
        #print(f'Latitude: {latitude}\nLongitude: {longitude}\nTemperature: {temperature}\nHumidity: {humidity}\nPressure: {pressure}\nAltitude: {altitude}')
        #print('\n')

        self.data = {
            # 'accelerometer': accel,
            # 'gyroscope': gyro,
            # 'magnetometer': mag,
            'timestamp': datetime.now(),
            'latitude': latitude,
            'longitude': longitude,
            'altitude': altitude,
            'temperature': temperature,
            'humidity': humidity,
            'pressure': pressure
        }

    def save_data(self):
        headers = ['timestamp', 'latitude', 'longitude',
                   'altitude', 'temperature', 'humidity', 'pressure']
        rows = [list(self.data.values())]

        if not os.path.exists('data.csv'):
            rows.insert(0, headers)

        with open('data.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(rows)

    def send_data(self):
        # latitude, longitude = self.gps.read_data()
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
            if GPIO.wait_for_edge(device.BUTTON_GPIO, GPIO.RISING):
                while True:
                    device.read_data()
                    device.save_data()
                    device.send_data()
                    sleep(0.5)

    except KeyboardInterrupt:
        print(f'\n[!] Process interrupted')
        device.kill()
