from abc import ABC
import attr
import queue
from psychopy import logging, visual, core
import serial
import threading
import time
import typing as tp


from .TriggerHandler import NumberEncodedTriggerHandler


@attr.s(auto_attribs=True, kw_only=True)
class SerialTriggerHandler(NumberEncodedTriggerHandler):
    _port: str
    _baudRate: int = 9600
    _minPulseWidth: float = 0.05  # in sec

    _maxNumTriggers = 255

    _dev: serial.Serial = attr.ib(init=False)
    _resetAfterTime: tp.Optional[float] = attr.ib(init=False, default=None)

    def __attrs_post_init__(self):
        super().__attrs_post_init__()

        logging.exp(f'Connecting to serial port at {self._port}')
        self._dev = serial.Serial(self._port, self._baudRate, timeout=10.)
        assert self._dev.is_open

    def update(self):
        super().update()

        if self._resetAfterTime is not None:
            if core.getTime() > self._resetAfterTime:
                logging.exp(f'Zeroing trigger output')
                self._dev.write(0x00)
                self._resetAfterTime = None

    def _trigger(self, key: str):
        val = self._triggerMapping[key]
        self._dev.write(val)
        self._resetAfterTime = core.getTime() + self._minPulseWidth

    
