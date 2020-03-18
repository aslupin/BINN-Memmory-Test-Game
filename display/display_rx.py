machine = 'display-node'
import ubinascii
import time
import network
from esp import espnow
from machine import Pin

led_buuild_in = Pin(2, Pin.OUT)

def starter():
    global led_buuild_in
    print("Start: " + machine)
    led_buuild_in.value(1) # turn LED on
    time.sleep(1)
    led_buuild_in.value(0) # turn LED off
    time.sleep(1)

def gameI(game):
    global leds
    for val in game:
        leds[val.color].value(val.value)
        time.sleep(5)

def gameII(game):
    global leds
    for val in game:
        leds[val.color].value(val.value)
        time.sleep(5)


def receive_callback(*dobj):
    msg = dict(dobj)
    
    # {
    #   game: 1,
    #   data: {
    #        color: red,
    #        value: 1   
    #   }
    # }

    print("Received:", msg)
    if(msg['game'] == 1 ):
        gameI(msg['data'])
    elif(msg['game'] == 2):
        gameII(msg['data'])
    
#starter  
starter()

# config network
w = network.WLAN()
w.active(True)
print('my mac addr (Display):', ubinascii.hexlify(w.config('mac'),':').decode())

#config LEDs
leds = {}
led_pins = {'1':4 ,'2':16 ,'3':17 ,'4':18 ,'5':19 ,'6':13}
for key, val in led_pins.items():
    leds[key] = Pin(val, Pin.OUT)

#print(leds, leds['1'], type(leds['1']))

# config espnow
espnow.init()
espnow.on_recv(receive_callback)

while True:
    pass









