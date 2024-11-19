import serial
import time

# Configure the serial port
serial_port = '/dev/serial0'
baud_rate = 115200
COM = 0x55

def calculate_checksum(buffer):
    """Calculate checksum."""
    return buffer[0] + buffer[1] + buffer[2]

def read_sensor(ser):
    """Read distance from the ultrasonic sensor."""
    buffer_RTT = [0, 0, 0, 0]
    ser.write(bytes([COM]))
    time.sleep(0.1)

    if ser.in_waiting > 0:
        time.sleep(0.004)  # Ensure full message is read
        first_byte = ser.read(1)
        if first_byte == b'\xff':  # Check for start byte
            buffer_RTT[0] = 0xFF
            for i in range(1, 4):
                buffer_RTT[i] = ord(ser.read(1))
            
            CS = calculate_checksum(buffer_RTT)
            if buffer_RTT[3] == CS:
                distance = (buffer_RTT[1] << 8) + buffer_RTT[2]
                return distance
            else:
                print("Checksum mismatch")
    return None

def setup_sensor():
    """Setup the serial connection for the sensor."""
    return serial.Serial(serial_port, baud_rate, timeout=1)
