from serial import Serial
import time

ser = Serial('COM4', 115200)
time.sleep(1)
rd = ser.readline()
print(rd)
print(type(rd))
