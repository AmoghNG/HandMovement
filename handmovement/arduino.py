"""
Interface to talk to the arduino
"""
import serial

from handmovement.schema import ActuatorData


class SerialInterface:
    def __init__(
        self,
        port: str = "COM5",
        baudrate: int = 115200,
    ) -> None:
        # Create a serial object
        self.ser = serial.Serial(timeout=1)

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
        self.ser.flush()
        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()
        data_tuple = actuator_data.to_list()
        # Clip the data b/w (0,100)
        data_list = [min(max(0, x), 100) for x in data_tuple]
        # data = " ".join(map(
        #     lambda x: str(x).zfill(3), data_list
        # ))
        # data += "\n"

        # print(f'sendng to arduino: {data}')
        # print(f'sendng to arduino: {len(data)}')

        # # Send data to Arduino
        # self.ser.write(data.encode())
        data_list = [255] + data_list
        # data_list = [255] + data_list + [255]
        print(data_list)
        # print(bytearray(data_list))
        # print(len(bytearray(data_list)))
        self.ser.write(bytearray(data_list))

        if not wait_for_ack:
            return True

        # Wait for response
        response = self.ser.read(2)

        if len(response) != 2:
            print("Error")
            return False

        response = [x for x in response]
        expected_response = [255, 255]

        print(f"Response: '{response}'")
        print(f"Expected: '{expected_response}'")

        # Check if the data was received
        if response == expected_response:
            print("Data was received by Arduino.")
            return True
        else:
            print("Failed to send data to Arduino.")
            return False
