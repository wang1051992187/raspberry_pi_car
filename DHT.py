"""
    温湿度传感器获取数据
    参考网址:https://blog.csdn.net/qq_19961917/article/details/82888111
"""
import Adafruit_DHT
import time
sensor = Adafruit_DHT.DHT22
pin = 27 # 定义引脚为27


def get_DHT():
    hu, temp = Adafruit_DHT.read_retry(sensor, pin)
    return temp,hu