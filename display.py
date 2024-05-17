from machine import Pin, SoftI2C
import ssd1306

class Display:
    def __init__(self, sda, scl):
        i2c = SoftI2C(sda=Pin(sda), scl=Pin(scl))
        self.buffer = ssd1306.SSD1306_I2C(128, 64, i2c)
        self.clear()
        self.show()
        
    def text(self, line, text):
        self.buffer.text(text, 0, line*8)
        
    def show(self):
        self.buffer.show()
        
    def clear(self):
        self.buffer.fill(0)