CREATE DATABASE IF NOT EXISTS OctaSatDB;

USE OctaSatDB;

CREATE TABLE telemetry_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp DATETIME NOT NULL,
    latitude DECIMAL(10, 7),
    longitude DECIMAL(10, 7),
    altitude FLOAT,
    temperature FLOAT,
    humidity FLOAT,
    pressure FLOAT,
    accel_x FLOAT DEFAULT 0,
    accel_y FLOAT DEFAULT 0,
    accel_z FLOAT DEFAULT 0,
    gyro_x FLOAT DEFAULT 0,
    gyro_y FLOAT DEFAULT 0,
    gyro_z FLOAT DEFAULT 0,
    mag_x FLOAT DEFAULT 0,
    mag_y FLOAT DEFAULT 0,
    mag_z FLOAT DEFAULT 0
);
