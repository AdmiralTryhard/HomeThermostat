from machine import Pin, PWM

class led:
    def __init__(self,pin_num,pwm, freq=10000):
        """pin_num -> int, pwm -> bool, freq -> int"""
        self.light = Pin(pin_num, Pin.OUT)
        self.PWM = pwm
        self.pin = pin_num
        self.freq = freq

        if self.PWM == True:
            self.light = PWM(self.light, self.freq)
            
    def set_brightness(self, brightness):
        """This will set brightness from 0 to 1 with 0 being nothing
        and 1 will be fully on.
        NOTE: REQUIRES PWM mode = True
        """
        try:
            if self.PWM:
                self.light.duty(int(brightness * 1023))
            elif brightness == 0 or brightness == 1:
                self.light.value(brightness)
            else:
                print("this value was for pwm, but you do not have a pwm LED at port" + str(self.pin))
                self.light.value(0)
        except:
            print("this is the problem light's pin number.", self.pin)

    def __del__(self):
        if self.PWM:
            self.light.deinit()

            