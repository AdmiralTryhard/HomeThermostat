# Home Thermometer
Do you want to remotely control your home temperatures? Fear not, for I have made the solution!

## Hardware Setup

This product needs the following: an ESP32 with Micropython running on it, a GPIO extension board, a bread board, an RGB LED, associated resistors, a rotary encoder, a screen capable of I2C communication, and cables

Each component was assembled with help from [Freenove](https://freenove.com)'s tutorials

## How it works
The product uses the ESP32 to connect to the Wifi. The ESP 32 will tell the screen to display an ip address to connect to. It will use port 8080. When connected, you can update the desired temperature with either the rotary encoder or the web page. Both stay synced with the use of web sockets. When you update one of the values, the other will show (so both the screen and webpage show the same desired temperature in Fahrenheit).

When a new temperature is given, the ESP32 will check the thermistor's resistance to get a temperature. If the temperature is within 2 degrees of the desired, the light will be a dim purple. Should the desired temp be higher, then the light will turn red. Should you need to cool things down, the light will turn blue.

The light simulation is in place of a real home thermometer system where it would just tell the furnace or air conditioning to turn on.
Should you actually want to hook this up, you would have to either work with your home's desired temperature system or make sure it can continuously check so that your furnace isn't blasting.

