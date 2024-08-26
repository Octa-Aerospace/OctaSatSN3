import mysql.connector
from mysql.connector import Error

class DatabaseManager:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if self.connection.is_connected():
                self.cursor = self.connection.cursor()
                print("Successfully connected to the database")
        except Error as e:
            print(f"Error while connecting to MySQL: {e}")

    def insert_telemetry_data(self, telemetry_data):
        try:
            if self.connection.is_connected():
                insert_query = """
                INSERT INTO telemetry_data (
                    timestamp, latitude, longitude, altitude, temperature, humidity, pressure,
                    accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z, mag_x, mag_y, mag_z
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                self.cursor.execute(insert_query, (
                    telemetry_data['timestamp'],
                    telemetry_data['latitude'],
                    telemetry_data['longitude'],
                    telemetry_data['altitude'],
                    telemetry_data['temperature'],
                    telemetry_data['humidity'],
                    telemetry_data['pressure'],
                    telemetry_data['accel_x'],
                    telemetry_data['accel_y'],
                    telemetry_data['accel_z'],
                    telemetry_data['gyro_x'],
                    telemetry_data['gyro_y'],
                    telemetry_data['gyro_z'],
                    telemetry_data['mag_x'],
                    telemetry_data['mag_y'],
                    telemetry_data['mag_z']
                ))
                self.connection.commit()
                print("Telemetry data inserted successfully")
        except Error as e:
            print(f"Failed to insert data into MySQL table: {e}")

    def close(self):
        if self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            print("MySQL connection is closed")
