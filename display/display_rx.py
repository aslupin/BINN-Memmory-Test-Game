machine = 'display-node'
import ubinascii
import time
import network
from esp import espnow
from machine import Pin

lb = Pin(2, Pin.OUT)

def starter():
    global led_buuild_in
    print("Start: " + machine)
    lb.value(1) # turn LED on
    time.sleep(1)
    lb.value(0) # turn LED off
    time.sleep(1)

def gameI(game):
    global leds
    time.sleep(1)
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


def receive_callback(*dobj):
    msg = dobj[0][1].decode("utf-8")
    
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

UNICAST_CONTROLLER = b'\x30\xae\xa4\x12\x1f\x28'
espnow.init()
espnow.add_peer(UNICAST_CONTROLLER)


#config LEDs
leds = {}
led_pins = {'1':15 ,'2':16 ,'3':17 ,'4':5 ,'5':18 ,'6':19}
for key, val in led_pins.items():
    leds[key] = Pin(val, Pin.OUT)

for k, v in leds.items():
#     print(v)
    v.value(1)


def recieveFromController(*dobj):
    global connect
    msg = dobj[0][1].decode("utf-8")
    mac = ''.join(["{:02X}".format(x) for x in dobj[0][0]])
    controller_mac = ''.join(["{:02X}".format(x) for x in UNICAST_CONTROLLER])
    print(mac,msg)
    time.sleep(0.2)
    if (mac == controller_mac and msg == 'connecting'):
        connect = True


connect = False
start = False

espnow.on_recv(recieveFromController)
while (not connect):
    print('wait for connection')
    time.sleep(1)
    lb.on()
    time.sleep(1)
    lb.off()
print('connected')
espnow.send(UNICAST_CONTROLLER, 'connected')
connect = True
lb.on()  # connect

# print(leds, leds['1'], type(leds['1']))

#config espnow
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









