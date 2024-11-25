from abc import ABC
import attr
from psychopy import logging, visual
import threading
import queue
import time
import typing as tp
import socket


@attr.s(auto_attribs=True)
class TriggerHandler(ABC):
    _triggerKeys: tp.List[str] = attr.ib(init=False, factory=list)

    _win: tp.Optional[visual.Window] = None
    
    def __attrs_post_init__(self):
        pass
    
    def register(self, key: str, **kwargs):
        logging.exp(f'Registering trigger: {key}')
        assert key not in self._triggerKeys
        self._register(key=key, **kwargs)
        
    def _register(self, key: str, **kwargs):
        raise NotImplementedError  # should be implemented by subclass
        
    def trigger(self, key: str, doDelayUntilWinFlip: bool = False):
        assert key in self._triggerKeys
        if doDelayUntilWinFlip:
            assert self._win is not None, 'Need to specify `win` when constructing TriggerHandler to support delay until flip'
            logging.exp(f'Queueing trigger for next win flip: {key}')
            self._win.callOnFlip(self.trigger, key=key, doDelayUntilWinFlip=False)
        else:
            logging.exp(f'Recording trigger: {key}')
            self._trigger(key=key)

    def update(self):
        pass  # only implemented by polling-type trigger handlers, but should be able to called without 
        # effect for any others
        
    def _trigger(self, key: str):
        raise NotImplementedError  # should be implemented by subclass
    
    
@attr.s(auto_attribs=True)
class NumberEncodedTriggerHandler(TriggerHandler, ABC):
    _triggerMapping: tp.Dict[str, int] = attr.ib(init=False, factory=dict)
    _maxNumTriggers: tp.Optional[int] = None
    
    def __attrs_post_init__(self):
        super().__attrs_post_init__()
        
    def _register(self, key: str, **kwargs):
        assert key not in self._triggerMapping
        if self._maxNumTriggers is not None:
            assert len(self._triggerMapping) < self._maxNumTriggers
        self._triggerMapping[key] = len(self._triggerMapping) + 1
        self._triggerKeys.append(key)
        
    
@attr.s(auto_attribs=True)
class LogTriggerHandler(TriggerHandler):
    def _register(self, key: str, **kwargs):
        self._triggerKeys.append(key)
        
    def _trigger(self, key: str):
        pass  # already logged by superclass


@attr.s(auto_attribs=True)
class TimeMultiplexedSingleChannelTriggerHandler(TriggerHandler):
    _pulseOnTime: float = 0.1  # in sec
    _pulseOffTime: float = 0.1  # in sec
    _numPulsesPerTrigger: tp.Dict[str, int] = attr.ib(init=False, factory=dict)
    _queue: queue.Queue = attr.ib(init=False, factory=lambda: queue.Queue(maxsize=1))
    _triggerInProgress: threading.Condition = attr.ib(init=False, factory=lambda: threading.Condition(threading.Lock()))

    def __attrs_post_init__(self):
        super().__attrs_post_init__()

    def _register(self, key: str, numPulses: int):
        assert key not in self._numPulsesPerTrigger
        self._triggerKeys.append(key)
        self._numPulsesPerTrigger[key] = numPulses  # note: no check for uniqueness of numPulses, since we may sometimes want to allow for redundant coding 
        logging.exp(f'Registering numPulsesPerTrigger: {numPulses} for {key}')

    def _trigger(self, key: str):

        numPulses = self._numPulsesPerTrigger[key]
        if numPulses == 0:
            # skip generating any pulses for this trigger
            return

        logging.exp(f'Getting ready to queue trigger {key}')

        didAcquire = self._triggerInProgress.acquire(False)
        if not didAcquire:
            errMsg = 'Previous trigger in progress, cannot start new trigger'
            logging.error(errMsg)
            raise RuntimeError(errMsg)
        
        try:
            self._queue.put_nowait(numPulses)
        except queue.Full:
            errMsg = 'Previous trigger has not started yet, cannot start new trigger'
            logging.error(errMsg)
            raise RuntimeError(errMsg)
        else:
            self._triggerInProgress.notify()
        finally:
            self._triggerInProgress.release()

    # note: subclasses must implement mechanism (either via polling or background process/thread to empty trigger queue)


@attr.s(auto_attribs=True)
class BackgroundPulseTriggerHandler(TimeMultiplexedSingleChannelTriggerHandler):
    _waitForReadyTimeout: float = 10.  # in sec, how long to wait for thread to start and send ready

    _threadQueue: queue.Queue = attr.ib(init=False, factory=lambda: queue.Queue(1))  # used to communicate back to main thread when worker thread is ready
    _triggerInProgress: threading.Condition = attr.ib(init=False, factory=lambda: threading.Condition(threading.Lock()))
    _thread: threading.Thread = attr.ib(init=False)

    def __attrs_post_init__(self):
        super().__attrs_post_init__()
    
        logging.debug('starting thread')

        self._thread = threading.Thread(target=self.__runThread, daemon=True)
        self._thread.start()

        logging.debug('Waiting for thread to init')
        try:
            evt = self._threadQueue.get(timeout=self._waitForReadyTimeout)  # wait for thread to be ready
        except queue.Empty:
            raise RuntimeError('Thread timed out on init')
        
        if evt == 'exception':
            raise RuntimeError('Thread raised an exception in init')
        elif evt == 'ready':
            pass
        else:
            raise NotImplementedError

    def __runThread(self):
        try:
            self._runThread()
        except Exception as e:
            self._threadQueue.put('exception')
            raise e

    def _runThread(self):
        logging.exp('Start of thread')
        self._threadQueue.put('ready')
        while True:
            logging.debug('Waiting for trigger')  # TODO: change to debug log level
            with self._triggerInProgress:
                self._triggerInProgress.wait()
                numPulses = self._queue.get()
                logging.exp(f'Triggering numPulses={numPulses}')  # TODO: change to debug log level
                for iPulse in range(numPulses):
                    self._pulseOn(iPulse=iPulse, numPulses=numPulses)
                    time.sleep(self._pulseOnTime)
                    self._pulseOff(iPulse=iPulse, numPulses=numPulses)
                    time.sleep(self._pulseOffTime)

    def _pulseOn(self, iPulse: int, numPulses: int):
        raise NotImplementedError  # to be implemented by subclass
    
    def _pulseOff(self, iPulse: int, numPulses: int):
        raise NotImplementedError  # to be implemented by subclass
    

@attr.s(auto_attribs=True)
class BackgroundPulseLogger(BackgroundPulseTriggerHandler):
    """
    Test class for verifying functionality of BackgroundPulseTriggerHandler without
    any extra hardware required.
    """
    def __attrs_post_init__(self):
        super().__attrs_post_init__()

    def _pulseOn(self, iPulse: int, numPulses: int):
        logging.exp(f'Pulse {iPulse+1}/{numPulses} on')

    def _pulseOff(self, iPulse: int, numPulses: int):
        logging.exp(f'Pulse {iPulse+1}/{numPulses} off')


@attr.s(auto_attribs=True)
class PolledPulseTriggerHandler(TimeMultiplexedSingleChannelTriggerHandler):
    _pulseGenerator: tp.Optional[tp.Generator[None, None, None]] = attr.ib(init=False, default=None)

    def __attrs_post_init__(self):
        super().__attrs_post_init__()
    
    def update(self):
        if not self._queue.empty():
            didAcquire = self._triggerInProgress.acquire(False)
            if not didAcquire:
                errMsg = 'Condition lock not available'
                logging.error(errMsg)
                raise RuntimeError(errMsg)
            numPulses = self._queue.get_nowait()

            assert self._pulseGenerator is None
            self._pulseGenerator = self._generatePulses(numPulses=numPulses)

        if self._pulseGenerator is not None:
            try:
                next(self._pulseGenerator)
            except StopIteration:
                self._pulseGenerator = None
                self._triggerInProgress.release()
            else:
                return
            
    def _trigger(self, key: str):
        super()._trigger(key)
        self.update()

    def _generatePulses(self, numPulses: int) -> tp.Generator[None, None, None]:
        logging.debug(f'Triggering numPulses={numPulses}')
        triggerStartTime = time.time()
        for iPulse in range(numPulses):
            self._pulseOn(iPulse=iPulse, numPulses=numPulses)
            while time.time() - triggerStartTime < iPulse * (self._pulseOnTime + self._pulseOffTime) + self._pulseOnTime:
                yield  
            self._pulseOff(iPulse=iPulse, numPulses=numPulses)
            while time.time() - triggerStartTime < (iPulse + 1) * (self._pulseOnTime + self._pulseOffTime):
                yield

    def _pulseOn(self, iPulse: int, numPulses: int):
        raise NotImplementedError  # to be implemented by subclass
    
    def _pulseOff(self, iPulse: int, numPulses: int):
        raise NotImplementedError  # to be implemented by subclass


@attr.s(auto_attribs=True)
class PolledPulseLogger(PolledPulseTriggerHandler):
    def __attrs_post_init__(self):
        super().__attrs_post_init__()

    def _pulseOn(self, iPulse: int, numPulses: int):
        logging.exp(f'Pulse {iPulse+1}/{numPulses} on')

    def _pulseOff(self, iPulse: int, numPulses: int):
        logging.exp(f'Pulse {iPulse+1}/{numPulses} off')    


@attr.s(auto_attribs=True, kw_only=True)
class CombinedTriggerHandlers(TriggerHandler):
    """
    Send triggers with multiple handlers at once.

    Note that trigger IDs may be different between handlers depending on their own key->value mapping,
    timing may be different depending on delay behavior, etc.
    """
    _triggerHandlers: tp.List[TriggerHandler]

    def __attrs_post_init__(self):
        super().__attrs_post_init__()
    
    def register(self, key: str, **kwargs):
        for th in self._triggerHandlers:
            th.register(key=key, **kwargs)
        return super().register(key, **kwargs)
    
    def _register(self, key: str, **kwargs):
        self._triggerKeys.append(key)
    
    def trigger(self, key: str, doDelayUntilWinFlip: bool = False):
        for th in self._triggerHandlers:
            th.trigger(key=key, doDelayUntilWinFlip=doDelayUntilWinFlip)
        # never call self._trigger, let children handle any delays
    
    def _trigger(self, key: str):
        pass

    def update(self):
        for th in self._triggerHandlers:
            th.update()
        return super().update()
    

def getDefaultTriggerHandler(**kwargs) -> TriggerHandler:
    

    whichDefault = 'PhotodiodePulse'
    # whichDefault = 'PulseLog'
    # whichDefault = ('PhotodiodePulse', 'Serial')
    # whichDefault = 'Serial'

    logging.exp(f'Getting default trigger handler {whichDefault}')

    def getHandler(whichDefault: str, **kwargs) -> TriggerHandler:
        if whichDefault == 'BCI2000':  # TODO: set to True unless debugging
            from .BCI2000MultiplexedTriggerHandler import BCI2000MultiplexedTriggerHandler
            return BCI2000MultiplexedTriggerHandler(**kwargs)
        elif whichDefault == 'PhotodiodePulse':
            from .PhotodiodePulseTriggerHandler import PhotodiodePulseTriggerHandler
            return PhotodiodePulseTriggerHandler(**kwargs)
        elif whichDefault == 'RTBoxPulse':
            from .RTBoxPulseTriggerHandler import RTBoxPulseTriggerHandler
            return RTBoxPulseTriggerHandler(**kwargs)
        elif whichDefault == 'PulseLog':
            return BackgroundPulseLogger(**kwargs)
        elif whichDefault == 'Serial':
            from .SerialTriggerHandler import SerialTriggerHandler
            if 'port' not in kwargs:
                kwargs['port'] = 'COM4'
            return SerialTriggerHandler(**kwargs)
        elif whichDefault == 'Log':
            return LogTriggerHandler(**kwargs)
        else:
            raise NotImplementedError(f'Unexpected key: {whichDefault}')

    if isinstance(whichDefault, str):
        return getHandler(whichDefault, **kwargs)
    else:
        # assume whichDefault is a list of keys for multiple handlers
        triggerHandlers = list()
        for key in whichDefault:
            triggerHandlers.append(getHandler(key, **kwargs))

        return CombinedTriggerHandlers(triggerHandlers=triggerHandlers, **kwargs)
    
    
        
