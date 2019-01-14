# -*- coding:utf-8 -*-
from PyQt4 import QtCore


class SensorListener(QtCore.QThread):

    def __init__(self, sensorPin, callback, qty_of_shoot, delayStart=0, listenDuration=10000, listenFreq=5):
        QtCore.QThread.__init__(self)
        self.sensorPin = sensorPin  # прослушиваемый Pin
        self.delayStart = delayStart  # задержка перед запуском прослушивания
        self.listenDuration = listenDuration  # Продолжительность прослушивания
        self.ListenFreq = listenFreq  # Частота опроса
        self.callback = callback # функция обратного вызова
        self.qty_of_shoot = qty_of_shoot # количество срабатываний

    def run(self):
        print "Слушам датчик %s" % (self.sensorPin)
        threshold = 0
        total_shoot = 0
        self.msleep(self.delayStart)
        while threshold < self.listenDuration:
            if self.sensorPin.getSignal():
                total_shoot += 1
                if total_shoot >= self.qty_of_shoot:
                    print 'Срабатывание датчика %s. Выход из потока прослушивания' % (self.sensorPin)

                    self.callback(True)
                    return
            else:
                threshold = threshold + self.ListenFreq
                self.msleep(self.ListenFreq)
        print 'TimeOut датчика прослушивания %s. Выход из потока' % (threshold)
        self.callback(False)