"""
background_process.py

This file contains separate processes to handle real-time sensor operations, including
ultrasonic sensor readings and IMU (Inertial Measurement Unit) data collection. By using
Python's multiprocessing module, each sensor runs in its own process, ensuring that data
is continuously updated without blocking the main program or other operations.

Processes:
1. sensor_reading_process: Reads distance data from an ultrasonic sensor and updates 
   a shared value for real-time access by other parts of the program.
2. imu_reading_process: Reads accelerometer, magnetometer, gyroscope, and temperature 
   data from an IMU sensor and updates a shared dictionary for real-time use.

Modules Used:
- ultrasonic_mod: Contains functions for setting up and reading ultrasonic sensors.
- inertial_mod: Contains functions for initializing and reading IMU sensor data.
- movement_mod: Provides functions for controlling movement, including horizontal, vertical, 
  turning, and pitch adjustments.

Shared Data:
- `shared_distance` (Value): Holds the current distance measured by the ultrasonic sensor.
- `shared_data` (dict): Holds the latest IMU readings, including acceleration, magnetometer,
  gyroscope, and temperature data.

This architecture ensures modularity and allows the main program to access sensor data in 
real-time, enabling tasks like navigation, object detection, and control.
"""

from multiprocessing import Process, Value, Queue
from modules.ultrasonic_mod import setup_sensor, read_sensor
from modules.inertial_mod import setup_imu, read_imu
from Visual_Detection.Working_detection_code import detect_code, stop_camera
import time

def ultrasonic_reading_process(shared_distance):
    """Process to continuously read the sensor."""
    ser = setup_sensor()
    try:
        while True:
            distance = read_sensor(ser)
            if distance is not None:
                with shared_distance.get_lock():
                    shared_distance.value = distance
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Stopping sensor process...")
    finally:
        ser.close()
        

def imu_reading_process(shared_data):
    """Process to continuously read IMU data."""
    sensor = setup_imu()
    print("IMU initialized and running.")
    while True:
        try:
            data = read_imu(sensor)
            if data:
                shared_data["acceleration"] = data["acceleration"]
                shared_data["magnetometer"] = data["magnetometer"]
                shared_data["gyroscope"] = data["gyroscope"]
                shared_data["temperature"] = data["temperature"]
            time.sleep(1.0)  # Adjust based on desired update rate
        except KeyboardInterrupt:
            print("Stopping IMU process...")
            break



def start_detection_process(result_queue):
    """
    Start the detection process from Working_DetectionCode.
    """
    detect_code(result_queue)  # Call the detection function

def stop_detection_process():
    """
    Stop the camera when exiting the detection process.
    """
    stop_camera()
