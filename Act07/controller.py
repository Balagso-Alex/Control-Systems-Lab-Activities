import serial
import time
import sys

# Configuration
SERIAL_PORT = '/dev/cu.usbmodem21401'  # Update to your Arduino's port
BAUD_RATE = 9600

def initialize_serial_connection(port, baud_rate):
    try:
        ser = serial.Serial(port, baud_rate, timeout=1)
        time.sleep(2)  # Wait for Arduino reset
        if ser.is_open:
            print(f"Connected to {port} at {baud_rate} bps.")
            return ser
    except serial.SerialException as e:
        print(f"ERROR: Port {port} inaccessible.")
        return None

def send_angle_to_arduino(ser_conn, angle):
    if ser_conn and ser_conn.is_open:
        command = str(angle) + '\n'
        ser_conn.write(command.encode('utf-8'))
        print(f"[Python] Sent: {angle}°")

if __name__ == "__main__":
    arduino_serial = initialize_serial_connection(SERIAL_PORT, BAUD_RATE)
    if not arduino_serial: sys.exit(1)

    try:
        while True:
            user_input = input("Enter angle (0-180, 'q' to quit): ").strip()
            if user_input.lower() == 'q': break
            
            try:
                degrees = int(user_input)
                if 0 <= degrees <= 180:
                    send_angle_to_arduino(arduino_serial, degrees)
                else:
                    print("Out of range (0-180).")
            except ValueError:
                print("Invalid input.")
            time.sleep(0.05)
    finally:
        if arduino_serial: arduino_serial.close()