leds={}
leds_pins = {
    '1':{'blue':1 ,"green":2 ,'red':3},
    '2':{'blue':1 ,"green":2 ,'red':3},
    '3':{'blue':1 ,"green":2 ,'red':3}
    }
i = 0
for led, pins in leds_pins.items():
    leds[led] = {}
    for color, val in pins.items():
        leds[led][color] = i
        i += 1
print(leds)

leds['3'] = leds['2']
leds['2'] = leds['1']
leds['1'] = {'blue':99 ,"green":99 ,'red':99}
print(leds)
