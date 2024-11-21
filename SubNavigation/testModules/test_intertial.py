from modules.inertial_mod import setup_imu, read_imu
import time

def test_imu():
    """Test the IMU sensor by reading data 10 times."""
    try:
        # Initialize the IMU sensor
        sensor = setup_imu()
        print("IMU initialized successfully.")
        print("Reading IMU data...")

        # Read and print sensor data 10 times
        for _ in range(10):
            data = read_imu(sensor)
            if data:
                print("Acceleration (m/s^2):", data["acceleration"])
                print("Magnetometer (gauss):", data["magnetometer"])
                print("Gyroscope (rad/s):", data["gyroscope"])
                print("Temperature (°C):", data["temperature"])
            else:
                print("Failed to read data from IMU.")
            time.sleep(1)  # Delay between readings
    except Exception as e:
        print(f"Error testing IMU: {e}")

# Run the test
if __name__ == "__main__":
    test_imu()
