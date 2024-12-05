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
from background_process import ultrasonic_reading_process, imu_reading_process, detection_loop
from modules.movement_mod import move_horizontal, move_vertical, turn, pitch
from modules.calibration_mod import imu_adjustment


import time

def check_distance(shared_distance):
    """Function to check the current distance value."""
    with shared_distance.get_lock():
        return shared_distance.value

if __name__ == "__main__":
    # Shared variables and queues
    frame_queue = queue.Queue(maxsize=1)
    with Manager() as manager:
        shared_data = manager.dict()

        # Start the IMU process
        imu_process = Process(target=imu_reading_process, args=(shared_data))
        imu_process.start()

        # Start the detection process
        model_path = "/path/to/your/model"
        detection_process = Process(target=detection_loop, args=(frame_queue, shared_data, model_path))
        detection_process.start()

        try:
            while True:
                # Access shared data
                detections = shared_data.get("detections", [])
                print(f"Detected Objects: {detections}")

                # Display frames from the queue
                try:
                    annotated_frame = frame_queue.get(timeout=1)
                    cv2.imshow("Camera", annotated_frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                except queue.Empty:
                    continue

        except KeyboardInterrupt:
            print("Stopping main process...")
        finally:
            # Clean up processes
            imu_process.terminate()
            detection_process.terminate()
            imu_process.join()
            detection_process.join()
            cv2.destroyAllWindows()
