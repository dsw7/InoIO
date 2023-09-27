from logging import getLogger
from time import sleep
from typing import Tuple
import serial
from inoio import errors


class InoIO:

    """Class for interfacing with an Arduino device.

    :param int, optional baudrate: Specify the baud rate.
    :param float, optional timeout: Specify the read timeout in sections.
    :param str, optional port: Specify the device name (i.e. "COM3" on Windows) or path to device
        (i.e. "/dev/ttyS2" on Linux).
    """

    logger = getLogger("inoio")

    def __init__(
        self,
        baudrate: int = 9600,
        port: str = "/dev/ttyS2",
        timeout: float = 5.00,
    ) -> None:
        self.baudrate = baudrate
        self.encoding = "utf-8"
        self.port = port
        self.timeout = timeout

        self.serial_port_obj: serial.Serial

    def init_app(
        self,
        baudrate: int,
        port: str,
        timeout: float,
    ) -> None:
        """Override parameters specified via class constructor. This method is useful
        for setting connection parameters if the InoIO class is being used as a Flask extension,
        for example. For more information, see https://flask.palletsprojects.com/en/2.3.x/extensions/

        :param int, optional baudrate: Specify the baud rate.
        :param float, optional timeout: Specify the read timeout in sections.
        :param str, optional port: Specify the device name (i.e. "COM3" on Windows) or path to device
            (i.e. "/dev/ttyS2" on Linux).
        """

        self.baudrate = baudrate
        self.port = port
        self.timeout = timeout

    def connect(self) -> None:
        """Connect to device.

        :raise InoIOConnectionError: If a connection could not be established.
        """

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
        except serial.serialutil.SerialException as e:
            raise errors.InoIOConnectionError(
                f"Could not connect on {self.port}"
            ) from e

        if not self.serial_port_obj.is_open:
            raise errors.InoIOConnectionError(f"No connection is open on {self.port}")

        # Opening a connection will send a DTR (Data Terminal Ready) signal to device, which will
        # force the device to reset. Give device 2 seconds to reset

        self.logger.debug(
            "DTR (Data Terminal Ready) was sent. Waiting for device to reset"
        )
        sleep(2)

        self.logger.debug("Device ready to accept input on %s", self.port)

    def disconnect(self) -> None:
        """Disconnect from device."""

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
