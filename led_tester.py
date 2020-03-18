import time
from esp import espnow
from machine import Pin
pin = 32
led_tester = Pin(pin, Pin.OUT)
#led_tester1 = Pin(22, Pin.OUT)

print('start ' + str(pin))
while True:
    led_tester.value(0)
    time.sleep(3)






