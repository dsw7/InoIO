# InoIO
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A small library for RX/TX with Arduino devices. This library assumes that the "backend" is running driver code somewhat akin to:
```c++
void setup()
{
    unsigned int baud_rate = 9600;
    ::Serial.begin(baud_rate);

    unsigned int timeout_msec = 10;
    ::Serial.setTimeout(timeout_msec);
}

void loop()
{
    while (::Serial.available() > 0)
    {
        ::String message = ::Serial.readString();
        message.trim();

        ::Serial.println("Received message: " + message);
        ::Serial.flush();
    }
}
```
