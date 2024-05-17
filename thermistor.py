from machine import Pin, ADC
import time
import math

class Thermostat():
    def __init__(self, port):
        self.port = port
        self.adc = ADC(Pin(port))
        self.adc.atten(ADC.ATTN_11DB)
        self.adc.width(ADC.WIDTH_11BIT)
        
    def getKelvin(self):
        """converts voltage to temperatures that are close to working. Resistor variance can mess with it"""
        adcValue = self.adc.read()
        voltage=adcValue/4095*3.3
        Rt=10*voltage/(3.3-voltage)
        tempK=(1/(1/(273.15+25)+(math.log(Rt/10))/3950))
        return tempK - 6

    def getCelsius(self):
        return self.getKelvin() - 273.15

    def getFahrenheit(self):
        return (self.getCelsius() * 9.0 / 5) + 32
