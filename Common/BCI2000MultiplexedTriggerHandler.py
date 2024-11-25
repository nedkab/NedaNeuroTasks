from abc import ABC
import attr
from psychopy import logging
import time
import typing as tp
import socket

from .TriggerHandler import NumberEncodedTriggerHandler


@attr.s(auto_attribs=True)
class BCI2000MultiplexedTriggerHandler(NumberEncodedTriggerHandler):
    _socket: socket.socket = attr.ib(init=False)
    _host: str = 'localhost'
    _port: int = 3999
    _bci2000EventName = 'PsychoPy'
    _maxNumTriggers: int = 255  # assuming BCI2000 event is configured as 8 bit width
    
    def __attrs_post_init__(self):
        super().__attrs_post_init__()
        
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.settimeout(1.)
        self._socket.connect((self._host, self._port))
        
        # run a dummy command to initiate connection, get past printed welcome message
        self._socket.sendall('help\n'.encode('ascii'))
        self._socket.recv(4096)  # welcome message
        time.sleep(0.1)
        self._socket.recv(4096)  # response to command
        
        # make sure that our event is configured already
        # (we can't easily configure ourselves since it must be declared before BCI2000 startup)
        resp = self._runCommand(f'exists event {self._bci2000EventName}')
        print(resp)
        assert resp == 'true', f'Event {self._bci2000EventName} must be declared before BCI2000 startup (probably in .bat file)'
        
    def _runCommand(self, cmd: str) -> str:
        """
        Run BCI2000 operator script action and get response.
        """
        logging.debug(f'Running BCI2000 command {cmd}')
        self._socket.sendall(f'{cmd}\n'.encode('ascii'))
        logging.debug('Waiting for response')
        resp = self._socket.recv(1024).decode().strip()
        # usually response includes a trailing '>' as a prompt for next command
        if resp.endswith('>'):
            resp = resp[:-1].strip()
        logging.debug(f'Response: {resp}')
        return resp
        
    def _trigger(self, key: str):
        number = self._triggerMapping[key]
        resp = self._runCommand(f'pulse event {self._bci2000EventName} {number}')
        assert len(resp) == 0, f'Problem pulsing BCI2000 event: {resp}'  # assume any non-empty response is an error message