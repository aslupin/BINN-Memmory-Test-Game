import time
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
i2c = I2C(scl=Pin(22),sda=Pin(21),freq=100000)
# oled = SSD1306_I2C(128,64,i2c)
# oled.fill(0)
# oled.text("ESP32 started...",0,0)
# oled.show()
print("Scanning I2C bus... found",i2c.scan())
time.sleep(0.5)
print("Send data to STM32...")
#i2c.writeto(0xA0, b'Hello from ESP32')
print("dfs")
while True:
    time.sleep(0.5)
    print("Receive data from STM32:", i2c.readfrom(0x50,3))