"""
inertial_mod.py

This module provides functions for interfacing with the Adafruit LSM9DS1 IMU sensor
using the CircuitPython library on a Raspberry Pi. It supports initializing the sensor
and reading data from the accelerometer, magnetometer, gyroscope, and temperature sensor.

Prerequisites:
- Install the Adafruit CircuitPython library for the LSM9DS1:
    sudo pip3 install adafruit-circuitpython-lsm9ds1

Functions:
1. setup_imu():
    - Initializes the LSM9DS1 sensor using I2C communication.
    - Returns a sensor object for subsequent readings.

2. read_imu(sensor):
    - Reads and retrieves data from the IMU sensor.
    - Outputs a dictionary containing:
        - Acceleration (m/s^2) on the X, Y, and Z axes.
        - Magnetometer data (gauss) on the X, Y, and Z axes.
        - Gyroscope data (rad/s) on the X, Y, and Z axes.
        - Temperature (°C).
        
"""
import board
import adafruit_lsm9ds1

def setup_imu():
    """Initialize the LSM9DS1 IMU sensor."""
    i2c = board.I2C()  # uses board.SCL and board.SDA
    sensor = adafruit_lsm9ds1.LSM9DS1_I2C(i2c)
    return sensor

def read_imu(sensor):
    """Read data from the IMU sensor."""
    try:
        accel_x, accel_y, accel_z = sensor.acceleration
        mag_x, mag_y, mag_z = sensor.magnetic
        gyro_x, gyro_y, gyro_z = sensor.gyro
        temp = sensor.temperature

        return {
            "acceleration": (accel_x, accel_y, accel_z),
            "magnetometer": (mag_x, mag_y, mag_z),
            "gyroscope": (gyro_x, gyro_y, gyro_z),
            "temperature": temp,
        }
    except Exception as e:
        print(f"Error reading IMU: {e}")
        return None
