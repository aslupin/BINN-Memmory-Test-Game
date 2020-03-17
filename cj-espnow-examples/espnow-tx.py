import network
from esp import espnow
import time

w = network.WLAN()
w.active(True)

BROADCAST = b'\xFF' * 6

espnow.init()
espnow.add_peer(BROADCAST)

count = 0
while True:
    count += 1
    msg = "Count = {}".format(count)
    print("Sending:", msg)
    espnow.send(BROADCAST, msg)
    time.sleep(1)
    