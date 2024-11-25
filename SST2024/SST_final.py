#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Neda Kaboodvand, neda.neuroscience@gmail.com

from datetime import datetime
from psychopy import locale_setup
from psychopy import prefs
from psychopy import sound, gui, visual, core, data, event, logging, clock, colors, layout
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)

import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle, choice as randchoice
import os  # handy system and path functions
import sys  # to get file system encoding

import psychopy.iohub as io
from psychopy.hardware import keyboard

# Run 'Before Experiment' code from code_config
maxResponseTime = 1.25  # in sec

ITISpan = (0.5, 1.0)  # time from response recorded to onset of next trial, jittered if span width > 0
# TODO: set this based on literature or testing; arbitrary for now
fixationSpan = (0.25, 0.25)  # in sec, time after blank before go cue, during which a fixation cue is shown

prepareBlockDuration = 2  # in sec

initialSSD = 0.2
ssdIncrement = 0.05  # increase by this much on correct stop
ssdDecrement = 0.05  # decrease by this much on incorrect go

arrowFillColor_go = 'white'
arrowFillColor_stop = 'red'

leftResponseKeys = ['left',
                    '1',
                    'num_1']
rightResponseKeys = ['right',
                     '2',
                     'num_2']
# Run 'Before Experiment' code from code_setup
import inspect
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from Common.TriggerHandler import getDefaultTriggerHandler

taskVersion = '0.1.7'
# Run 'Before Experiment' code from code_setup_practice





# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)
# Store info about the experiment session
psychopyVersion = '2022.2.2'
expName = 'StopSignalTask'  # from the Builder filename that created this script
expInfo = {
    'participant': f"{randint(0, 999999):06.0f}",
    'session': '001',
    'doPractice': True,
}
# --- Show participant info dialog --
dlg = gui.DlgFromDict(dictionary=expInfo, sortKeys=False, title=expName)
if dlg.OK == False:
    core.quit()  # user pressed cancel
#expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['date'] = datetime.now().strftime('%Y-%m-%d_%H%M%S.%f')  
expInfo['expName'] = expName
expInfo['psychopyVersion'] = psychopyVersion
corTime = core.getTime()
expInfo['coreTime'] =  datetime.fromtimestamp(corTime).strftime('%Y-%m-%d_%H%M%S.%f') 

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + u'data/%s_%s_%s' % (expInfo['participant'], expName, expInfo['date'])

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    originPath='F:\\NotOnDropbox\\ConsultingUCSF\\OCDTasks\\StopSignalTask\\StopSignalTask.py',
    savePickle=True, saveWideText=True,
    dataFileName=filename)
# save a log file for detail verbose info
logFile = logging.LogFile(filename+'.log', level=logging.INFO)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

endExpNow = False  # flag for 'escape' or other condition => quit the exp
frameTolerance = 0.001  # how close to onset before 'same' frame

# Start Code - component code to be run after the window creation

# --- Setup the Window ---
win = visual.Window(
    size=[2560, 1440], fullscr=True, screen=1, 
    winType='pyglet', allowStencil=False,
    monitor='testMonitor', color=[-1, -1, -1], colorSpace='rgb',
    blendMode='avg', useFBO=True, 
    units='height')
win.mouseVisible = False
# store frame rate of monitor if we can measure it
expInfo['frameRate'] = win.getActualFrameRate()
if expInfo['frameRate'] != None:
    frameDur = 1.0 / round(expInfo['frameRate'])
else:
    frameDur = 1.0 / 60.0  # could not measure, so guess
# --- Setup input devices ---
ioConfig = {}

# Setup iohub keyboard
ioConfig['Keyboard'] = dict(use_keymap='psychopy')

ioSession = '1'
if 'session' in expInfo:
    ioSession = str(expInfo['session'])
ioServer = io.launchHubServer(window=win, **ioConfig)
eyetracker = None

# create a default keyboard (e.g. to check for escape)
defaultKeyboard = keyboard.Keyboard(backend='iohub')

# --- Initialize components for Routine "setup" ---
# Run 'Begin Experiment' code from code_setup
# Run 'Begin Experiment' code from code_setup
triggerHandler = getDefaultTriggerHandler(win=win)
triggerHandler.register('practiceStart', numPulses=4)
triggerHandler.register('skippedPracticeStart', numPulses=5)
triggerHandler.register('blockFeedbackStart', numPulses=3)
triggerHandler.register('fixationStart', numPulses=0)
triggerHandler.register('trialStart', numPulses=2)
triggerHandler.register('stopCueStart', numPulses=0)
triggerHandler.register('ITI', numPulses=0)

thisExp.addData('taskVersion', taskVersion)

allResponseKeys = leftResponseKeys + rightResponseKeys

# --- Initialize components for Routine "instr1" ---
text_instr1 = visual.TextStim(win=win, name='text_instr1',
    text='',
    font='Open Sans',
    pos=(0, 0), height=0.05, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-1.0)
key_resp_instr1 = keyboard.Keyboard()

# --- Initialize components for Routine "setup_practice" ---

# --- Initialize components for Routine "prepare_practice" ---
fixation_prepare_practice = visual.ShapeStim(
    win=win, name='fixation_prepare_practice', vertices='cross',
    size=(0.1, 0.1),
    ori=0.0, pos=(0, 0), anchor='center',
    lineWidth=1.0,     colorSpace='rgb',  lineColor='white', fillColor='white',
    opacity=None, depth=-1.0, interpolate=True)

# --- Initialize components for Routine "fixation" ---
poly_fix = visual.ShapeStim(
    win=win, name='poly_fix',
    size=(0.1, 0.1), vertices='circle',
    ori=0.0, pos=(0, 0), anchor='center',
    lineWidth=1.0,     colorSpace='rgb',  lineColor='white', fillColor='white',
    opacity=None, depth=-1.0, interpolate=True)

# --- Initialize components for Routine "trial" ---
key_resp_trial = keyboard.Keyboard()
arrow = visual.ShapeStim(
    win=win, name='arrow', vertices=[[-0.5, 0.1], [0.2, 0.1], [0.2, 0.3], [0.5, 0], [0.2, -0.3], [0.2, -0.1], [-0.5, -0.1]],
    size=(0.15, 0.15),
    ori=1.0, pos=(0, 0), anchor='center',
    lineWidth=1.0,     colorSpace='rgb',  lineColor='black', fillColor='white',
    opacity=None, depth=-2.0, interpolate=True)

# --- Initialize components for Routine "ITI" ---
text_ITI = visual.TextStim(win=win, name='text_ITI',
    text='',
    font='Open Sans',
    pos=(0, 0), height=0.07, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=1.0, 
    languageStyle='LTR',
    depth=-1.0);

# --- Initialize components for Routine "block_feedback" ---
text_feedback = visual.TextStim(win=win, name='text_feedback',
    text='',
    font='Open Sans',
    pos=(0, 0), height=0.05, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
key_resp_feedback = keyboard.Keyboard()

# --- Initialize components for Routine "instr2" ---
text_instr2 = visual.TextStim(win=win, name='text_instr2',
    text='',
    font='Open Sans',
    pos=(0, 0), height=0.05, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
key_resp_instr2 = keyboard.Keyboard()

# --- Initialize components for Routine "setup_block" ---
text_setup_block = visual.TextStim(win=win, name='text_setup_block',
    text='Prepare to start the next block.\n\nPress space to continue.',
    font='Open Sans',
    pos=(0, 0), height=0.05, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-1.0);
key_resp_setup_block = keyboard.Keyboard()

# --- Initialize components for Routine "fixation" ---
poly_fix = visual.ShapeStim(
    win=win, name='poly_fix',
    size=(0.1, 0.1), vertices='circle',
    ori=0.0, pos=(0, 0), anchor='center',
    lineWidth=1.0,     colorSpace='rgb',  lineColor='white', fillColor='white',
    opacity=None, depth=-1.0, interpolate=True)

# --- Initialize components for Routine "trial" ---
key_resp_trial = keyboard.Keyboard()
arrow = visual.ShapeStim(
    win=win, name='arrow', vertices=[[-0.5, 0.1], [0.2, 0.1], [0.2, 0.3], [0.5, 0], [0.2, -0.3], [0.2, -0.1], [-0.5, -0.1]],
    size=(0.15, 0.15),
    ori=1.0, pos=(0, 0), anchor='center',
    lineWidth=1.0,     colorSpace='rgb',  lineColor='black', fillColor='white',
    opacity=None, depth=-2.0, interpolate=True)

# --- Initialize components for Routine "ITI" ---
text_ITI = visual.TextStim(win=win, name='text_ITI',
    text='',
    font='Open Sans',
    pos=(0, 0), height=0.07, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=1.0, 
    languageStyle='LTR',
    depth=-1.0)

# --- Initialize components for Routine "block_feedback" ---
text_feedback = visual.TextStim(win=win, name='text_feedback',
    text='',
    font='Open Sans',
    pos=(0, 0), height=0.05, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0)
key_resp_feedback = keyboard.Keyboard()

# --- Initialize components for Routine "done" ---
text_done = visual.TextStim(win=win, name='text_done',
    text='Done!\n\nPress space to continue.',
    font='Open Sans',
    pos=(0, 0), height=0.05, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0)
key_resp_done = keyboard.Keyboard()

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.Clock()  # to track time remaining of each (possibly non-slip) routine 

# --- Prepare to start Routine "setup" ---
continueRoutine = True
routineForceEnded = False
# update component parameters for each repeat
# Run 'Begin Routine' code from code_setup
thisTrialSSD = initialSSD
# keep track of which components have finished
setupComponents = []
for thisComponent in setupComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
frameN = -1

# --- Run Routine "setup" ---
while continueRoutine:
    # get current time
    t = routineTimer.getTime()
    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        routineForceEnded = True
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in setupComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# --- Ending Routine "setup" ---
for thisComponent in setupComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# the Routine "setup" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# --- Prepare to start Routine "instr1" ---
continueRoutine = True
routineForceEnded = False
# update component parameters for each repeat
# Run 'Begin Routine' code from code_instr1
if expInfo['doPractice']:
    instrText = inspect.cleandoc("""
    Stop signal task


    In each trial, you will see a left or right arrow. Your task in most trials is to press the corresponding arrow on the keyboard as quickly and accurately as possible. 

    However, if you see the arrow turn red, withhold your response and do not press any key.

    We will start with some practice trials. Press SPACE to continue.
    """)
    
else:
    instrText = inspect.cleandoc("""
    Stop signal task


    In each trial, you will see a left or right arrow. Your task in most trials is to press the corresponding arrow on the keyboard as quickly and accurately as possible. 

    However, if you see the arrow turn red, withhold your response and do not press any key.

    Practice skipped. We will start with the main task. Press SPACE to continue.
    """)
text_instr1.setText(instrText)
key_resp_instr1.keys = []
key_resp_instr1.rt = []
_key_resp_instr1_allKeys = []
# keep track of which components have finished
instr1Components = [text_instr1, key_resp_instr1]
for thisComponent in instr1Components:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
frameN = -1

# --- Run Routine "instr1" ---
while continueRoutine:
    # get current time
    t = routineTimer.getTime()
    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    # Run 'Each Frame' code from code_instr1
    triggerHandler.update()
    
    # *text_instr1* updates
    if text_instr1.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        text_instr1.frameNStart = frameN  # exact frame index
        text_instr1.tStart = t  # local t and not account for scr refresh
        text_instr1.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(text_instr1, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'text_instr1.started')
        text_instr1.setAutoDraw(True)

 
    # *key_resp_instr1* updates
    waitOnFlip = False  
    if key_resp_instr1.status == NOT_STARTED and tThisFlip >= 1-frameTolerance:
        # keep track of start time/frame for later
        key_resp_instr1.frameNStart = frameN  # exact frame index
        key_resp_instr1.tStart = t  # local t and not account for scr refresh
        key_resp_instr1.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(key_resp_instr1, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'key_resp_instr1.started')
        key_resp_instr1.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(key_resp_instr1.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(key_resp_instr1.clearEvents, eventType='keyboard')  # clear events on next screen flip
    if key_resp_instr1.status == STARTED and not waitOnFlip:
        theseKeys = key_resp_instr1.getKeys(keyList=['space'], waitRelease=False)
        _key_resp_instr1_allKeys.extend(theseKeys)
        if len(_key_resp_instr1_allKeys):
            key_resp_instr1.keys = _key_resp_instr1_allKeys[-1].name  # just the last key pressed
            key_resp_instr1.rt = _key_resp_instr1_allKeys[-1].rt
            # a response ends the routine
            continueRoutine = False
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        routineForceEnded = True
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in instr1Components:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# --- Ending Routine "instr1" ---
for thisComponent in instr1Components:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# check responses
if key_resp_instr1.keys in ['', [], None]:  # No response was made
    key_resp_instr1.keys = None
thisExp.addData('key_resp_instr1.keys',key_resp_instr1.keys)
if key_resp_instr1.keys != None:  # we had a response
    thisExp.addData('key_resp_instr1.rt', key_resp_instr1.rt)
thisExp.nextEntry()
# the Routine "instr1" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# --- Prepare to start Routine "setup_practice" ---
continueRoutine = True
routineForceEnded = False
# update component parameters for each repeat
# Run 'Begin Routine' code from code_setup_practice
thisBlockLabel = "practice"
isPractice = True

blockGoRTs = []
blockNumGoOmissions = 0
blockNumGoResponses = 0
blockNumGoTrials = 0
blockNumStopTrials = 0
blockNumStopFailures = 0
# keep track of which components have finished
setup_practiceComponents = []
for thisComponent in setup_practiceComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
frameN = -1

# --- Run Routine "setup_practice" ---
while continueRoutine:
    # get current time
    t = routineTimer.getTime()
    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        routineForceEnded = True
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in setup_practiceComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# --- Ending Routine "setup_practice" ---
for thisComponent in setup_practiceComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# the Routine "setup_practice" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# --- Prepare to start Routine "prepare_practice" ---
continueRoutine = True
routineForceEnded = False
# update component parameters for each repeat
# Run 'Begin Routine' code from code_prepare_practice
if expInfo['doPractice']:
    triggerHandler.trigger('practiceStart')
else:
    triggerHandler.trigger('skippedPracticeStart')
# keep track of which components have finished
prepare_practiceComponents = [fixation_prepare_practice]
for thisComponent in prepare_practiceComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
frameN = -1

# --- Run Routine "prepare_practice" ---
while continueRoutine:
    # get current time
    t = routineTimer.getTime()
    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    # Run 'Each Frame' code from code_prepare_practice
    triggerHandler.update()
    
    # *fixation_prepare_practice* updates
    if fixation_prepare_practice.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        fixation_prepare_practice.frameNStart = frameN  # exact frame index
        fixation_prepare_practice.tStart = t  # local t and not account for scr refresh
        fixation_prepare_practice.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(fixation_prepare_practice, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'fixation_prepare_practice.started')
        fixation_prepare_practice.setAutoDraw(True)
    if fixation_prepare_practice.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > fixation_prepare_practice.tStartRefresh + prepareBlockDuration-frameTolerance:
            # keep track of stop time/frame for later
            fixation_prepare_practice.tStop = t  # not accounting for scr refresh
            fixation_prepare_practice.frameNStop = frameN  # exact frame index
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'fixation_prepare_practice.stopped')
            fixation_prepare_practice.setAutoDraw(False)
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        routineForceEnded = True
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in prepare_practiceComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# --- Ending Routine "prepare_practice" ---
for thisComponent in prepare_practiceComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# the Routine "prepare_practice" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# set up handler to look after randomisation of conditions etc
practiceTrials = data.TrialHandler(nReps=4 if expInfo['doPractice'] else 0, method='random', 
    extraInfo=expInfo, originPath=-1,
    trialList=data.importConditions('PracticeTrialConditions.csv'),
    seed=None, name='practiceTrials')
thisExp.addLoop(practiceTrials)  # add the loop to the experiment
thisPracticeTrial = practiceTrials.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisPracticeTrial.rgb)
if thisPracticeTrial != None:
    for paramName in thisPracticeTrial:
        exec('{} = thisPracticeTrial[paramName]'.format(paramName))

for thisPracticeTrial in practiceTrials:
    currentLoop = practiceTrials
    # abbreviate parameter names if possible (e.g. rgb = thisPracticeTrial.rgb)
    if thisPracticeTrial != None:
        for paramName in thisPracticeTrial:
            exec('{} = thisPracticeTrial[paramName]'.format(paramName))
    
    # --- Prepare to start Routine "fixation" ---
    continueRoutine = True
    routineForceEnded = False
    # update component parameters for each repeat
    # Run 'Begin Routine' code from code_fix
    thisFixationDuration = random() * (fixationSpan[1] - fixationSpan[0]) + fixationSpan[0]
    triggerHandler.trigger('fixationStart', doDelayUntilWinFlip=True)
    # keep track of which components have finished
    fixationComponents = [poly_fix]
    for thisComponent in fixationComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "fixation" ---
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        # Run 'Each Frame' code from code_fix
        triggerHandler.update()
        
        # *poly_fix* updates
        if poly_fix.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            poly_fix.frameNStart = frameN  # exact frame index
            poly_fix.tStart = t  # local t and not account for scr refresh
            poly_fix.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(poly_fix, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'poly_fix.started')
            poly_fix.setAutoDraw(True)
        if poly_fix.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > poly_fix.tStartRefresh + thisFixationDuration-frameTolerance:
                # keep track of stop time/frame for later
                poly_fix.tStop = t  # not accounting for scr refresh
                poly_fix.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'poly_fix.stopped')
                poly_fix.setAutoDraw(False)
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in fixationComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "fixation" ---
    for thisComponent in fixationComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # the Routine "fixation" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "trial" ---
    continueRoutine = True
    routineForceEnded = False
    # update component parameters for each repeat
    # Run 'Begin Routine' code from code_trial
    thisExp.addData('SSD', thisTrialSSD if stopOrGo == 'stop' else '')
    hasShownStopThisTrial = False
    arrowFillColor = arrowFillColor_go
    triggerHandler.trigger('trialStart', doDelayUntilWinFlip=True)
    key_resp_trial.keys = []
    key_resp_trial.rt = []
    _key_resp_trial_allKeys = []
    arrow.setOri(0 if arrowDirection=='right' else 180)
    # keep track of which components have finished
    trialComponents = [key_resp_trial, arrow]
    for thisComponent in trialComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "trial" ---
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        # Run 'Each Frame' code from code_trial
        if stopOrGo == 'stop' and not hasShownStopThisTrial and tThisFlip >= thisTrialSSD-frameTolerance:
            arrowFillColor = arrowFillColor_stop
            hasShownStopThisTrial = True
            thisExp.timestampOnFlip(win, 'arrow_stop.started')
            triggerHandler.trigger('stopCueStart', doDelayUntilWinFlip=True)
        
        triggerHandler.update()
        
        # *key_resp_trial* updates
        waitOnFlip = False
        if key_resp_trial.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            key_resp_trial.frameNStart = frameN  # exact frame index
            key_resp_trial.tStart = t  # local t and not account for scr refresh
            key_resp_trial.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(key_resp_trial, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'key_resp_trial.started')
            key_resp_trial.status = STARTED
            # AllowedKeys looks like a variable named `allResponseKeys`
            if not type(allResponseKeys) in [list, tuple, np.ndarray]:
                if not isinstance(allResponseKeys, str):
                    logging.error('AllowedKeys variable `allResponseKeys` is not string- or list-like.')
                    core.quit()
                elif not ',' in allResponseKeys:
                    allResponseKeys = (allResponseKeys,)
                else:
                    allResponseKeys = eval(allResponseKeys)
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(key_resp_trial.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(key_resp_trial.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if key_resp_trial.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > key_resp_trial.tStartRefresh + maxResponseTime-frameTolerance:
                # keep track of stop time/frame for later
                key_resp_trial.tStop = t  # not accounting for scr refresh
                key_resp_trial.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'key_resp_trial.stopped')
                key_resp_trial.status = FINISHED

        if key_resp_trial.status == STARTED and not waitOnFlip:
            NedaRespTime = datetime.now().strftime('%Y-%m-%d_%H%M%S.%f')
            NedaCoreRespTime = core.getTime()  
            NedaCoreRespTime = datetime.fromtimestamp(NedaCoreRespTime).strftime('%Y-%m-%d_%H%M%S.%f') 
            thisExp.addData('NedaCoreRespTime', NedaCoreRespTime)
            thisExp.addData('NedaRespTime', NedaRespTime)
            # key checking here     
            theseKeys = key_resp_trial.getKeys(keyList=list(allResponseKeys), waitRelease=False)
            _key_resp_trial_allKeys.extend(theseKeys)
            if len(_key_resp_trial_allKeys):
                key_resp_trial.keys = _key_resp_trial_allKeys[0].name  # just the first key pressed
                key_resp_trial.rt = _key_resp_trial_allKeys[0].rt
                # a response ends the routine
                continueRoutine = False
        
        # *arrow* updates
        if arrow.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            arrow.frameNStart = frameN  # exact frame index
            arrow.tStart = t  # local t and not account for scr refresh
            arrow.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(arrow, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'arrow.started')
            arrow.setAutoDraw(True)
        
        if arrow.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > arrow.tStartRefresh + maxResponseTime-frameTolerance:
                # keep track of stop time/frame for later
                arrow.tStop = t  # not accounting for scr refresh
                arrow.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'arrow.stopped')
                arrow.setAutoDraw(False)

        if arrow.status == STARTED:  # only update if drawing
            arrow.setFillColor(arrowFillColor, log=False)
        
        # check for quit (typically the Esc key) 
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in trialComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "trial" ---
    for thisComponent in trialComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # Run 'End Routine' code from code_trial
    feedbackStr = ''
    if stopOrGo == 'go':
        wasCorrect = False
        if len(key_resp_trial.keys) > 0:
            if arrowDirection == 'left':
                if key_resp_trial.keys in leftResponseKeys:
                    wasCorrect = True
            elif arrowDirection == 'right':
                if key_resp_trial.keys in rightResponseKeys:
                    wasCorrect = True
            else:
                raise NotImplementedError
        if len(key_resp_trial.keys) == 0:
            feedbackStr = 'Too slow'
            blockGoRTs.append(maxResponseTime)
            blockNumGoOmissions += 1
        else:
            feedbackStr = 'Correct' if wasCorrect else 'Incorrect'
            blockGoRTs.append(key_resp_trial.rt)
            blockNumGoResponses += 1
        blockNumGoTrials += 1    
    else:
        wasCorrect = len(key_resp_trial.keys) == 0
        feedbackStr = 'Correct' if wasCorrect else 'Incorrect'
        if wasCorrect:
            thisTrialSSD += ssdIncrement
        else:
            thisTrialSSD = max(thisTrialSSD - ssdDecrement, 0)
            blockNumStopFailures += 1
        blockNumStopTrials += 1    
            
    thisExp.addData('response', key_resp_trial.keys)
    thisExp.addData('rt', key_resp_trial.rt)
    thisExp.addData('correct', wasCorrect)
    # check responses
    if key_resp_trial.keys in ['', [], None]:  # No response was made
        key_resp_trial.keys = None
    practiceTrials.addData('key_resp_trial.keys',key_resp_trial.keys)
    if key_resp_trial.keys != None:  # we had a response
        practiceTrials.addData('key_resp_trial.rt', key_resp_trial.rt)
    # the Routine "trial" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "ITI" ---
    continueRoutine = True
    routineForceEnded = False
    # update component parameters for each repeat
    # Run 'Begin Routine' code from code_ITI
    thisITI = random() * (ITISpan[1] - ITISpan[0]) + ITISpan[0]
    triggerHandler.trigger('ITI', doDelayUntilWinFlip=True)
    text_ITI.setColor('aqua' if wasCorrect else 'red', colorSpace='rgb')
    text_ITI.setOpacity(isPractice)
    text_ITI.setText(feedbackStr)
    # keep track of which components have finished
    ITIComponents = [text_ITI]
    for thisComponent in ITIComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "ITI" ---
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        # Run 'Each Frame' code from code_ITI
        triggerHandler.update()
        
        # *text_ITI* updates
        if text_ITI.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            text_ITI.frameNStart = frameN  # exact frame index
            text_ITI.tStart = t  # local t and not account for scr refresh
            text_ITI.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(text_ITI, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'text_ITI.started')
            text_ITI.setAutoDraw(True)
        if text_ITI.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > text_ITI.tStartRefresh + thisITI-frameTolerance:
                # keep track of stop time/frame for later
                text_ITI.tStop = t  # not accounting for scr refresh
                text_ITI.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'text_ITI.stopped')
                text_ITI.setAutoDraw(False)
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in ITIComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "ITI" ---
    for thisComponent in ITIComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # the Routine "ITI" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    thisExp.nextEntry()
    
# completed 4 if expInfo['doPractice'] else 0 repeats of 'practiceTrials'

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

# --- Prepare to start Routine "block_feedback" ---
continueRoutine = True
routineForceEnded = False
# update component parameters for each repeat
text_feedback.setText("""Block complete!

Mean reaction time: %.0f ms
(lower is better)

Number of missed responses: %d
(should be zero)

Probability of response after stop signal: %.2f
(should be close to 0.5)

Press space to continue.
""" % (sum(blockGoRTs)/len(blockGoRTs)*1e3, blockNumGoOmissions, blockNumStopFailures / blockNumStopTrials) if expInfo['doPractice'] else "")
key_resp_feedback.keys = []
key_resp_feedback.rt = []
_key_resp_feedback_allKeys = []
# Run 'Begin Routine' code from code_feedback
if isPractice:
    if expInfo['doPractice']:
        triggerHandler.trigger('blockFeedbackStart', doDelayUntilWinFlip=True)
    else:
        continueRoutine=False
# keep track of which components have finished
block_feedbackComponents = [text_feedback, key_resp_feedback]
for thisComponent in block_feedbackComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
frameN = -1

# --- Run Routine "block_feedback" ---
while continueRoutine:
    # get current time
    t = routineTimer.getTime()
    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *text_feedback* updates
    if text_feedback.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        text_feedback.frameNStart = frameN  # exact frame index
        text_feedback.tStart = t  # local t and not account for scr refresh
        text_feedback.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(text_feedback, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'text_feedback.started')
        text_feedback.setAutoDraw(True)
    
    # *key_resp_feedback* updates
    waitOnFlip = False
    if key_resp_feedback.status == NOT_STARTED and tThisFlip >= 1-frameTolerance:
        # keep track of start time/frame for later
        key_resp_feedback.frameNStart = frameN  # exact frame index
        key_resp_feedback.tStart = t  # local t and not account for scr refresh
        key_resp_feedback.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(key_resp_feedback, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'key_resp_feedback.started')
        key_resp_feedback.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(key_resp_feedback.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(key_resp_feedback.clearEvents, eventType='keyboard')  # clear events on next screen flip

    if key_resp_feedback.status == STARTED and not waitOnFlip:
        theseKeys = key_resp_feedback.getKeys(keyList=['space'], waitRelease=False)
        _key_resp_feedback_allKeys.extend(theseKeys)
        if len(_key_resp_feedback_allKeys):
            key_resp_feedback.keys = _key_resp_feedback_allKeys[-1].name  # just the last key pressed
            key_resp_feedback.rt = _key_resp_feedback_allKeys[-1].rt
            # a response ends the routine
            continueRoutine = False
    # Run 'Each Frame' code from code_feedback
    triggerHandler.update()
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        routineForceEnded = True
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in block_feedbackComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# --- Ending Routine "block_feedback" ---
for thisComponent in block_feedbackComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# check responses
if key_resp_feedback.keys in ['', [], None]:  # No response was made
    key_resp_feedback.keys = None
thisExp.addData('key_resp_feedback.keys',key_resp_feedback.keys)
if key_resp_feedback.keys != None:  # we had a response
    thisExp.addData('key_resp_feedback.rt', key_resp_feedback.rt)
thisExp.nextEntry()
# the Routine "block_feedback" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# --- Prepare to start Routine "instr2" ---
continueRoutine = True
routineForceEnded = False
# update component parameters for each repeat
key_resp_instr2.keys = []
key_resp_instr2.rt = []
_key_resp_instr2_allKeys = []
# Run 'Begin Routine' code from code_practice_cleanup
thisTrialSSD = initialSSD

if not expInfo['doPractice']:
    continueRoutine=False
# keep track of which components have finished
instr2Components = [text_instr2, key_resp_instr2]
for thisComponent in instr2Components:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
frameN = -1

# --- Run Routine "instr2" ---
while continueRoutine:
    # get current time
    t = routineTimer.getTime()
    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *text_instr2* updates
    if text_instr2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        text_instr2.frameNStart = frameN  # exact frame index
        text_instr2.tStart = t  # local t and not account for scr refresh
        text_instr2.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(text_instr2, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'text_instr2.started')
        text_instr2.setAutoDraw(True)
    if text_instr2.status == STARTED:  # only update if drawing
        text_instr2.setText('Practice complete. \n\nPress space when ready to proceed with main task.', log=False)
    
    # *key_resp_instr2* updates
    waitOnFlip = False
    if key_resp_instr2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        key_resp_instr2.frameNStart = frameN  # exact frame index
        key_resp_instr2.tStart = t  # local t and not account for scr refresh
        key_resp_instr2.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(key_resp_instr2, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'key_resp_instr2.started')
        key_resp_instr2.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(key_resp_instr2.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(key_resp_instr2.clearEvents, eventType='keyboard')  # clear events on next screen flip
    if key_resp_instr2.status == STARTED and not waitOnFlip:
        theseKeys = key_resp_instr2.getKeys(keyList=['space'], waitRelease=False)
        _key_resp_instr2_allKeys.extend(theseKeys)
        if len(_key_resp_instr2_allKeys):
            key_resp_instr2.keys = _key_resp_instr2_allKeys[-1].name  # just the last key pressed
            key_resp_instr2.rt = _key_resp_instr2_allKeys[-1].rt
            # a response ends the routine
            continueRoutine = False
    # Run 'Each Frame' code from code_practice_cleanup
    triggerHandler.update()
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        routineForceEnded = True
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in instr2Components:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# --- Ending Routine "instr2" ---
for thisComponent in instr2Components:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# check responses
if key_resp_instr2.keys in ['', [], None]:  # No response was made
    key_resp_instr2.keys = None
thisExp.addData('key_resp_instr2.keys',key_resp_instr2.keys)
if key_resp_instr2.keys != None:  # we had a response
    thisExp.addData('key_resp_instr2.rt', key_resp_instr2.rt)
thisExp.nextEntry()
# the Routine "instr2" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# set up handler to look after randomisation of conditions etc
blocks = data.TrialHandler(nReps=5.0, method='random', 
    extraInfo=expInfo, originPath=-1,
    trialList=[None],
    seed=None, name='blocks')
thisExp.addLoop(blocks)  # add the loop to the experiment
thisBlock = blocks.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisBlock.rgb)
if thisBlock != None:
    for paramName in thisBlock:
        exec('{} = thisBlock[paramName]'.format(paramName))

for thisBlock in blocks:
    currentLoop = blocks
    # abbreviate parameter names if possible (e.g. rgb = thisBlock.rgb)
    if thisBlock != None:
        for paramName in thisBlock:
            exec('{} = thisBlock[paramName]'.format(paramName))
    
    # --- Prepare to start Routine "setup_block" ---
    continueRoutine = True
    routineForceEnded = False
    # update component parameters for each repeat
    # Run 'Begin Routine' code from code_setup_block
    thisBlockLabel = blocks.thisN + 1
    isPractice = False
    
    
    blockGoRTs = []
    blockNumGoOmissions = 0
    blockNumGoResponses = 0
    blockNumGoTrials = 0
    blockNumStopTrials = 0
    blockNumStopFailures = 0
    
    if blocks.thisN == 0:
        continueRoutine = False  # we just showed instruction screen before this, don't need to pause here
    key_resp_setup_block.keys = []
    key_resp_setup_block.rt = []
    _key_resp_setup_block_allKeys = []
    # keep track of which components have finished
    setup_blockComponents = [text_setup_block, key_resp_setup_block]
    for thisComponent in setup_blockComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "setup_block" ---
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        # Run 'Each Frame' code from code_setup_block
        triggerHandler.update()
        
        # *text_setup_block* updates
        if text_setup_block.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            text_setup_block.frameNStart = frameN  # exact frame index
            text_setup_block.tStart = t  # local t and not account for scr refresh
            text_setup_block.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(text_setup_block, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'text_setup_block.started')
            text_setup_block.setAutoDraw(True)
        
        # *key_resp_setup_block* updates
        waitOnFlip = False
        if key_resp_setup_block.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            key_resp_setup_block.frameNStart = frameN  # exact frame index
            key_resp_setup_block.tStart = t  # local t and not account for scr refresh
            key_resp_setup_block.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(key_resp_setup_block, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'key_resp_setup_block.started')
            key_resp_setup_block.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(key_resp_setup_block.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(key_resp_setup_block.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if key_resp_setup_block.status == STARTED and not waitOnFlip:
            theseKeys = key_resp_setup_block.getKeys(keyList=['space'], waitRelease=False)
            _key_resp_setup_block_allKeys.extend(theseKeys)
            if len(_key_resp_setup_block_allKeys):
                key_resp_setup_block.keys = _key_resp_setup_block_allKeys[-1].name  # just the last key pressed
                key_resp_setup_block.rt = _key_resp_setup_block_allKeys[-1].rt
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in setup_blockComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "setup_block" ---
    for thisComponent in setup_blockComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # check responses
    if key_resp_setup_block.keys in ['', [], None]:  # No response was made
        key_resp_setup_block.keys = None
    blocks.addData('key_resp_setup_block.keys',key_resp_setup_block.keys)
    if key_resp_setup_block.keys != None:  # we had a response
        blocks.addData('key_resp_setup_block.rt', key_resp_setup_block.rt)
    # the Routine "setup_block" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # set up handler to look after randomisation of conditions etc
    subblocks = data.TrialHandler(nReps=4.0, method='random', 
        extraInfo=expInfo, originPath=-1,
        trialList=[None],
        seed=None, name='subblocks')
    thisExp.addLoop(subblocks)  # add the loop to the experiment
    thisSubblock = subblocks.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisSubblock.rgb)
    if thisSubblock != None:
        for paramName in thisSubblock:
            exec('{} = thisSubblock[paramName]'.format(paramName))
    
    for thisSubblock in subblocks:
        currentLoop = subblocks
        # abbreviate parameter names if possible (e.g. rgb = thisSubblock.rgb)
        if thisSubblock != None:
            for paramName in thisSubblock:
                exec('{} = thisSubblock[paramName]'.format(paramName))
        
        # set up handler to look after randomisation of conditions etc
        trials = data.TrialHandler(nReps=2.0, method='random', 
            extraInfo=expInfo, originPath=-1,
            trialList=data.importConditions('TrialConditions.csv'),
            seed=None, name='trials')
        thisExp.addLoop(trials)  # add the loop to the experiment
        thisTrial = trials.trialList[0]  # so we can initialise stimuli with some values
        # abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
        if thisTrial != None:
            for paramName in thisTrial:
                exec('{} = thisTrial[paramName]'.format(paramName))
        
        for thisTrial in trials:
            currentLoop = trials
            # abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
            if thisTrial != None:
                for paramName in thisTrial:
                    exec('{} = thisTrial[paramName]'.format(paramName))
            
            # --- Prepare to start Routine "fixation" ---
            continueRoutine = True
            routineForceEnded = False
            # update component parameters for each repeat
            # Run 'Begin Routine' code from code_fix
            thisFixationDuration = random() * (fixationSpan[1] - fixationSpan[0]) + fixationSpan[0]
            triggerHandler.trigger('fixationStart', doDelayUntilWinFlip=True)
            # keep track of which components have finished
            fixationComponents = [poly_fix]
            for thisComponent in fixationComponents:
                thisComponent.tStart = None
                thisComponent.tStop = None
                thisComponent.tStartRefresh = None
                thisComponent.tStopRefresh = None
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED
            # reset timers
            t = 0
            _timeToFirstFrame = win.getFutureFlipTime(clock="now")
            frameN = -1
            
            # --- Run Routine "fixation" ---
            while continueRoutine:
                # get current time
                t = routineTimer.getTime()
                tThisFlip = win.getFutureFlipTime(clock=routineTimer)
                tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame
                # Run 'Each Frame' code from code_fix
                triggerHandler.update()
                
                # *poly_fix* updates
                if poly_fix.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                    # keep track of start time/frame for later
                    poly_fix.frameNStart = frameN  # exact frame index
                    poly_fix.tStart = t  # local t and not account for scr refresh
                    poly_fix.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(poly_fix, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'poly_fix.started')
                    poly_fix.setAutoDraw(True)
                if poly_fix.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > poly_fix.tStartRefresh + thisFixationDuration-frameTolerance:
                        # keep track of stop time/frame for later
                        poly_fix.tStop = t  # not accounting for scr refresh
                        poly_fix.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'poly_fix.stopped')
                        poly_fix.setAutoDraw(False)
                
                # check for quit (typically the Esc key)
                if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                    core.quit()
                
                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    routineForceEnded = True
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in fixationComponents:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            
            # --- Ending Routine "fixation" ---
            for thisComponent in fixationComponents:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            # the Routine "fixation" was not non-slip safe, so reset the non-slip timer
            routineTimer.reset()
            
            # --- Prepare to start Routine "trial" ---
            continueRoutine = True
            routineForceEnded = False
            # update component parameters for each repeat
            # Run 'Begin Routine' code from code_trial
            thisExp.addData('SSD', thisTrialSSD if stopOrGo == 'stop' else '')
            hasShownStopThisTrial = False
            arrowFillColor = arrowFillColor_go
            triggerHandler.trigger('trialStart', doDelayUntilWinFlip=True)
            key_resp_trial.keys = []
            key_resp_trial.rt = []
            _key_resp_trial_allKeys = []
            arrow.setOri(0 if arrowDirection=='right' else 180)
            # keep track of which components have finished
            trialComponents = [key_resp_trial, arrow]
            for thisComponent in trialComponents:
                thisComponent.tStart = None
                thisComponent.tStop = None
                thisComponent.tStartRefresh = None
                thisComponent.tStopRefresh = None
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED
            # reset timers
            t = 0
            _timeToFirstFrame = win.getFutureFlipTime(clock="now")
            frameN = -1
            
            # --- Run Routine "trial" ---
            while continueRoutine:
                # get current time
                t = routineTimer.getTime()
                tThisFlip = win.getFutureFlipTime(clock=routineTimer)
                tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame
                # Run 'Each Frame' code from code_trial
                if stopOrGo == 'stop' and not hasShownStopThisTrial and tThisFlip >= thisTrialSSD-frameTolerance:
                    arrowFillColor = arrowFillColor_stop
                    hasShownStopThisTrial = True
                    thisExp.timestampOnFlip(win, 'arrow_stop.started')
                    triggerHandler.trigger('stopCueStart', doDelayUntilWinFlip=True)
                
                triggerHandler.update()
                
                # *key_resp_trial* updates
                waitOnFlip = False
                if key_resp_trial.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                    # keep track of start time/frame for later
                    key_resp_trial.frameNStart = frameN  # exact frame index
                    key_resp_trial.tStart = t  # local t and not account for scr refresh
                    key_resp_trial.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(key_resp_trial, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'key_resp_trial.started')
                    key_resp_trial.status = STARTED
                    # AllowedKeys looks like a variable named `allResponseKeys`
                    if not type(allResponseKeys) in [list, tuple, np.ndarray]:
                        if not isinstance(allResponseKeys, str):
                            logging.error('AllowedKeys variable `allResponseKeys` is not string- or list-like.')
                            core.quit()
                        elif not ',' in allResponseKeys:
                            allResponseKeys = (allResponseKeys,)
                        else:
                            allResponseKeys = eval(allResponseKeys)
                    # keyboard checking is just starting
                    waitOnFlip = True
                    win.callOnFlip(key_resp_trial.clock.reset)  # t=0 on next screen flip
                    win.callOnFlip(key_resp_trial.clearEvents, eventType='keyboard')  # clear events on next screen flip
                if key_resp_trial.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > key_resp_trial.tStartRefresh + maxResponseTime-frameTolerance:
                        # keep track of stop time/frame for later
                        key_resp_trial.tStop = t  # not accounting for scr refresh
                        key_resp_trial.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'key_resp_trial.stopped')
                        key_resp_trial.status = FINISHED
                if key_resp_trial.status == STARTED and not waitOnFlip:
                    NedaRespTime = datetime.now().strftime('%Y-%m-%d_%H%M%S.%f')
                    NedaCoreRespTime = core.getTime() 
                    NedaCoreRespTime = datetime.fromtimestamp(NedaCoreRespTime).strftime('%Y-%m-%d_%H%M%S.%f')
                    thisExp.addData('NedaCoreRespTime', NedaCoreRespTime)
                    thisExp.addData('NedaRespTime', NedaRespTime)
                    # key checking here   
                    theseKeys = key_resp_trial.getKeys(keyList=list(allResponseKeys), waitRelease=False)
                    _key_resp_trial_allKeys.extend(theseKeys)
                    if len(_key_resp_trial_allKeys):

                        NedaRespTime = datetime.now().strftime('%Y-%m-%d_%H%M%S.%f')  
                        trials.addData('NedaRespTime', NedaRespTime)

                        key_resp_trial.keys = _key_resp_trial_allKeys[0].name  # just the first key pressed
                        key_resp_trial.rt = _key_resp_trial_allKeys[0].rt
                        # a response ends the routine
                        continueRoutine = False
                
                # *arrow* updates
                if arrow.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                    # keep track of start time/frame for later
                    arrow.frameNStart = frameN  # exact frame index
                    arrow.tStart = t  # local t and not account for scr refresh
                    arrow.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(arrow, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'arrow.started')
                    arrow.setAutoDraw(True)

                if arrow.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > arrow.tStartRefresh + maxResponseTime-frameTolerance:
                        # keep track of stop time/frame for later
                        arrow.tStop = t  # not accounting for scr refresh
                        arrow.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'arrow.stopped')
                        arrow.setAutoDraw(False)
                if arrow.status == STARTED:  # only update if drawing
                    ArrowStartTime = datetime.now().strftime('%Y-%m-%d_%H%M%S.%f')
                    ArrowStartCoreTime = core.getTime() 
                    ArrowStartCoreTime = datetime.fromtimestamp(ArrowStartCoreTime).strftime('%Y-%m-%d_%H%M%S.%f')  
                    thisExp.addData('ArrowStartCoreTime', ArrowStartCoreTime)
                    thisExp.addData('ArrowStartTime', ArrowStartTime)
                    arrow.setFillColor(arrowFillColor, log=False)
               
                # check for quit (typically the Esc key)
                if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                    core.quit()
                
                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    routineForceEnded = True
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in trialComponents:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            
            # --- Ending Routine "trial" ---
            for thisComponent in trialComponents:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            # Run 'End Routine' code from code_trial
            feedbackStr = ''
            if stopOrGo == 'go':
                wasCorrect = False
                if len(key_resp_trial.keys) > 0:
                    if arrowDirection == 'left':
                        if key_resp_trial.keys in leftResponseKeys:
                            wasCorrect = True
                    elif arrowDirection == 'right':
                        if key_resp_trial.keys in rightResponseKeys:
                            wasCorrect = True
                    else:
                        raise NotImplementedError
                if len(key_resp_trial.keys) == 0:
                    feedbackStr = 'Too slow'
                    blockGoRTs.append(maxResponseTime)
                    blockNumGoOmissions += 1
                else:
                    feedbackStr = 'Correct' if wasCorrect else 'Incorrect'
                    blockGoRTs.append(key_resp_trial.rt)
                    blockNumGoResponses += 1
                blockNumGoTrials += 1    
            else:
                wasCorrect = len(key_resp_trial.keys) == 0
                feedbackStr = 'Correct' if wasCorrect else 'Incorrect'
                if wasCorrect:
                    thisTrialSSD += ssdIncrement
                else:
                    thisTrialSSD = max(thisTrialSSD - ssdDecrement, 0)
                    blockNumStopFailures += 1
                blockNumStopTrials += 1    
                    
            thisExp.addData('response', key_resp_trial.keys)
            thisExp.addData('rt', key_resp_trial.rt)
            thisExp.addData('correct', wasCorrect)
            # check responses
            if key_resp_trial.keys in ['', [], None]:  # No response was made
                key_resp_trial.keys = None
            trials.addData('key_resp_trial.keys',key_resp_trial.keys)
            if key_resp_trial.keys != None:  # we had a response
                trials.addData('key_resp_trial.rt', key_resp_trial.rt)
            # the Routine "trial" was not non-slip safe, so reset the non-slip timer
            routineTimer.reset()
            
            # --- Prepare to start Routine "ITI" ---
            continueRoutine = True
            routineForceEnded = False
            # update component parameters for each repeat
            # Run 'Begin Routine' code from code_ITI
            thisITI = random() * (ITISpan[1] - ITISpan[0]) + ITISpan[0]
            triggerHandler.trigger('ITI', doDelayUntilWinFlip=True)
            text_ITI.setColor('aqua' if wasCorrect else 'red', colorSpace='rgb')
            text_ITI.setOpacity(isPractice)
            text_ITI.setText(feedbackStr)
            # keep track of which components have finished
            ITIComponents = [text_ITI]
            for thisComponent in ITIComponents:
                thisComponent.tStart = None
                thisComponent.tStop = None
                thisComponent.tStartRefresh = None
                thisComponent.tStopRefresh = None
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED
            # reset timers
            t = 0
            _timeToFirstFrame = win.getFutureFlipTime(clock="now")
            frameN = -1
            
            # --- Run Routine "ITI" ---
            while continueRoutine:
                # get current time
                t = routineTimer.getTime()
                tThisFlip = win.getFutureFlipTime(clock=routineTimer)
                tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame
                # Run 'Each Frame' code from code_ITI
                triggerHandler.update()
                
                # *text_ITI* updates
                if text_ITI.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                    # keep track of start time/frame for later
                    text_ITI.frameNStart = frameN  # exact frame index
                    text_ITI.tStart = t  # local t and not account for scr refresh
                    text_ITI.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(text_ITI, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'text_ITI.started')
                    text_ITI.setAutoDraw(True)
                if text_ITI.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > text_ITI.tStartRefresh + thisITI-frameTolerance:
                        # keep track of stop time/frame for later
                        text_ITI.tStop = t  # not accounting for scr refresh
                        text_ITI.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'text_ITI.stopped')
                        text_ITI.setAutoDraw(False)
                
                # check for quit (typically the Esc key)
                if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                    core.quit()
                
                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    routineForceEnded = True
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in ITIComponents:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            
            # --- Ending Routine "ITI" ---
            for thisComponent in ITIComponents:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            # the Routine "ITI" was not non-slip safe, so reset the non-slip timer
            routineTimer.reset()
            thisExp.nextEntry()
            
        # completed 2.0 repeats of 'trials'
        
    # completed 4.0 repeats of 'subblocks'
    
    
    # --- Prepare to start Routine "block_feedback" ---
    continueRoutine = True
    routineForceEnded = False
    # update component parameters for each repeat
    text_feedback.setText("""Block complete!

Mean reaction time: %.0f ms
(lower is better)

Number of missed responses: %d
(should be zero)

Probability of response after stop signal: %.2f
(should be close to 0.5)

Press space to continue.
""" % (sum(blockGoRTs)/len(blockGoRTs)*1e3, blockNumGoOmissions, blockNumStopFailures / blockNumStopTrials) if expInfo['doPractice'] else "")
    key_resp_feedback.keys = []
    key_resp_feedback.rt = []
    _key_resp_feedback_allKeys = []
    # Run 'Begin Routine' code from code_feedback
    if isPractice:
        if expInfo['doPractice']:
            triggerHandler.trigger('blockFeedbackStart', doDelayUntilWinFlip=True)
        else:
            continueRoutine=False
    # keep track of which components have finished
    block_feedbackComponents = [text_feedback, key_resp_feedback]
    for thisComponent in block_feedbackComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "block_feedback" ---
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *text_feedback* updates
        if text_feedback.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            text_feedback.frameNStart = frameN  # exact frame index
            text_feedback.tStart = t  # local t and not account for scr refresh
            text_feedback.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(text_feedback, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'text_feedback.started')
            text_feedback.setAutoDraw(True)
        
        # *key_resp_feedback* updates
        waitOnFlip = False
        if key_resp_feedback.status == NOT_STARTED and tThisFlip >= 1-frameTolerance:
            # keep track of start time/frame for later
            key_resp_feedback.frameNStart = frameN  # exact frame index
            key_resp_feedback.tStart = t  # local t and not account for scr refresh
            key_resp_feedback.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(key_resp_feedback, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'key_resp_feedback.started')
            key_resp_feedback.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(key_resp_feedback.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(key_resp_feedback.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if key_resp_feedback.status == STARTED and not waitOnFlip:
            theseKeys = key_resp_feedback.getKeys(keyList=['space'], waitRelease=False)
            _key_resp_feedback_allKeys.extend(theseKeys)
            if len(_key_resp_feedback_allKeys):
                key_resp_feedback.keys = _key_resp_feedback_allKeys[-1].name  # just the last key pressed
                key_resp_feedback.rt = _key_resp_feedback_allKeys[-1].rt
                # a response ends the routine
                continueRoutine = False
        # Run 'Each Frame' code from code_feedback
        triggerHandler.update()
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in block_feedbackComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "block_feedback" ---
    for thisComponent in block_feedbackComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # check responses
    if key_resp_feedback.keys in ['', [], None]:  # No response was made
        key_resp_feedback.keys = None
    blocks.addData('key_resp_feedback.keys',key_resp_feedback.keys)
    if key_resp_feedback.keys != None:  # we had a response
        blocks.addData('key_resp_feedback.rt', key_resp_feedback.rt)
    # the Routine "block_feedback" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
# completed 5.0 repeats of 'blocks'


# --- Prepare to start Routine "done" ---
continueRoutine = True
routineForceEnded = False
# update component parameters for each repeat
key_resp_done.keys = []
key_resp_done.rt = []
_key_resp_done_allKeys = []
# keep track of which components have finished
doneComponents = [text_done, key_resp_done]
for thisComponent in doneComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
frameN = -1

# --- Run Routine "done" ---
while continueRoutine:
    # get current time
    t = routineTimer.getTime()
    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *text_done* updates
    if text_done.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        text_done.frameNStart = frameN  # exact frame index
        text_done.tStart = t  # local t and not account for scr refresh
        text_done.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(text_done, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'text_done.started')
        text_done.setAutoDraw(True)
    
    # *key_resp_done* updates
    waitOnFlip = False
    if key_resp_done.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        key_resp_done.frameNStart = frameN  # exact frame index
        key_resp_done.tStart = t  # local t and not account for scr refresh
        key_resp_done.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(key_resp_done, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'key_resp_done.started')
        key_resp_done.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(key_resp_done.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(key_resp_done.clearEvents, eventType='keyboard')  # clear events on next screen flip
    if key_resp_done.status == STARTED and not waitOnFlip:
        theseKeys = key_resp_done.getKeys(keyList=['space'], waitRelease=False)
        _key_resp_done_allKeys.extend(theseKeys)
        if len(_key_resp_done_allKeys):
            key_resp_done.keys = _key_resp_done_allKeys[-1].name  # just the last key pressed
            key_resp_done.rt = _key_resp_done_allKeys[-1].rt
            # a response ends the routine
            continueRoutine = False
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        routineForceEnded = True
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in doneComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# --- Ending Routine "done" ---
for thisComponent in doneComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# check responses
if key_resp_done.keys in ['', [], None]:  # No response was made
    key_resp_done.keys = None
thisExp.addData('key_resp_done.keys',key_resp_done.keys)
if key_resp_done.keys != None:  # we had a response
    thisExp.addData('key_resp_done.rt', key_resp_done.rt)
thisExp.nextEntry()
# the Routine "done" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# --- End experiment ---
# Flip one final time so any remaining win.callOnFlip() 
# and win.timeOnFlip() tasks get executed before quitting
win.flip()

# these shouldn't be strictly necessary (should auto-save)
thisExp.saveAsWideText(filename+'.csv', delim='auto')
thisExp.saveAsPickle(filename)
logging.flush()
# make sure everything is closed down
if eyetracker:
    eyetracker.setConnectionState(False)
thisExp.abort()  # or data files will save again on exit
win.close()
core.quit()
