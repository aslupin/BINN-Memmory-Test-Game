import time
import network
from esp import espnow
from machine import Pin

# config network
w = network.WLAN()
w.active(True)
print('my mac addr:', w.config('mac'))

# config esp32
UNICAST_CONTROLLER = b'\xFF' * 6
espnow.init()
espnow.add_peer(UNICAST_CONTROLLER)

def sendToController(pin):
    msg = {}
    msg['player'] = 1 # number of player
    msg['action'] = {}
    msg['action']['color'] = pin
    msg['action']['value'] = 1 # True , False
    espnow.send(UNICAST_CONTROLLER, str(msg)) 

    # {
    #     'player' : 1 
    #     'action' : {
    #        'color' : 'red'
    #        'value': 1
    #       }
    # }

# config switchs
switchs = {}
switch_pins = {'blue':1 ,"green":2 ,'red':3}

for key, val in switch_pins.items():
    switchs[key] = Pin(val, Pin.IN)



while True:
    if(switchs['blue'].value()):
        sendToController('blue')
    elif(switchs['green'].value()):
        sendToController('green')
    elif(switchs['red'].value()):
        sendToController('red')
    
    