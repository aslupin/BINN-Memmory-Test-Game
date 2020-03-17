import time
import network
from esp import espnow

w = network.WLAN()
w.active(True)
espnow.init()

def receive_callback(*dobj):
    mac, msg = dobj
    print("Received:", msg)
    print("From:", ":".join(["{:02X}".format(x) for x in mac]))

espnow.on_recv(receive_callback)

while True:
    pass
