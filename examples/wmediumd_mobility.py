#!/usr/bin/python

"""
Setting the position of Nodes (only for Stations and Access Points)
and providing mobility using mobility models with wmediumd enabled."""

from mininet.node import Controller
from mininet.log import setLogLevel, info
from mn_wifi.link import wmediumd
from mn_wifi.cli import CLI_wifi
from mn_wifi.net import Mininet_wifi


def topology():

    "Create a network."
    net = Mininet_wifi(controller=Controller, link=wmediumd)

    info("*** Creating nodes\n")
    ap1 = net.addAccessPoint('ap1', ssid='new-ssid', mode='a', channel='36',
                             position='150,150,0')
    net.addStation('sta1', mac='00:00:00:00:00:02', ip='10.0.0.2/8')
    net.addStation('sta2', mac='00:00:00:00:00:03', ip='10.0.0.3/8')
    c1 = net.addController('c1')

    info("*** Configuring Propagation Model\n")
    net.setPropagationModel(model="logDistance", exp=3)  #传播模型

    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()

    net.plotGraph(max_x=300, max_y=300)    #画图最大范围

    net.setMobilityModel(time=0, model='RandomDirection', max_x=300, max_y=300,
                         min_v=0.5, max_v=0.8, seed=20)  #设计随机移动模型，最小速度和最大速度一样

    info("*** Starting network\n")
    net.build()   #拓扑建立
    c1.start()    #控制器开始
    ap1.start([c1])   #ap连接控制器

    info("*** Running CLI\n")
    CLI_wifi(net)

    info("*** Stopping network\n")
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    topology()
