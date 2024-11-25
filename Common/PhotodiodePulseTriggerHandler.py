from abc import ABC
import attr
from psychopy import logging, visual
import time
import typing as tp
import socket

from .TriggerHandler import PolledPulseTriggerHandler


@attr.s(auto_attribs=True)
class PhotodiodePulseTriggerHandler(PolledPulseTriggerHandler):
    _stimSize: tp.Tuple[float, float] = (0.07, 0.07) 
    _stimSizeUnits: str = 'height'

    _stim: visual.shape.ShapeStim = attr.ib(init=False)

    def __attrs_post_init__(self):
        super().__attrs_post_init__()

        if self._win is None:
            raise ValueError('Must specify win for PhotodiodePulseTriggerHandler')
        
        winSize = self._win.size
        if self._stimSizeUnits == 'pix':
            stimPos = tuple(winSize[i]/2 - self._stimSize[i]/2 for i in range(2))    
        elif self._stimSizeUnits == 'height':
            stimPos = tuple(winSize[i]/2 / winSize[1] - self._stimSize[i]/2 for i in range(2))
        else:
            raise NotImplementedError

        stimPos = tuple(stimPos[i] * (1, -1)[i] for i in range(2))

        self._stim = visual.rect.Rect(win=self._win,
                                      size=self._stimSize,
                                      pos=stimPos,
                                      units=self._stimSizeUnits,
                                      fillColor='black',
                                      name='PhotodiodePulseStimulus',
                                      autoDraw=True)

    def trigger(self, key: str, doDelayUntilWinFlip: bool = False):
        # Since we're triggering with visual stimuli, the trigger will always be synchronized with the win flip.
        # Also, want to be sure to submit this change before the next flip() call to have time to draw the changes.
        assert key in self._triggerKeys
        # keep log messages consistent with parent class, even though
        # visual stimulus trigger won't update until next flip
        if doDelayUntilWinFlip:
            logging.exp(f'Queueing trigger for next win flip: {key}')
            self._win.callOnFlip(lambda key=key: logging.exp(f'Recording trigger: {key}'))
        else:
            logging.exp(f'Recording trigger: {key}')  
        self._trigger(key=key)

    def _pulseOn(self, iPulse: int, numPulses: int):
        self._stim.fillColor = 'white'
        logging.exp(f'Pulse {iPulse+1}/{numPulses} on')

    def _pulseOff(self, iPulse: int, numPulses: int):
        self._stim.fillColor = 'black'
        logging.exp(f'Pulse {iPulse+1}/{numPulses} off')