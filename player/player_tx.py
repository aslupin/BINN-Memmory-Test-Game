import ubinascii
import time
import network
from esp import espnow
from machine import Pin, I2C
import ssd1306
import json

lb = Pin(2, Pin.OUT)


class Button:
    """
    Debounced pin handler
    usage e.g.:
    def button_callback(pin):
        print("Button (%s) changed to: %r" % (pin, pin.value()))
    button_handler = Button(
        pin=Pin(32, mode=Pin.IN, pull=Pin.PULL_UP), callback=button_callback)
    """

    def __init__(self, pin, callback, color='', trigger=Pin.IRQ_FALLING, min_ago=300):
        self.callback = callback
        self.min_ago = min_ago
        self.color = color
        self._blocked = False
        self._next_call = time.ticks_ms() + self.min_ago

        pin.irq(trigger=trigger, handler=self.debounce_handler)

    def call_callback(self, pin):
        self.callback(self.color)
        # self.callback(pin)

    def debounce_handler(self, pin):
        if time.ticks_ms() > self._next_call:
            self._next_call = time.ticks_ms() + self.min_ago
            self.call_callback(pin)
        # else:
        #    print("debounce: %s" % (self._next_call - time.ticks_ms()))

# config OLED
i2c = I2C(-1, scl=Pin(22), sda=Pin(21))
oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)
# config network
w = network.WLAN()
w.active(True)
print('my mac addr (Player):', ubinascii.hexlify(w.config('mac'), ':').decode())


# config esp32
UNICAST_CONTROLLER = b'\x30\xae\xa4\x12\x1f\x28'
# UNICAST_CONTROLLER = b'\x30aea4121f28'
espnow.init()
espnow.add_peer(UNICAST_CONTROLLER)


def setterOLED(*messenger, posy=[]):
    if(not posy):
        posy = [0, 10, 20]

    oled.fill(0)
    for msg in messenger:
        print(msg)
        oled.text(str(msg), 0, posy.pop(0))
    oled.show()

def addLightOnBorad(color):
    print('sw color :' + color)
    global leds
    bitmapColor = {
        'blue': {'blue': 0, "green": 1, 'red': 1},
        'green': {'blue': 1, "green": 0, 'red': 1},
        'red': {'blue': 1, "green": 1, 'red': 0},
    }

    for index in range(3):
        led = str(index + 1)
        for key_color, _ in leds[led].items():
            if(led == '3'):
                leds[led][key_color].value(bitmapColor[color][key_color])
            else:
                prev = str(int(led) + 1)
                leds[led][key_color].value(leds[prev][key_color].value())


def sendToController(color):
    addLightOnBorad(color)
    msg = {}
    msg['player'] = 1  # number of player
    msg['action'] = {}
    msg['action']['color'] = color
    msg['action']['value'] = 1  # True , False
    espnow.send(UNICAST_CONTROLLER, str(msg))
    print('Send success')
    #setterOLED("MODE: playing", color+" pressed!")
    # {
    #     'player' : 1
    #     'action' : {
    #        'color' : 'red'
    #        'value': 1
    #       }
    # }


# config leds
leds = {}
leds_pins = {
    '1': {'blue': 27, "green": 15, 'red': 14},
    '2': {'blue': 33, "green": 26, 'red': 25},
    '3': {'blue': 19, "green": 32, 'red': 18}
}


def setLed():
    for led, pins in leds_pins.items():
        leds[led] = {}
        for color, val in pins.items():
            leds[led][color] = Pin(val, Pin.OUT)
            leds[led][color].value(1)

            # {
            # '1': {'blue': 1, 'green': 1, 'red': 1},
            # '2': {'blue': 1, 'green': 1, 'red': 1},
            # '3': {'blue': 1, 'green': 1, 'red': 1}
            # } # 1 = Pin


setLed()
# config switchs
switchs = {}
switch_pins = {'blue': 16, "green": 17, 'red': 5}

for key, val in switch_pins.items():
    switchs[key] = Button(pin=Pin(
        val, mode=Pin.IN, pull=Pin.PULL_UP), callback=sendToController, color=key)

# unit test

# switchs['blue'] = Button(pin=Pin(16, mode=Pin.IN, pull=Pin.PULL_UP), callback=button_a_callback)
# switchs['blue'] = Button(pin=Pin(17, mode=Pin.IN, pull=Pin.PULL_UP), callback=button_a_callback)
# switchs['red'] = Button(pin=Pin(5, mode=Pin.IN, pull=Pin.PULL_UP), callback=button_b_callback)
# addLightOnBorad('green')
# addLightOnBorad('red')
# leds['1']['blue'].value(0)
# leds['1']['green'].value(0)
# leds['1']['red'].value(0)
# leds['2']['blue'].value(0)
# leds['2']['green'].value(0)
# leds['2']['red'].value(0)
# leds['3']['blue'].value(0)
# leds['3']['green'].value(0)
# leds['3']['red'].value(0)


def recieveFromController(*dobj):
    global connect
    msg = dobj[0][1].decode("utf-8")
    mac = ''.join(["{:02X}".format(x) for x in dobj[0][0]])
    controller_mac = ''.join(["{:02X}".format(x) for x in UNICAST_CONTROLLER])
    # print(dobj, msg)
    if(mac == controller_mac):
        if(not connect):           
            if(msg == 'connecting'):
                connect = True
        else:
            # connected 
            '''
            msg['msg'] should be tuple<string>: 
            msg['msg'] = "'1','2','3'" => msgs = ('1','2','3')

            setterOLED will parse each arguments to newline.
            parse for tuple<string>
            '''
            print('old:', msg)
            msg = msg.replace("\"", "$") 
            msg = msg.replace("'", "\"")
            msg = msg.replace("$", "'")
            print('new:', msg)
            msg = json.loads(msg)
            msgs = eval(msg['msg'])   
            setterOLED(*msgs) 
            
            


connect = False
start = False

espnow.on_recv(recieveFromController)
setterOLED('connecting...')
while (not connect):
    
    print('wait for connection...')
    time.sleep(1)
    lb.on()
    time.sleep(1)
    lb.off()
setterOLED('connected')
print('connected')
espnow.send(UNICAST_CONTROLLER, 'connected')
connect = True
setLed()
lb.on()  # connect

while True:
    pass
