"""
This script serves as the central controller for the autonomous submersible vehicle.
It handles the following operations:
1. IMU Calibration and Data Processing:
   - Collects and processes data from the Inertial Measurement Unit (IMU) using a 
     separate process to continuously update the shared data dictionary with 
     acceleration, magnetometer, gyroscope, and temperature readings.

2. Ultrasonic Sensor Operations:
   - Processes data from ultrasonic sensors to detect walls or obstacles in the environment.

3. Movement Control:
   - Coordinates movement control for the submersible, including direction adjustments
     (horizontal, vertical, turning, and pitching) based on sensor feedback.

4. Object Detection:
   - Integrates YOLOv8-based object detection to identify and track objects underwater.
"""

from multiprocessing import Process, Value, Manager, Queue
from background_process import ultrasonic_reading_process, imu_reading_process, start_detection_process, stop_detection_process
from modules.movement_mod import move_horizontal, move_vertical, turn, pitch
from modules.calibration_mod import imu_adjustment
import time
from picamera2 import Picamera2


def check_distance(shared_distance):
    """Function to check the current distance value."""
    with shared_distance.get_lock():
        return shared_distance.value

def movement(screen_x, screen_y, x_center, y_center):
    """
    Calculate movement adjustments based on detected positions.
    """
    move_x = screen_x - x_center
    move_y = screen_y - y_center
    print(f"Move X: {move_x}, Move Y: {move_y}")
    # Add motor control commands here
    #NEED TO CHANGE THE PARAMS 
    move_horizontal(move_x)  # Example: move in the x-direction
    move_vertical(move_y)    # Example: move in the y-direction
    #now just move forwards 
    return move_x, move_y

if __name__ == "__main__":
    # Shared variable to store distance
    distance_value = Value('d', -1.0)  # 'd' stands for double (float)

    with Manager() as manager:
        imu_data = manager.dict()
        detection_queue = Queue()  # Queue to receive detection results

        # Start the ultrasonic sensor process
        ultrasonic_process = Process(target=ultrasonic_reading_process, args=(distance_value,))
        ultrasonic_process.start()

        # Start the IMU sensor process
        imu_process = Process(target=imu_reading_process, args=(imu_data,))
        imu_process.start()

        # Start the detection process
        detection_process = Process(target=start_detection_process, args=(detection_queue,))
        detection_process.start()

        picam2 = Picamera2()
        frame = picam2.capture_array()
        screen_height, screen_width, _ = frame.shape
        screen_x, screen_y = screen_width // 2, screen_height // 2

        # Example screen center coordinates
        # screen_x, screen_y = 320, 240  # Adjust based on your resolution


        try:
            while True:
                # Check and print the ultrasonic distance in real-time
                distance = check_distance(distance_value)
                print(f"Ultrasonic Sensor Distance: {distance} mm")

                # Perform IMU adjustments
                imu_adjustment(imu_data)

                # Check for detection results
                if not detection_queue.empty():
                    x_center, y_center = detection_queue.get()
                    print(f"Detected Object Center: ({x_center}, {y_center})")

                    # Adjust movement based on detection
                    movement(screen_x, screen_y, x_center, y_center)

                time.sleep(1.0)  # Adjust the loop frequency as needed
        except KeyboardInterrupt:
            print("Stopping main process...")

            # Terminate all processes
            ultrasonic_process.terminate()
            imu_process.terminate()
            detection_process.terminate()

            ultrasonic_process.join()
            imu_process.join()
            detection_process.join()

            stop_detection_process()  # Clean up detection resources
