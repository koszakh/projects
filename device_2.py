"""Импорт кода, содержащего алгоритм Дейкстры"""
# -*- coding: utf-8 -*-
import math
from math import sqrt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import Dijkstra_xyz
from Dijkstra_xyz import *

class Neighbor:
    """Класс объектов соседних устройств"""
    def __init__(self, neighborid, technology, bandwidth, distance):
        self.neighborid = neighborid
        self.technology = technology
        self.bandwidth = bandwidth
        self.distance = distance

class  Device:
    "Класс объектов устройств передачи данных"
    def __init__(self, deviceid, technology, maxcon, data_type, x, y, z):
        self.deviceid = deviceid
        self.technology = technology
        self.maxcon = maxcon # Максимальное количество подключенных устройств
        self.neighbors = {}
        self.data_type = data_type
        self.x = x
        self.y = y
        self.z = z

    def addneighbor(self, neighborid, technology, bandwidth, x, y, z):
        "Добавление соседнего устройства"
        if self.technology == technology:
            if len(self.neighbors) <= self.maxcon:  # Проверка на количество подключенных устройств
                distance = sqrt((self.x - x) ** 2 + (self.y - y) ** 2 + (self.z - z) ** 2)
                if (distance < 60 and technology == "Bluetooth") or \
                        (distance < 100 and technology == "WiFi"):
                    # Проверка на вхождение устройства с таким ID в список соседей
                    if not neighborid in self.neighbors:
                        self.neighbors[neighborid] = Neighbor(neighborid,
                                                              technology, bandwidth, distance)
                    else:
                        print("Устройство с id=", neighborid, " уже есть.", sep="")
                else:
                    print("Расстояние между подключаемыми девайсами должно быть не больше 60 м"
                          " для Bluetooth и 200 м для Wi-Fi устройств.")
            else:
                print("У устройства не может быть больше 7 соседей!")
        else:
            print("Устройства передают данные по разным протоколам передачи.")

    def weight_calc(self, neighborid):
        "Вычисление стоимости канала"
        data_type_value = {"text": 1, "audio": 2, "video": 3}
        if neighborid in self.neighbors.keys():
            weight = (100 * self.neighbors[neighborid].distance * data_type_value[self.data_type])\
                     / self.neighbors[neighborid].bandwidth
            return weight
        else:
            print("Соседнего устройства с таким ID нет.", sep="")

if __name__ == '__main__':
    DEV_LIST = []
    GATEWAY = Device(0, "WiFi", 7, "text", 7, 5, 5)
    GATEWAY.addneighbor(1, "WiFi", 1024, 1, 1, 1)
    GATEWAY.addneighbor(2, "WiFi", 512, 2, 5, 9)
    GATEWAY.addneighbor(3, "WiFi", 758, 4, 7, 11)
    DEV_LIST.append(GATEWAY)

    DEV_1 = Device(1, "WiFi", 7, "audio", 1, 1, 1)
    DEV_1.addneighbor(0, "WiFi", 1024, 7, 5, 5)
    DEV_1.addneighbor(2, "WiFi", 1024, 2, 5, 9)
    DEV_1.addneighbor(4, "WiFi", 758, 10, 3, 6)
    DEV_LIST.append(DEV_1)

    DEV_2 = Device(2, "WiFi", 7, "video", 2, 5, 9)
    DEV_2.addneighbor(3, "WiFi", 2048, 4, 7, 11)
    DEV_2.addneighbor(1, "WiFi", 1024, 1, 1, 1)
    DEV_2.addneighbor(0, "WiFi", 512, 7, 5, 5)
    DEV_LIST.append(DEV_2)

    DEV_3 = Device(3, "WiFi", 7, "text", 4, 7, 11)
    DEV_3.addneighbor(0, "WiFi", 758, 7, 5, 5)
    DEV_3.addneighbor(2, "WiFi", 2048, 2, 5, 9)
    DEV_3.addneighbor(4, "WiFi", 1024, 10, 3, 6)
    DEV_LIST.append(DEV_3)

    DEV_4 = Device(4, "WiFi", 7, "audio", 10, 3, 6)
    DEV_4.addneighbor(1, "WiFi", 758, 1, 1, 1)
    DEV_4.addneighbor(3, "WiFi", 1024, 4, 7, 11)
    DEV_LIST.append(DEV_4)
    dijkstra(DEV_LIST)

    u = np.linspace(0, 2 * np.pi, 50)
    v = np.linspace(0, np.pi, 50)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    for item in DEV_LIST:
        if item.technology == "WiFi":
            clr = "orange"
        else:
            clr = "blue"
        x1 = np.outer(np.cos(u), np.sin(v)) + item.x
        y1 = np.outer(np.sin(u), np.sin(v)) + item.y
        z1 = np.outer(np.ones(np.size(u)), np.cos(v)) + item.z
        ax.plot_surface(x1, y1, z1, color=clr)

    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')
    plt.show()
