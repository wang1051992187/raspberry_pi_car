"""
获取GPS信号
"""
import serial
serial = serial.Serial('/dev/ttyS0', 115200)#≈ 打开/dev/ttyS0并设置波特率为115200, 只适用于Linux
print(serial.portstr)# 能看到第一个串口的标识




import serial
import time

ser = serial.Serial("/dev/ttyS0",115200,timeout=0.5)
print(ser.portstr)

time.sleep(3)

ser.write("AT+CGPS=1\n".encode())
time.sleep(0.5)

for i in range(0,100):
    if ser.inWaiting() >0:
        data = ser.read()
        print(data)

time.sleep(3)

ser.write("AT+CGPSINFO\n".encode())
for i in range(0,100):
    if ser.inWaiting() >0:
        data = ser.read()
        print(data)

print(ser.read(50))

time.sleep(3)

ser.write("AT+CGPS=0\n".encode())
time.sleep(0.5)

for i in range(0,100):
    if ser.inWaiting() >0:
        data = ser.read()
        print(data)

ser.close


import serial
import time

ser = serial.Serial("/dev/ttyS0",115200)
print(ser.portstr)

time.sleep(3)

ser.write("AT+CSQ\r\n".encode())
time.sleep(0.5)
i = 0
print('out:')
for i in range(0,100):
    if ser.inWaiting() >0:
        data = ser.read()
        print(data)

ser.close