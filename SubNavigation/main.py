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
     
"""

from multiprocessing import Process, Value, Manager
from background_process import ultrasonic_reading_process, imu_reading_process
from modules.movement_mod import move_horizontal, move_vertical, turn, pitch
from modules.calibration_mod import imu_adjustment


import time

def check_distance(shared_distance):
    """Function to check the current distance value."""
    with shared_distance.get_lock():
        return shared_distance.value

if __name__ == "__main__":
    # Shared variable to store distance
    distance_value = Value('d', -1.0)  # 'd' stands for double (float)

    with Manager() as manager:
        imu_data = manager.dict()

        # Start the ultrasonic sensor process
        ultrasonic_process = Process(target=ultrasonic_reading_process, args=(distance_value,))
        ultrasonic_process.start()

        # Start the IMU sensor process
        imu_process = Process(target=imu_reading_process, args=(imu_data,))
        imu_process.start()

        try:
            while True:
                # Check and print the ultrasonic distance in real-time
                distance = check_distance(distance_value)
                print(f"Ultrasonic Sensor Distance: {distance} mm")

                # Perform IMU adjustments
                imu_adjustment(imu_data)

                time.sleep(1.0)  # Adjust the loop frequency as needed
        except KeyboardInterrupt:
            print("Stopping main process...")

            # Terminate both processes
            ultrasonic_process.terminate()
            imu_process.terminate()

            ultrasonic_process.join()
            imu_process.join()
