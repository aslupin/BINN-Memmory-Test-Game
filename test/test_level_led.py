import machine
import time
import math

leds_pins = {
    '1': {'blue': 27, "green": 15, 'red': 14},
    '2': {'blue': 33, "green": 26, 'red': 25},
    '3': {'blue': 19, "green": 32, 'red': 18}
}


led = machine.PWM(machine.Pin(27), freq=1024)
led.duty(512)
time.sleep(1)
led = machine.Pin(27)
led.value(1)
time.sleep(1)
led.value(0)

# def pulse(l, t):
#     for i in range(20):
#         l.duty(int(math.sin(i / 10 * math.pi) * 500 + 500))
#         time.sleep_ms(t)

# for i in range(10):
#     pulse(led, 20)
