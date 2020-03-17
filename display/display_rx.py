machine = 'display-node'
import time
import network
from esp import espnow
from machine import Pin
led_buuild_in = Pin(2, Pin.OUT)

def starter():
    print("Start: " + machine)
    led_buuild_in.value(1) # turn LED on
    time.sleep(1)
    led_buuild_in.value(0) # turn LED off
    time.sleep(1)

def receive_callback(*dobj):
    global leds
    msg = dobj
    print("Received:", msg)
    #msg = {color: 'green', value: 1}
    #
    #for val in msg:
    #    leds[val.color].value(val.value)
    #    time.sleep(5)
    
    #print("From:", ":".join(["{:02X}".format(x) for x in msg]))
    
#starter  
starter()

# config network
w = network.WLAN()
w.active(True)

#config LEDs
leds = {}
led_pins = {'1':4 ,'2':16 ,'3':17 ,'4':18 ,'5':19 ,'6':13}
for key, val in led_pins.items():
    leds[key] = Pin(val, Pin.OUT)

#print(led_pins)
    #time.sleep(1)
# config espnow
espnow.init()
espnow.on_recv(receive_callback)

while True:
    pass









