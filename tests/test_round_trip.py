from random import choice
from string import ascii_letters, digits
from typing import Generator
from pytest import mark, fixture
from inoio import InoIO


def generate_random_string(num_strings: int, len_strings: int) -> list[str]:
    alphanumeric = ascii_letters + digits

    result = []

    for _ in range(num_strings):
        result.append("".join(choice(alphanumeric) for _ in range(len_strings)))

    return result


@fixture(scope="module")
def connection() -> Generator[InoIO, None, None]:
    conn = InoIO(port="/dev/ttyS2")
    conn.connect()

    yield conn
    conn.disconnect()


@mark.parametrize("string", generate_random_string(num_strings=10, len_strings=1))
def test_echo_strings_1(connection: InoIO, string: str) -> None:
    assert connection.write(string) == 1
    assert connection.read() == f"Received message: {string}"


@mark.parametrize("string", generate_random_string(num_strings=10, len_strings=15))
def test_echo_strings_15(connection: InoIO, string: str) -> None:
    assert connection.write(string) == 15
    assert connection.read() == f"Received message: {string}"


@mark.parametrize("string", generate_random_string(num_strings=10, len_strings=100))
def test_echo_strings_100(connection: InoIO, string: str) -> None:
    assert connection.write(string) == 100
    assert connection.read() == f"Received message: {string}"
