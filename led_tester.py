import time
from esp import espnow
from machine import Pin

led_tester = Pin(21, Pin.OUT)
led_tester1 = Pin(22, Pin.OUT)

while True:
    led_tester.value(0)
    led_tester1.value(0)
    time.sleep(3)
    









