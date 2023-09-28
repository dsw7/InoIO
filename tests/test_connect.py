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
