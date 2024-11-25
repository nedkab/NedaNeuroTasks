from abc import ABC
import attr
import queue
from psychopy import logging, visual, core
import threading
import time
import typing as tp
import socket

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'RTBox_py'))

from .TriggerHandler import BackgroundPulseTriggerHandler
from RTBox import RTBox


@attr.s(auto_attribs=True)
class RTBoxPulseTriggerHandler(BackgroundPulseTriggerHandler):

    _eventCode: int = 0b00000001  # set to 1 for first pin only; set to 255 for all pins
    
    _dev: tp.Optional[RTBox] = attr.ib(init=False, default=None)
    
    def __attrs_post_init__(self):
        super().__attrs_post_init__()

    def _runThread(self):

        print("logging.info('Initializing connection to RTBox')")
        assert self._dev is None
        try:
            self._dev = RTBox(
                host_clock=core.getTime,
                boxID=0
            )
        except EnvironmentError as e:
            print("logging.error('Problem with RTBox initialization')")
            raise e
        
        print("logging.info('Connected to RTBox')")

        self._dev.TTLResting(pol=[0, 0])  # set polarity to low resting

        self._dev.TTLWidth(width=float('Inf'))  # keep TTL level at specified value until changed by next TTL command

        # note: the above two settings are persistent; if other experiment scripts expect *different* persistent settings,
        #  they must change settings accordingly

        self._Dev.info()  # print some info about RTBox (note: just gets printed to stdout, not through logging)

        tSend, ub = self._dev.TTL(eventCode=0)
        print("logging.exp(f'Zeroed RTBox outputs (tSend: {tSend} ub: {ub})')")

        return super()._runThread()
    
    def _pulseOn(self, iPulse: int, numPulses: int):
        tSend, ub = self._dev.TTL(eventCode=self._eventCode)
        print("logging.exp(f'Pulse {iPulse+1}/{numPulses} on (tSend: {tSend} ub: {ub})')")

    def _pulseOff(self, iPulse: int, numPulses: int):
        tSend, ub = self._dev.TTL(eventCode=0)
        logging.exp(f'Pulse {iPulse+1}/{numPulses} off (tSend: {tSend} ub: {ub})')
    
