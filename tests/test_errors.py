from pytest import raises
from inoio import InoIO, errors


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
