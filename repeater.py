"""Определение координат повторителя"""
# -*- coding: utf-8 -*-
import random
import math
from math import sqrt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np

class Point():
    """ Класс, объекты которого являются точками в 3-мерном пространстве """
    in_range = False
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    def In_range(self):
        self.in_range = True

    def Out_of_range(self):
        self.in_range = False

def clustering(dev_mas, clust_num, iter_num):
    """ Алгоритм нахождения координат повторителя """
    iterations = 0 # Число итераций
    k = 0
    flag = False # Условие окончания цикла
    Sum = {} # Сумма квадратов расстояний от устройства до повторителя
    Sumx = {} # Сумма квадратов значений координат x устройств
    Sumy = {} # Сумма квадратов значений координат y устройств
    Sumz = {} # Сумма квадратов значений координат z устройств
    dev_count = {} # Массив, содержащий количество устройств, подключенных к повторителям
    dist = {} # Массив расстояний между устройством и повторителем
    rep_mas = {} # Массив координат повторителей

    for i in range(clust_num):
        rep_mas[i] = Point(random.randint(0, 50), random.randint(0, 50), random.randint(0, 50))

    while flag is False:
        iterations = iterations + 1
        full_sum = 0

        for i in range(len(dev_mas)):
            dist[i] = 10000
            dev_mas[i].Out_of_range()

        for i in range(clust_num):
            Sum[i] = 0
            Sumx[i] = 0
            Sumy[i] = 0
            Sumz[i] = 0
            dev_count[i] = 0

        for j in range(len(dev_mas)):
            for i in range(len(rep_mas)):
                if sqrt((rep_mas[i].x - dev_mas[j].x) ** 2 + (rep_mas[i].x - dev_mas[j].x) ** 2 +
                        (rep_mas[i].x - dev_mas[j].x) ** 2) < dist[j]:
                    dist[j] = sqrt((rep_mas[i].x - dev_mas[j].x) ** 2 +
                                   (rep_mas[i].x - dev_mas[j].x) ** 2 +
                                   (rep_mas[i].x - dev_mas[j].x) ** 2)
                    k = i
            Sum[k] = Sum[k] + (rep_mas[k].x - dev_mas[j].x) ** 2 + \
                     (rep_mas[k].x - dev_mas[j].x) ** 2 + (rep_mas[k].x - dev_mas[j].x) ** 2
            Sumx[k] = Sumx[k] + dev_mas[j].x ** 2
            Sumy[k] = Sumy[k] + dev_mas[j].y ** 2
            Sumz[k] = Sumz[k] + dev_mas[j].z ** 2

            if sqrt((rep_mas[i].x - dev_mas[j].x) ** 2 + (rep_mas[i].x - dev_mas[j].x) ** 2 +
                    (rep_mas[i].x - dev_mas[j].x) ** 2) < 50:
                dev_mas[j].In_range()

        for i in range(clust_num):
            full_sum = full_sum + Sum[i]

        for i in range(len(dist)):
            print("dist[", i, "] = ", dist[i], sep="")

        print("full_sum = ", full_sum, sep="")
        all_in_range = True

        for i in range(len(dev_mas)):
            if dev_mas[i].in_range == False:
                all_in_range = False
                break

        if all_in_range is True:
            print("Связь со всеми устройствами установлена после ", iterations, " итераций(-и)", sep="")
            flag = True
        elif iterations == iter_num:
            print("Превышено число итераций. Для установления связи необходимо больше повторителей")
            flag = True
        else:
            print("Не со всеми устройствами установлена связь")
            for i in range(clust_num):
                rep_mas[i].x = sqrt(Sumx[i]) * random.randint(0, 1)
                rep_mas[i].y = sqrt(Sumy[i]) * random.randint(0, 1)
                rep_mas[i].z = sqrt(Sumz[i]) * random.randint(0, 1)

    u = np.linspace(0, 2 * np.pi, 50)
    v = np.linspace(0, np.pi, 50)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    for i in range(len(dev_mas)):
        if dev_mas[i].technology == "WiFi":
            clr = "orange"
        else:
            clr = "blue"
        x1 = 5 * np.outer(np.cos(u), np.sin(v)) + dev_mas[i].x
        y1 = 5 * np.outer(np.sin(u), np.sin(v)) + dev_mas[i].y
        z1 = 5 * np.outer(np.ones(np.size(u)), np.cos(v)) + dev_mas[i].z
        ax.plot_surface(x1, y1, z1, color=clr)

    for j in range(len(rep_mas)):
        x2 = 5 * np.outer(np.cos(u), np.sin(v)) + rep_mas[j].x
        y2 = 5 * np.outer(np.sin(u), np.sin(v)) + rep_mas[j].y
        z2 = 5 * np.outer(np.ones(np.size(u)), np.cos(v)) + rep_mas[j].z
        ax.plot_surface(x2, y2, z2, color='g')

    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')
    plt.show()


