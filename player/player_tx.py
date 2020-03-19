
import ubinascii
import time
import network
from esp import espnow
from machine import Pin
lb = Pin(2, Pin.OUT)
class Button:
    """
    Debounced pin handler
    usage e.g.:
    def button_callback(pin):
        print("Button (%s) changed to: %r" % (pin, pin.value()))
    button_handler = Button(pin=Pin(32, mode=Pin.IN, pull=Pin.PULL_UP), callback=button_callback)
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
        #self.callback(pin)

    def debounce_handler(self, pin):
        if time.ticks_ms() > self._next_call:
            self._next_call = time.ticks_ms() + self.min_ago
            self.call_callback(pin)
        #else:
        #    print("debounce: %s" % (self._next_call - time.ticks_ms()))

def button_a_callback(pin):
    print("Button A (%s) changed to: %r" % (pin, pin.value()))
    #lb.value(not lb.value())


def button_b_callback(pin):
    print("Button B (%s) changed to: %r" % (pin, pin.value()))


# config network
w = network.WLAN()
w.active(True)
print('my mac addr (Player):', ubinascii.hexlify(w.config('mac'),':').decode())


# config esp32
UNICAST_CONTROLLER = b'\x240ac49f5058'
espnow.init()
espnow.add_peer(UNICAST_CONTROLLER)

def addLightOnBorad(color):
    print('sw color :' + color)
    global leds
    bitmapColor = {
        'blue' :{'blue':0 ,"green":1 ,'red':1},
        'green':{'blue':1 ,"green":0 ,'red':1},
        'red'  :{'blue':1 ,"green":1 ,'red':0},
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
    msg['player'] = 1 # number of player
    msg['action'] = {}
    msg['action']['color'] = color
    msg['action']['value'] = 1 # True , False
    espnow.send(UNICAST_CONTROLLER, str(msg))
    print('Send success')

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
    '1':{'blue':27 ,"green":15 ,'red':14},
    '2':{'blue':33 ,"green":26 ,'red':25},
    '3':{'blue':19 ,"green":32 ,'red':18}
    }

for led, pins in leds_pins.items():
    leds[led] = {}
    for color, val in pins.items():
        leds[led][color] = Pin(val, Pin.OUT)
        leds[led][color].value(1)
        #{
        # '1': {'blue': 1, 'green': 1, 'red': 1}, 
        # '2': {'blue': 1, 'green': 1, 'red': 1}, 
        # '3': {'blue': 1, 'green': 1, 'red': 1}
        # } # 1 = Pin

# config switchs
switchs = {}
switch_pins = {'blue':16 ,"green":17 ,'red':5}

for key, val in switch_pins.items():
    switchs[key] = Button(pin=Pin(val, mode=Pin.IN, pull=Pin.PULL_UP), callback=sendToController, color=key)

### unit test

#switchs['blue'] = Button(pin=Pin(16, mode=Pin.IN, pull=Pin.PULL_UP), callback=button_a_callback)
#switchs['blue'] = Button(pin=Pin(17, mode=Pin.IN, pull=Pin.PULL_UP), callback=button_a_callback)
#switchs['red'] = Button(pin=Pin(5, mode=Pin.IN, pull=Pin.PULL_UP), callback=button_b_callback)
#addLightOnBorad('green')
#addLightOnBorad('red')
#leds['1']['blue'].value(0)
#leds['1']['green'].value(0)
#leds['1']['red'].value(0)
#leds['2']['blue'].value(0)
#leds['2']['green'].value(0)
#leds['2']['red'].value(0)
#leds['3']['blue'].value(0)
#leds['3']['green'].value(0)
#leds['3']['red'].value(0)
    
while True:
    pass

    