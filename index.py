#!/usr/bin/env python
# coding=utf-8

import os.path
#import picamera
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
#from DHT import get_DHT


WIDTH = 700
HEIGHT = 500
FPS = 15

html_url = "127.0.0.1:8000"
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
        msg = ''
        way = self.get_argument('way', 'q')
        if way == 'w':
            msg = '已启动前进'
        elif way == 's':
            msg = '已启动后退'
        elif way == 'a':
            msg = '已启动左转'
        elif way == 'd':
            msg = '已启动右转'
        elif way == 'q':
            msg = '已启动停止'
        elif way == 'u':
            msg = '已启动加速'
        elif way == 'o':
            msg = '已启动减速'
        elif way == 'e':
            msg = '已启动切换'
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


class HistoryHandler(tornado.web.RequestHandler):
    """
    历史数据
    建立SQLite数据库保存数据
    包含小车这次行走的数据(经纬度数据)
    小车行走得到的温湿度变化(温度数据)
    """
    def get(self):
        self.render('history.html',title="历史数据",url=html_url,active=2)

    def post(self):
        pass

class HumitureHandler(tornado.web.RequestHandler):
    """
    温湿度获取
    """
    def get(self):
        #temperature,humidity = get_DHT() # 获取温湿度信息
        temperature = random.uniform(30.0,40.0)
        humidity = random.uniform(23.1,50.0)
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
    """
    def get(self):
        self.render('selfdrive.html',title="自动驾驶",url=html_url,active=3)

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

"""
def piCamera():
    camera = picamera.PiCamera()
    camera.resolution = (WIDTH, HEIGHT)
    camera.framerate = FPS
    camera.start_preview()

    time.sleep(2)  # 相机初始化
    return camera
"""

def getGPS():
    """
    实时获取GPS经纬度信息
    :return:
    """
    # import serial
    return [121.554156, 31.289672]

if __name__ == "__main__":
    # 获取GPS信息
    #camera = piCamera()
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
                  #(r"/camera", WSHandler, dict(camera=camera)),
                  ],
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        debug=True
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()