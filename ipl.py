import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
ir = 17

GPIO.setup(ir,GPIO.IN)
try:
 while True:
    if GPIO.input(ir) == 0:
        print("obstacle detected ")

    else:
        print("not detected")
except KeyboardInterrupt:
   print("program stopped")
finally:
 GPIO.cleanup()



 # ultasonic sensor 

import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

trig = 22
echo = 23

GPIO.setup(trig,GPIO.OUTPUT)
GPIO.setup(echo,GPIO.INPUT)

try:
   while True:
      GPIO.output(trig,False)
      time.sleep(0.01)
      GPIO.output(trig,True)
      time.sleep(0.00001)
      GPIO.output(trig,False)

      while GPIO.input(echo) == 0:
        start = time.time()
      while GPIO.input(echo) == 1:
         end = time.time()

      dist = (end - start) * 17150
      if dist<20:
       print("Obstacle detected")
      else:
       print("No obstacle")

      time.sleep(0.5)

except KeyboardInterrupt:
    print("Stopped")

finally:
    GPIO.cleanup()



import serial
import pynmea2

# Open serial port (for GPS module)
port = serial.Serial("/dev/serial0", baudrate=9600, timeout=1)

while True:
    try:
        data = port.readline().decode('utf-8', errors='ignore')
        if data.startswith('$GPGGA'):
            msg = pynmea2.parse(data)
            print(f"Latitude: {msg.latitude}, Longitude: {msg.longitude}")
    except pynmea2.ParseError:
        continue


from grove.display.jhd1802 import JHD1802
import RPi.GPIO as GPIO
import time


# Initialize LCD and IR sensor
lcd = JHD1802()
ir_pin = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(ir_pin, GPIO.IN)

lcd.setCursor(0, 0)
lcd.write("Welcome")

try:
    while True:
        if GPIO.input(ir_pin) == 0:
            lcd.setCursor(1, 0)
            lcd.write("Object detected  ")  # 16 chars max; extra spaces clear previous text
        else:
            lcd.setCursor(1, 0)
            lcd.write("Not detected     ")
        time.sleep(1)

except KeyboardInterrupt:
    pass

finally:
    lcd.clear()
    GPIO.cleanup()


import RPi.GPIO as GPIO
import time

import setmode(GPIO.BCM)
led = [17,27,22,5]

for pin in led:
   GPIO.setup(pin,GPIO.OUT)
try:
   while True:
      GPIO.output(17, GPIO.HIGH)
      GPIO.output(27, GPIO.HIGH)
      GPIO.output(22, GPIO.LOW)
      GPIO.output(5, GPIO.LOW)
      time.sleep(0.5) 
       

      GPIO.output(17, GPIO.HIGH)
      GPIO.output(27, GPIO.HIGH)
      GPIO.output(22, GPIO.LOW)
      GPIO.output(5, GPIO.LOW)
      time.sleep(0.5)
finally:
   GPIO.cleanup()
