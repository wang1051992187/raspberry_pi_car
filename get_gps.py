# """
# 获取GPS信号
# """
# import serial
# serial = serial.Serial('/dev/ttyS0', 115200)#≈ 打开/dev/ttyS0并设置波特率为115200, 只适用于Linux
# print(serial.portstr)# 能看到第一个串口的标识
#
#
#
#
# import serial
# import time
#
# ser = serial.Serial("/dev/ttyS0",115200,timeout=0.5)
# print(ser.portstr)
#
# time.sleep(3)
#
# ser.write("AT+CGPS=1\n".encode())
# time.sleep(0.5)
#
# for i in range(0,100):
#     if ser.inWaiting() >0:
#         data = ser.read()
#         print(data)
#
# time.sleep(3)
#
# ser.write("AT+CGPSINFO\n".encode())
# for i in range(0,100):
#     if ser.inWaiting() >0:
#         data = ser.read()
#         print(data)
#
# print(ser.read(50))
#
# time.sleep(3)
#
# ser.write("AT+CGPS=0\n".encode())
# time.sleep(0.5)
#
# for i in range(0,100):
#     if ser.inWaiting() >0:
#         data = ser.read()
#         print(data)
#
# ser.close
#
#
# import serial
# import time
#
# ser = serial.Serial("/dev/ttyS0",115200)
# print(ser.portstr)
#
# time.sleep(3)
#
# ser.write("AT+CSQ\r\n".encode())
# time.sleep(0.5)
# i = 0
# print('out:')
# for i in range(0,100):
#     if ser.inWaiting() >0:
#         data = ser.read()
#         print(data)
#
# ser.close

i = -1
def gpsinfo():
    global i
    data = [
        [121.553722, 31.294585],
        [121.553722, 31.294585],
        [121.553722, 31.294585],
        [121.553722, 31.294585],
        [121.553674, 31.294553],
        [121.553674, 31.294553],
        [121.55369, 31.294548],
        [121.55369, 31.294548],
        [121.553668, 31.294544],
        [121.553668, 31.294544],
        [121.553641, 31.294516],
        [121.553641, 31.294516],
        [121.55362, 31.294507],
        [121.55362, 31.294508],
        [121.553598, 31.294489],
        [121.553598, 31.294488],
        [121.553561, 31.294461],
        [121.553560, 31.294460],
        [121.553437, 31.294347],
        [121.553438, 31.294346],
        [121.553411, 31.294315],
        [121.553410, 31.294312],
        [121.553416, 31.294305],
        [121.553416, 31.294305],
        [121.553357, 31.29425],
        [121.553354, 31.29424],
        [121.553389, 31.294296]
    ]
    if i == 8:
        i -= 1
    else:
        i +=1
    print(data[i])
    return data[i]