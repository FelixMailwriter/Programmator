# -*- coding:utf-8 -*-

import time
from Pin import Pin
from SensorListener import SensorListener
from PyQt4 import QtCore
from PyQt4.Qt import QObject


class Programmator(QObject):

    def __init__(self):
        QObject.__init__(self)
        pins = self._getPins()
        self.pinSwitcher = Pin (pins['Button'],'OUT')
        self.pinYellow = Pin(pins['Yellow'], 'IN')
        self.pinGreen = Pin(pins['Green'], 'IN')

        self.green_work=False
        self.yellow_work=False

        self.pinSwitcher.enable()

        self.init()


    def init(self):
        # проверка работоспособности сканнера
        print 'Prg init'
        trycount=0
        while (trycount < 10):
            self.pinSwitcher.disable()
            self.greenled_listener = SensorListener(self.pinGreen, self._set_green, 1)
            self.yellowled_listener = SensorListener(self.pinYellow, self._set_yellow, 1)
            self.greenled_listener.start()
            self.yellowled_listener.start()
            time.sleep(.5)
            print 'green = {}; yellow = {}'.format(self.green_work, self.yellow_work)
            if self.green_work and self.yellow_work:
                break
            else:
                trycount += 1
                self.pinSwitcher.enable()
                time.sleep(1)
        print 'Trycount = {}'.format(trycount)
        if trycount < 3:
            print 'Programmator OK'
        else:
            print 'Programmator failed'
        self.pinSwitcher.enable()
        self.green_work = False
        self.yellow_work = False


    def _readKey(self):
        trycount=0
        while trycount < 10 and self.pinGreen:
            self.pinSwitcher.disable()
            time.sleep(0.5)
            self.pinSwitcher.enable()
            trycount += 1
        if trycount >= 10 and self.pinGreen:
            print 'Prg is broken. restarting...' # restart prg

        self.greenled_listener = SensorListener(self.pinGreen, self._set_green, 1)
        self.yellowled_listener = SensorListener(self.pinYellow, self._set_yellow, 1)

    def _readKeyHandler(self, result):
        if result:
            print 'Read OK'
        else:
            print 'Read FAILED!'

    def _buttonClick(self, pin, holdtime=0.5):
        pin.disable()
        time.sleep(holdtime)
        pin.enable()


    def _getPins(self):
        pins={}
        pins['Button']=17
        pins['Yellow']=27
        pins['Green']=22
        return pins

    def _set_green(self, value):
        self.green_work = value

    def _set_yellow(self, value):
        self.yellow_work = value