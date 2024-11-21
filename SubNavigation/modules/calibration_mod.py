"""
This module is in charge of the calibration/stabilization of the vehicle. This will heavily depend on the motion of it
"""
from modules.movement_mod import move_horizontal, move_vertical, turn, pitch

def imu_adjustment(shared_data: dict):
    """
    Perform real-time adjustment using IMU data.
    - Fetch IMU readings from the shared dictionary.
    - Compute required adjustments (e.g., pitch, roll, yaw).
    - Apply corrections to stabilize or reorient the vehicle.
    """
    try:
        # Fetch IMU data from the shared dictionary
        acceleration = shared_data.get("acceleration", (0.0, 0.0, 0.0))
        gyroscope = shared_data.get("gyroscope", (0.0, 0.0, 0.0))
        magnetometer = shared_data.get("magnetometer", (0.0, 0.0, 0.0))
        temperature = shared_data.get("temperature", 0.0)

        # Print IMU readings for debugging
        print(f"Acceleration: {acceleration}")
        print(f"Gyroscope: {gyroscope}")
        print(f"Magnetometer: {magnetometer}")
        print(f"Temperature: {temperature:.3f}°C")

        # TODO: Add adjustment logic based on IMU readings

    except Exception as e:
        print(f"Error during IMU adjustment: {e}")