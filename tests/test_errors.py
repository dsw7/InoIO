from pytest import raises
from inoio import InoIO, errors


def test_invalid_port() -> None:
    conn = InoIO(port=27117)  # type: ignore

    with raises(errors.InoIOConnectionError) as excinfo:
        conn.connect()

    assert "One or more parameters is of invalid type" in str(excinfo)


def test_invalid_baudrate() -> None:
    conn = InoIO(baudrate="foobar")  # type: ignore

    with raises(errors.InoIOConnectionError) as excinfo:
        conn.connect()

    assert "One or more parameters is of invalid type" in str(excinfo)


def test_invalid_timeout() -> None:
    conn = InoIO(timeout="foobar")  # type: ignore

    with raises(errors.InoIOConnectionError) as excinfo:
        conn.connect()

    assert "One or more parameters is of invalid type" in str(excinfo)


def test_connect_disconnect_write(pytestconfig) -> None:
    port = pytestconfig.getoption("port")

    conn = InoIO(port=port)
    conn.connect()
    conn.disconnect()

    with raises(errors.InoIOTransmissionError) as excinfo:
        conn.write("Foobar")

    assert "Cannot send message. No connection is open" in str(excinfo)


def test_connect_disconnect_read(pytestconfig) -> None:
    port = pytestconfig.getoption("port")

    conn = InoIO(port=port)
    conn.connect()
    conn.disconnect()

    with raises(errors.InoIOTransmissionError) as excinfo:
        conn.read()

    assert "Cannot read from device. No connection is open" in str(excinfo)
