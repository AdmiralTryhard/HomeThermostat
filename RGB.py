import LED
from machine import Pin,PWM
import random
import time


class rgb_led:
    def __init__(self, pinr, ping, pinb):
        """rgb leds are just 3 lights hooked up into 1 component, each one needs a pin on the ESP32"""
        self.red = LED.led(pinr, True)
        self.green = LED.led(ping, True)
        self.blue = LED.led(pinb, True)
        self.r = 0
        self.g = 0
        self.b = 0
    
    
    def set_light(self, r, g, b, update=False):
        """use this to set a specific color from 0 to 1 for all colors"""
    
        self.red.set_brightness(1 - (r*r))
        self.green.set_brightness(1 - (g*g))
        self.blue.set_brightness(1 - (b*b))
        if update:
            self.update_red(r)
            self.update_green(g)
            self.update_blue(b)
    
    def update_red(self, new_value):
        """use to manipulate singular values without erasing others"""
        self.r = new_value


    def update_green(self, new_value):
        """use to manipulate singular values without erasing others"""
        self.g = new_value
            
            
    def update_blue(self, new_value):
        """use to manipulate singular values without erasing others"""

        self.b = new_value


    def enact_color_update(self):
        """changes color to the current stored values."""
        self.set_light(self.r, self.g, self.b)
        
    
    def rave_mode(self, seconds):
        """constantly update own value and go to sleep."""
        for i in range(100*seconds):
            self.enact_color_update()
            time.sleep_ms(10)
    
    def random_color(self):
    
        color_values = [random.random() for _ in range(3)]
        self.set_light(color_values[0], color_values[1], color_values[2])
    
        return color_values
    
    def __del__(self):
        del(self.red)
        del(self.green)
        del(self.blue)
        