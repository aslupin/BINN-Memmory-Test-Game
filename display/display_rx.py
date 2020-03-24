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
        if(val == 'green'):
            ledd = ['1','4']
        elif(val == 'red'):
            ledd = ['2','5']
        elif(val == 'blue'):
            ledd = ['3','6']
        leds[ledd[0]].value(0)
        leds[ledd[1]].value(0)
        time.sleep(0.6)
        leds[ledd[0]].value(1)
        leds[ledd[1]].value(1)
        time.sleep(0.1)

def gameII(game):
    global leds
    for val in game:
        if(val == 'green'):
            ledd = ['1','4']
        elif(val == 'red'):
            ledd = ['2','5']
        elif(val == 'blue'):
            ledd = ['3','6']
        leds[ledd[0]].value(0)
        leds[ledd[1]].value(0)
        time.sleep(0.5)
        leds[ledd[0]].value(1)
        leds[ledd[1]].value(1)
        time.sleep(0.1)


def receive_callback(*dobj):
    msg = dict(dobj)
    
    # {
    #   game: 1,
    #   data: {
    #        color: red,
    #        value: 1   
    #   }
    # }

    print("Received: ", msg)
    msg = eval(msg)
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
led_pins = {'1':15 ,'2':16 ,'3':17 ,'4':5 ,'5':18 ,'6':19}
for key, val in led_pins.items():
    leds[key] = Pin(val, Pin.OUT)

for k, v in leds.items():
#     print(v)
    v.value(1)
    
# print(leds, leds['1'], type(leds['1']))

#config espnow
espnow.init()
espnow.on_recv(receive_callback)

while True:
    pass

## test ###################
# msg = "{ 'game' : 1, 'data' : [ 'red', 'red', 'green', 'blue', 'green', 'red', 'blue', 'blue', 'red', 'green'] }"

# print("Received: ", msg)
# msg = eval(msg)
# if(msg['game'] == 1 ):
#     gameI(msg['data'])
# elif(msg['game'] == 2):
#     gameII(msg['data'])
###########################









