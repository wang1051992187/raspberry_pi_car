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

WIDTH = 700
HEIGHT = 500
FPS = 100

from tornado.options import define, options

define("port", default=8000, help="run on the given port", type=int)


class IndexHandler(tornado.web.RequestHandler):
    def initialize(self):
        pass
    def get(self):
        self.render('index.html',title="首页")

    def post(self):
        pass

class ControlHandler(tornado.web.RequestHandler):
    """
    实时控制
    """
    def get(self):
        self.render('control.html',title="实时控制")

    def post(self):
        pass

class HistoryHandler(tornado.web.RequestHandler):
    """
    历史数据
    """
    def get(self):
        self.render('history.html',title="历史数据")

    def post(self):
        pass

class SelfdriveHandler(tornado.web.RequestHandler):
    """
    自动驾驶
    """
    def get(self):
        self.render('selfdrive.html',title="自动驾驶")

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


if __name__ == "__main__":
    #camera = piCamera()
    print("complete initialization")
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[(r'/', IndexHandler),
                  (r'/control', ControlHandler),
                  (r'/history', HistoryHandler),
                  (r'/selfdrive', SelfdriveHandler),
                  #(r"/camera", WSHandler, dict(camera=camera)),
                  ],
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        debug=True
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()