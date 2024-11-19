from multiprocessing import Process, Value
from background_process import ultrasonic_reading_process, imu_reading_process
from modules.movement_mod import move_horizontal, move_vertical, turn, pitch

import time

def check_distance(shared_distance):
    """Function to check the current distance value."""
    with shared_distance.get_lock():
        return shared_distance.value

if __name__ == "__main__":
    # Shared variable to store distance
    distance_value = Value('d', -1.0)  # 'd' stands for double (float)

    # Start the background process
    process = Process(target=ultrasonic_reading_process, args=(distance_value,))
    process.start()

    try:
        while True:
            # Check and print the distance in real-time
            distance = check_distance(distance_value)
            print(f"Current Distance: {distance} mm")
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("Stopping main process...")
        process.terminate()
        process.join()
