"""
Interface to talk to the arduino
"""
import serial

from handmovement.schema import ActuatorData


class SerialInterface:
    def __init__(
        self,
        port: str = "COM5",
        baudrate: int = 57600,
    ) -> None:
        # Create a serial object
        self.ser = serial.Serial()

        # Define the serial port and baud rate.
        self.ser.port = port
        self.ser.baudrate = baudrate

        # Open the serial connection
        self.ser.open()

        # Check if the serial connection is open
        if self.ser.is_open:
            print("Serial connection is open.")
        else:
            print("Failed to open serial connection.")
            raise Exception(f"Error connecting to device({port}, {baudrate})")

    def send_actuator_percs(
        self, actuator_data: ActuatorData, wait_for_ack: bool = False
    ) -> bool:
        data_list = actuator_data.to_list()
        data = ",".join(map(str, data_list))
        data += "\n"

        # Send data to Arduino
        self.ser.write(data.encode())

        if not wait_for_ack:
            return True

        # Wait for response
        response = self.ser.readline().decode().strip()

        print("Response", response)

        # Check if the data was received
        if response == f"Got: {data}":
            print("Data was received by Arduino.")
            return True
        else:
            print("Failed to send data to Arduino.")
            return False
