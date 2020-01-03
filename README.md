### 基于树莓派的4G远程控制水陆两栖多功能巡检车
    硬件：
         1.树莓派3B
         2.微雪SIM_7000C
         3.电机驱动板


    应用框架及相关技术：
         1.python tornado框架
         2.picamera

**Tornado架构详细设计**

    本系统在Tonado架构之上根据不同的设计需要对整个项目进行如下类模块设计：

序号 | 名称 |  类名 
:-:|:-:|:-:
1 | 首页界面类 | IndexHandler 
2 | 实时控制界面类 | ControlHandler 
3 | 实时控制类 | TocontrolHandler 
4 | 树莓派基本信息类 | RaspberryinfoHandler 
5 | 实时数据界面类 | HistoryHandler 
6 | 温湿度类 | HumitureHandler 
7 | 自主巡检界面类 | SelfdriveHandler 
8 | 实时视频类 | WSHandler 
9 | GPS数据信息类 | GetGPS 

在系统界面方面，本系统分别有实时控制界面、实时数据界面和自主巡检界面，具体情况如表所示：

| 序号 |     名称     |      类名      |
| :--: | :----------: | :------------: |
|  1   | 实时控制界面 |  control.html  |
|  2   | 实时数据界面 |  history.html  |
|  3   | 自主巡检界面 | selfdrive.html |

**实时图像传输设计**
    
    本实时图像传输技术采用websocket技术，以Tornado的websocket为基础，实现游览器和服务器的双向通讯。树莓派服务器通过创建拍摄和发送线程，将每帧数据通过websocket形式发送给游览器端。

![Image text](https://raw.githubusercontent.com/wang1051992187/raspberry_pi_car/master/imgs/image072.png)

**运行截图**


实时控制界面

![实时控制](<https://raw.githubusercontent.com/wang1051992187/raspberry_pi_car/master/imgs/image077.png>)

温湿度

![温度](<https://raw.githubusercontent.com/wang1051992187/raspberry_pi_car/master/imgs/image081.png>)



运行轨迹

![运行轨迹](<https://raw.githubusercontent.com/wang1051992187/raspberry_pi_car/master/imgs/image085.png>)

自动巡检

![](<https://raw.githubusercontent.com/wang1051992187/raspberry_pi_car/master/imgs/image087.png>)
