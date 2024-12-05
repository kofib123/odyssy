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
import queue
import cv2
from modules.detection_mod import process_frame
from picamera2 import Picamera2
from ultralytics import YOLO


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

def detection_loop(frame_queue, shared_data, model_path, threshold=0.7):
    """
    Infinite loop to perform object detection and update shared data.

    Args:
        frame_queue (queue.Queue): A queue for sharing annotated frames.
        shared_data (dict): A shared dictionary for detected objects.
        model_path (str): Path to the YOLO model.
        threshold (float): Confidence threshold for detection.
    """
    # Initialize the camera and model
    picam2 = Picamera2()
    picam2.preview_configuration.main.size = (640, 480)
    picam2.preview_configuration.main.format = "RGB888"
    picam2.preview_configuration.align()
    picam2.configure("preview")
    picam2.start()

    model = YOLO(model_path)
    model.fuse()

    print("Detection loop initialized and running.")

    try:
        while True:
            # Capture a frame
            frame = picam2.capture_array()

            # Process the frame using detection_code.py
            annotated_frame, detected_objects = process_frame(frame, model, threshold)

            # Update shared data
            shared_data["detections"] = detected_objects

            # Add annotated frame to queue
            try:
                frame_queue.put(annotated_frame, block=False)
            except queue.Full:
                try:
                    frame_queue.get_nowait()
                    frame_queue.put(annotated_frame, block=False)
                except queue.Empty:
                    pass

    except KeyboardInterrupt:
        print("Stopping detection loop...")
    finally:
        picam2.stop()
