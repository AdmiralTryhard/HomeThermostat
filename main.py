import asyncio
import thermistor
import json
from microdot import Microdot
from websocket import with_websocket
from wifi import Wifi
from display import Display
from RotaryEncoder import RotaryEncoder
from RGB import rgb_led


wifi = Wifi('WIFI NAME GOES HERE', 'WIFI PASSWORD GOES HERE')

display = Display(23, 22) #local display working via I2C
ip_address = wifi.get_ip_addr()
display.text(0, ip_address) # initial set up needs to be by the ESP32
display.show()

thermo = thermistor.Thermostat(36)

light = rgb_led(0, 4, 5)
light.set_light(0.25, 0, 0.25, True)

temp = thermo.getFahrenheit()
desired = 68

port = 8080
app = Microdot()

#local functions
def check_heat(goal):
    global light

    if thermo.getFahrenheit() + 2.0 < goal:
        light.update_red(1.0)
    else:
        light.update_red(0.25)
    light.enact_color_update()


def check_cool(goal):
    global light
    if thermo.getFahrenheit() - 2.0 > goal:
        light.update_blue(1.0)
    else:
        light.update_blue(0.25)

    light.enact_color_update()
    
    
#Web functions
@app.route('/')
async def index(request):
    ipaddr = ip_address
    with open('index.html', 'r') as f:
        text = f.read().replace('ADDRESS', f'{ipaddr}:{port}')
        return text, {'Content-Type': 'text/html'}


@app.route('/update')
@with_websocket
async def temperature(request, ws):
    def local_temp_update(change):
        """this is the temperature being changed by the rotary encoder"""
        global desired, stagnating
        stagnating = False
        new_desire = desired + change
        # temps are clamped between 60 and 80. Not sure who would want temps out of this range
        new_desire = max(60, new_desire)
        new_desire = min(80, new_desire)

        desired = new_desire
        
        check_cool(int(desired)) #desired is sent as a string
        check_heat(int(desired))
        actively_heating = light.r == 1.0
        actively_cooling = light.b == 1.0
        
        
        data = {
            "Cooling": actively_heating,
            "Heating": actively_cooling,
            "Desired": desired,
            "CurrentTemp": thermo.getFahrenheit()}
        display_text = "desired temp: " + str(desired)

        display.clear()
        display.text(0, display_text)
        display.show()

        asyncio.run(ws.send(json.dumps(data)))

    rotator = RotaryEncoder(18, 19, local_temp_update) # handler function when rotated
    while True:
        desired = await ws.receive()
        check_cool(int(desired))
        check_heat(int(desired))
        actively_heating = light.r == 1.0
        actively_cooling = light.b == 1.0
        
        data = {
            "Cooling": actively_heating,
            "Heating": actively_cooling,
            "Desired": desired,
            "CurrentTemp": thermo.getFahrenheit()}
        display.clear()
        display_text = "desired temp: " + str(desired)
        display.text(0, display_text)
        display.show()

        await ws.send(json.dumps(data))


try:
    app.run(port=port)

finally:
    light.set_light(0,0,0)
