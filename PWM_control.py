from tkinter import *
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor
from Adafruit_PWM_Servo_Driver import PWM
import time

# 直流电机设置
mh = Adafruit_MotorHAT(addr=0x60)
mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)
myMotor = mh.getMotor(4)

# 舵机设置
pwm = PWM(0x60, debug=False)


def setServoPulse(channel, pulse):
    pulseLength = 1000000.0  # 1,000,000 us per second
    pulseLength /= 50.0  # 60 Hz
    pulseLength /= 4096.0  # 12 bits of resolution
    pulse *= 1000.0
    pulse /= (pulseLength * 1.0)
    pwm.setPWM(channel, 0, int(pulse))


def write(servonum, x):
    y = x / 90.0 + 0.5
    y = max(y, 0.5)
    y = min(y, 2.5)
    setServoPulse(servonum, y)


pwm.setPWMFreq(50)
W1 = 150  # 前舵机转向角度
s = 0  # speed
maxs = 200  # max speed
write(0, W1)  # 前舵机
write(1, 90)  # 后舵机

# 调用Tkinter模块控制电机和舵机
root = Tk()


def callback(event):
    global W1
    global s
    global maxs
    if event.keysym == "w":
        print("前进:")
        if s < 0:
            for i in reversed(range(-s)):
                myMotor.setSpeed(i)
                time.sleep(0.005)
            s = 0
        myMotor.run(Adafruit_MotorHAT.FORWARD)
        for i in range(s, maxs):
            myMotor.setSpeed(i)
            time.sleep(0.005)
        s = maxs - 1
    elif event.keysym == "s":
        print("后退:")
        if s > 0:
            for i in reversed(range(s)):
                myMotor.setSpeed(i)
                time.sleep(0.005)
            s = 0
        myMotor.run(Adafruit_MotorHAT.BACKWARD)
        for i in reversed(range(-maxs + 1, s + 1)):
            myMotor.setSpeed(-i)
            time.sleep(0.005)
        s = -maxs + 1
    elif (event.keysym == "d"):
        print("右转")
        W1 += 2
        W1 = min(180, W1)
        write(0, W1)
    elif (event.keysym == "a"):
        print("左转")
        W1 -= 2
        W1 = max(120, W1)
        write(0, W1)
    elif (event.keysym == "q"):
        print("Stop!")
        for i in reversed(range(abs(maxs + 1))):
            myMotor.setSpeed(i)
            time.sleep(0.005)
        s = 0
        myMotor.run(Adafruit_MotorHAT.RELEASE)
    elif (event.keysym == "t"):
        print("陆地模式")
        write(1, 90)
    elif (event.keysym == "y"):
        print("水上模式")
        write(1, 180)
    elif event.keysym == "Up":
        maxs += 5
        maxs = min(maxs, 255)
        print("speed up:", maxs)
        if s:
            myMotor.setSpeed(maxs)
    elif event.keysym == "Down":
        maxs -= 5
        maxs = max(0, maxs)
        print("speed down:", maxs)
        if s:
            myMotor.setSpeed(maxs)
    else:
        print("请输入正确的控制按键:q,w,a,s,d,t,y")


frame = Frame(root, width=200, height=200)
frame.bind("<Key>", callback)
frame.focus_set()
frame.pack()

mainloop()

