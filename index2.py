#!/usr/bin/env python
# coding=utf-8

import os.path
import picamera
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import time
import io
import tornado
import tornado.websocket
import tornado.web
import socket
from threading import Thread
import asyncio
import random
from get_rasp_info import get_rasp_infos
from DHT import get_DHT
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor
from Adafruit_PWM_Servo_Driver import PWM
import time
from get_gps import gpsinfo

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

h_l = 85
h_r = 85

write(0, W1)  # 前舵机
write(1, h_r)  # 右后舵机
write(14,h_l)  # 左后舵机

WIDTH = 700
HEIGHT = 500
FPS = 90

html_url = "192.168.43.74:8000"
#html_url = "www.51zzb.top"
from tornado.options import define, options


define("port", default=8000, help="run on the given port", type=int)


class IndexHandler(tornado.web.RequestHandler):
    def initialize(self):
        pass
    def get(self):
        self.render('index.html',title="首页",url=html_url,active=0)

    def post(self):
        pass


class ControlHandler(tornado.web.RequestHandler):
    """
    实时控制
    增加实时温湿度信息
    实时经纬度在地图显示信息
    """
    def get(self):
        self.render('control.html',title="实时控制",url=html_url,active=1)

    def post(self):
        pass


class TocontrolHandler(tornado.web.RequestHandler):
    """
    实时控制
    """
    def get(self):
        global W1
        global h_l # 后轮左边舵机转向
        global h_r # 后轮右边舵机转向
        global s
        global maxs
        global type
        msg = ''
        way = self.get_argument('way', 'q')
        if way == 'w':
            msg = '已启动前进'
            if s<0:
                for i in reversed(range(-s)):
                    myMotor.setSpeed(i)
                    time.sleep(0.005)
                s=0
            myMotor.run(Adafruit_MotorHAT.FORWARD)
            for i in range(s,maxs):
                myMotor.setSpeed(i)
                time.sleep(0.005)
            s=maxs-1
        elif way == 's':
            msg = '已启动后退'
            if s>0:
                for i in reversed(range(s)):
                    myMotor.setSpeed(i)
                    time.sleep(0.005)
                s=0
            myMotor.run(Adafruit_MotorHAT.BACKWARD)
            for i in reversed(range(-maxs+1,s+1)):
                myMotor.setSpeed(-i)
                time.sleep(0.005)
            s=-maxs+1
        elif way == 'a':
            msg = '已启动左转'
            print("左转")
            W1-=2
            W1=max(120,W1)
            write(0, W1)
        elif way == 'd':
            msg = '已启动右转'
            print("右转")
            W1+=2
            W1=min(180,W1)
            write(0, W1)
        elif way == 'q':
            msg = '已启动停止'
            for i in reversed(range(abs(maxs+1))):
                myMotor.setSpeed(i)
                time.sleep(0.005)
            s=0
            myMotor.run(Adafruit_MotorHAT.RELEASE)
        elif way == 'u':
            msg = '已启动加速'
            maxs+=5
            maxs=min(maxs,255)
            print("speed up:",maxs)
            if s:
                myMotor.setSpeed(maxs)
        elif way == 'o':
            msg = '已启动减速'
            maxs-=5
            maxs=max(0,maxs)
            print("speed down:",maxs)
            if s:
                myMotor.setSpeed(maxs)
        elif way == 'e':
            msg = '已启动切换'
            if type == 1: # 陆地
                write(1, 90)  # 右后舵机
                write(14, 85)  # 左后舵机
                print("type:",type)
                type = 0
                print("type_change:",type)
            elif type == 0 :
                print("type2:",type)
                write(1, 180)  # 右后舵机
                write(14, 2)  # 左后舵机
                type = 1
                print("type2_change:",type)
            else:
                write(1, 180)  # 右后舵机
                write(14, 2)  # 左后舵机
                type = 1
                print("other_type:",type)
        elif way == 'bll':
            msg = "左后轮左转"
            h_l += 2
            h_l = min(180, h_l)
            write(14, h_l)
            print(h_l)

        elif way == 'blr':
            msg = "左后轮右转"
            h_l -= 2
            h_l = max(0, h_l)
            write(14, h_l)
            print(h_l)

        elif way == 'brl':
            msg = "右后轮左转"
            h_r += 2
            h_r = min(180, h_r)
            write(1, h_r)
            print(h_r)

        elif way == 'brr':
            msg = "右后轮右转"
            h_r -= 2
            h_r = max(0, h_r)
            write(1, h_r)
            print(h_r)

        data = {
            'msg': msg
        }
        self.write(data)

    def post(self):
        pass


class RaspberryinfoHandler(tornado.web.RequestHandler):
    """
    树莓派基本信息
    参考网址 http://shumeipai.nxez.com/2014/10/04/get-raspberry-the-current-status-and-data.html
    """
    def get(self):
        cpu_tem, cpu_use, RAM_use = get_rasp_infos()
        data = {
            'cpu': cpu_tem,
            'cpu_use': cpu_use,
            'ram': RAM_use
        }
        self.write(data)

    def post(self):
        pass

class GpsinfoHandler(tornado.web.RequestHandler):
    def get(self):
        gps = gpsinfo()
        data = {
            'jingdu':gps[0],
            'weidu':gps[1]
        }
        self.write(data)

    def post(self):
        pass

class HistoryHandler(tornado.web.RequestHandler):
    """
    历史数据
    建立SQLite数据库保存数据
    包含小车这次行走的数据(经纬度数据)
    小车行走得到的温湿度变化(温度数据)


    能够选择不同的记录
    每次小车行驶的经纬度信息
    每次记录的温湿度
    """
    def get(self):
        self.render('history.html',title="实时数据",url=html_url,active=2)

    def post(self):
        pass

class HumitureHandler(tornado.web.RequestHandler):
    """
    温湿度获取
    """
    def get(self):
        try :
            temperature,humidity = get_DHT() # 获取温湿度信息
        except :
            temperature = random.uniform(60.0,65.0)
            humidity = random.uniform(25.1,27.0)
        if temperature is None or humidity is None:
            temperature = random.uniform(60.0, 65.0)
            humidity = random.uniform(25.1, 27.0)
        data = {
            "temperature":temperature,
            "humidity":humidity
        }
        self.write(data)

    def post(self):
        pass

class SelfdriveHandler(tornado.web.RequestHandler):
    """
    自动驾驶

    根据选择不同的信息数据，来实现自动驾驶
    """
    def get(self):
        self.render('selfdrive.html',title="自动巡检",url=html_url,active=3)

    def post(self):
        pass

class WSHandler(tornado.websocket.WebSocketHandler):
    def initialize(self, camera):
        self.camera = camera
        self.state = True

    def open(self):
        print(self.request.remote_ip, ": connection opened")
        t = Thread(target=self.loop)  # 创建拍摄和发送线程
        t.setDaemon(True)
        t.start()

    def loop(self):
        new_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(new_loop)
        loop = asyncio.get_event_loop()
        stream = io.BytesIO()

        for foo in self.camera.capture_continuous(stream, "jpeg"):
            stream.seek(0)
            self.write_message(stream.read(), binary=True)
            stream.seek(0)
            stream.truncate()
            if not self.state:
                break

    def on_close(self):
        self.state = False  # 结束视频传输循环
        self.close()  # 关闭WebSocket会话
        print(self.request.remote_ip, ": connection closed")


def piCamera():
    camera = picamera.PiCamera()
    camera.resolution = (WIDTH, HEIGHT)
    camera.rotation = 90
    camera.framerate = FPS
    camera.start_preview()

    time.sleep(2)  # 相机初始化
    return camera


def getGPS():
    """
    实时获取GPS经纬度信息
    :return:
    """
    # import serial
    return [121.554156, 31.289672]

if __name__ == "__main__":
    # 获取GPS信息
    camera = piCamera()
    print("complete initialization")
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[(r'/', IndexHandler),
                  (r'/control', ControlHandler),
                  (r'/history', HistoryHandler),
                  (r'/selfdrive', SelfdriveHandler),
                  (r'/raspberryinfo', RaspberryinfoHandler),
                  (r'/tocontrol', TocontrolHandler),
                  (r'/humiture',HumitureHandler),
                  (r'/gpsinfo', GpsinfoHandler),
                  (r"/camera", WSHandler, dict(camera=camera)),
                  ],
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        debug=True
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()