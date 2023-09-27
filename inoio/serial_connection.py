import sys
from logging import getLogger
from time import sleep
from typing import Tuple
import serial


class InoIO:
    logger = getLogger("inoio")

    def __init__(
        self,
        baudrate: int = 9600,
        encoding: str = "utf-8",
        port: str = "/dev/ttyS2",
        timeout: float = 5.00,
    ) -> None:
        self.baudrate = baudrate
        self.encoding = encoding
        self.port = port
        self.timeout = timeout

        self.serial_port_obj: serial.Serial

    def connect(self) -> None:
        try:
            self.serial_port_obj = serial.Serial(
                baudrate=self.baudrate,
                port=self.port,
                timeout=self.timeout,
                # Defaults used by Serial.begin()
                # See www.arduino.cc/reference/en/language/functions/communication/serial/begin/
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
            )
        except serial.serialutil.SerialException as exception:
            sys.exit(f'An exception occurred when connecting: "{exception}"')

        if not self.serial_port_obj.is_open:
            sys.exit(f'Could not connect to "{self.serial_port_obj.name}"')

        # Opening a connection will send a DTR (Data Terminal Ready) signal to device, which will
        # force the device to reset. Give device 2 seconds to reset

        self.logger.debug(
            "DTR (Data Terminal Ready) was sent. Waiting for device to reset"
        )
        sleep(2)

        self.logger.debug("Device ready to accept instructions!")

    def disconnect(self) -> None:
        if self.serial_port_obj is None:
            self.logger.debug("Not closing connection. Connection was never opened!")
            return

        self.logger.debug("Closing connection!")

        if self.serial_port_obj.is_open:
            self.serial_port_obj.close()

    def send_message(self, message: str) -> None:
        self.logger.debug('Sending message: "%s"', message)
        message_encoded = message.encode(encoding=self.encoding)

        self.logger.debug("Sent %i bytes", self.serial_port_obj.write(message_encoded))
        self.serial_port_obj.flush()

    def receive_message(self) -> Tuple[bool, str]:
        self.logger.debug("Waiting to receive message...")
        message_received = False

        while not message_received:
            while self.serial_port_obj.in_waiting < 1:
                pass

            bytes_from_dev = (
                self.serial_port_obj.read_until()
            )  # Reads until \n by default
            message_received = True

        if len(bytes_from_dev) > 80:
            self.logger.debug("Received message: %s...", bytes_from_dev[:80])
            self.logger.debug("Message was truncated due to excessive length")
        else:
            self.logger.debug("Received message: %s", bytes_from_dev)

        try:
            results = bytes_from_dev.decode(self.encoding).strip()
        except UnicodeDecodeError as e:
            return False, f'An exception occurred when decoding results: "{e}"'

        status, message = results.split(";")

        return int(status) == 1, message
