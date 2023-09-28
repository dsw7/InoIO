from pytest import raises
from inoio import InoIO, errors


def test_invalid_port() -> None:
    conn = InoIO(port=27117)  # type: ignore

    with raises(errors.InoIOConnectionError) as excinfo:
        conn.connect()

    conn.disconnect()
    assert "One or more parameters is of invalid type" in str(excinfo)


def test_invalid_baudrate() -> None:
    conn = InoIO(baudrate="foobar")  # type: ignore

    with raises(errors.InoIOConnectionError) as excinfo:
        conn.connect()

    conn.disconnect()
    assert "One or more parameters is of invalid type" in str(excinfo)


def test_invalid_timeout() -> None:
    conn = InoIO(timeout="foobar")  # type: ignore

    with raises(errors.InoIOConnectionError) as excinfo:
        conn.connect()

    conn.disconnect()
    assert "One or more parameters is of invalid type" in str(excinfo)


def test_invalid_port_init_app() -> None:
    conn = InoIO()
    conn.init_app(port=27117)  # type: ignore

    with raises(errors.InoIOConnectionError) as excinfo:
        conn.connect()

    conn.disconnect()
    assert "One or more parameters is of invalid type" in str(excinfo)


def test_invalid_baudrate_init_app() -> None:
    conn = InoIO()
    conn.init_app(baudrate="foobar")  # type: ignore

    with raises(errors.InoIOConnectionError) as excinfo:
        conn.connect()

    conn.disconnect()
    assert "One or more parameters is of invalid type" in str(excinfo)


def test_invalid_timeout_init_app() -> None:
    conn = InoIO()
    conn.init_app(timeout="foobar")  # type: ignore

    with raises(errors.InoIOConnectionError) as excinfo:
        conn.connect()

    conn.disconnect()
    assert "One or more parameters is of invalid type" in str(excinfo)


def test_connect_disconnect(pytestconfig) -> None:
    port = pytestconfig.getoption("port")

    conn = InoIO(port=port)
    conn.connect()
    conn.write("foobar")

    assert conn.device.is_open

    conn.disconnect()
    assert not conn.device.is_open

    conn.disconnect()
    assert not conn.device.is_open


def test_disconnect_without_connect(pytestconfig) -> None:
    port = pytestconfig.getoption("port")

    conn = InoIO(port=port)
    assert not hasattr(conn, "device")

    conn.disconnect()


def test_multiple_connect(pytestconfig) -> None:
    port = pytestconfig.getoption("port")

    conn = InoIO(port=port)
    conn.connect()
    conn.connect()
    conn.disconnect()
