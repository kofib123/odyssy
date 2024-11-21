import serial
import time


# Configure the UART port
serial_port = '/dev/serial0'  # Raspberry Pi's UART
baud_rate = 115200
ser = serial.Serial(serial_port, baud_rate, timeout=1)

COM = 0x55
buffer_RTT = [0, 0, 0, 0]

def calculate_checksum(buffer):
    """Calculate checksum."""
    return buffer[0] + buffer[1] + buffer[2]

def read_distance():
    """Read distance from ultrasonic sensor."""
    global buffer_RTT
    # Send the command byte
    ser.write(bytes([COM]))
    time.sleep(0.1)  # Small delay to allow response

    # Check if data is available
    if ser.in_waiting > 0:
        time.sleep(0.004)  # Slight delay to ensure complete data is read
        first_byte = ser.read(1)
        if first_byte == b'\xff':  # Check for start byte
            buffer_RTT[0] = 0xFF
            # Read the next 3 bytes
            for i in range(1, 4):
                buffer_RTT[i] = ord(ser.read(1))  # Convert byte to int

            # Calculate checksum
            CS = calculate_checksum(buffer_RTT)
            if buffer_RTT[3] == CS:
                # Calculate distance in mm
                distance = (buffer_RTT[1] << 8) + buffer_RTT[2]
                print(f"Distance: {distance} mm")
                return distance
            else:
                print("Checksum mismatch")
        else:
            print("Invalid start byte")

    return None

# Main loop
try:
    while True:
        distance = read_distance()
        time.sleep(0.1)  # Adjust based on sensor's refresh rate
except KeyboardInterrupt:
    print("Exiting program...")
    ser.close()
