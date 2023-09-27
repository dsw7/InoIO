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
