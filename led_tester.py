import time
from esp import espnow
from machine import Pin
import time

from micropython import const
from machine import Pin, Timer

# BUTTON_A_PIN = const(16)
# # BUTTON_B_PIN = const(33)

# class Button:
#     """
#     Debounced pin handler
#     usage e.g.:
#     def button_callback(pin):
#         print("Button (%s) changed to: %r" % (pin, pin.value()))
#     button_handler = Button(pin=Pin(32, mode=Pin.IN, pull=Pin.PULL_UP), callback=button_callback)
#     """

#     def __init__(self, pin, callback, trigger=Pin.IRQ_FALLING, min_ago=300):
#         self.callback = callback
#         self.min_ago = min_ago

#         self._blocked = False
#         self._next_call = time.ticks_ms() + self.min_ago

#         pin.irq(trigger=trigger, handler=self.debounce_handler)

#     def call_callback(self, pin):
#         self.callback(pin)

#     def debounce_handler(self, pin):
#         if time.ticks_ms() > self._next_call:
#             self._next_call = time.ticks_ms() + self.min_ago
#             self.call_callback(pin)
#         #else:
#         #    print("debounce: %s" % (self._next_call - time.ticks_ms()))
        
        
# def button_a_callback(pin):
#     print("Button A (%s) changed to: %r" % (pin, pin.value()))


# def button_b_callback(pin):
#     print("Button B (%s) changed to: %r" % (pin, pin.value()))

# while True:
#     button_a = Button(pin=Pin(BUTTON_A_PIN, mode=Pin.IN, pull=Pin.PULL_UP), callback=button_a_callback)
#     time.sleep(1)
    
# button_b = Button(pin=Pin(BUTTON_B_PIN, mode=Pin.IN, pull=Pin.PULL_UP), callback=button_b_callback)
# #from pyb import Pin


# sw1 = Pin(5, Pin.IN)
# sw2 = Pin(16, Pin.IN)

#led_tester = Pin(pin, Pin.OUT)
#led_tester1 = Pin(22, Pin.OUT)

#print('start ' + str(pin))


ledbuild = Pin(2, Pin.OUT)

#sw3 = Pin(17, Pin.IN )

while True:
    ledbuild.value(1)
    time.sleep(1)
    




