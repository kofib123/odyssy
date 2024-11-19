""" Run This on Raspberry Pi: sudo pip3 install adafruit-circuitpython-lsm9ds1"""
import time
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
