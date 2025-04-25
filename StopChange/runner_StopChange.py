# Auhtor: Neda Kaboodvand, neda.neuroscience@gmail.com

import os, sys, random
import numpy as np
from datetime import datetime
from psychopy import visual, core, event, data, gui, logging

from psychopy.hardware import keyboard
kb = keyboard.Keyboard()  # create a persistent keyboard object

# -------------------------------------------------------------------------
# --------------------------- PARAMETERS -----------------------------------
# -------------------------------------------------------------------------
# maxResponseTime   = 1.25 
maxResponseTime = 1 # update on 4/22/2025: 2.0 decreased to 0.7

feedbackDuration  = 0.5    # per-trial feedback in practice
#fixationSpan      = (0.25, 0.25)  # time range for fixation cross
#ITIspan           = (0.5, 1.0)    # random ITI range
# prepareBlockDur   = 2.0           # time before each block starts

'''
[Verbruggen et al. 2019](https://elifesciences.org/articles/46323)
SSD initially set to 300 ms, adjusted in increments of 50 ms
    - But mentioned as starting at 200 ms elsewhere in documentation

Use tracking procedure to vary SSD
        - Increase SSD after each successful stop, decrease SSD after each unsuccessful stop
        - Use 50 ms increment as a reasonable compromise between convergence speed and sensitivity
        - Decrease on **all** unsuccessful stop trials, including both correct and incorrect direction go responses on stop trials.

Indeed, after successful stopping, SSD increases, obstructing the stop process on the next stop-signal trial, 
while after unsuccessful stopping, SSD decreases, helping the stop process on the next stop-signal trial. 
This SST feature is known as “tracking procedure” and it maintains the overall inhibition probability near 50%. 
The tracking procedure allows making participants systematically fail to inhibit their responses at half of the total task trials."

The SSD is increased by 50 ms for each stop trial in which the participant correctly stops; 
the SSD is decreased by 50 ms for each stop trial in which the participant incorrectly "goes" 
(i.e. responds, whether it's the matching direction or not).
'''
# Stop-signal delays (SSD) logic
initialSSD    = 0.2
ssdIncrement  = 0.05 # increase by this much on correct stop
ssdDecrement  = 0.05 # decrease by this much on incorrect go

# Keys
leftKeys   = ['left','1','num_1']
rightKeys  = ['right','2','num_2']
downKeys   = ['down']
escapeKey  = ['escape']
allResp    = leftKeys + rightKeys + downKeys

# For data files
practiceConditionsFile = 'PracticeTrialConditions.csv'
mainConditionsFile     = 'MainTrialConditions.csv'

# Number of practice reps (4 if doPractice, else 0)
practiceReps = 2#4  

# Number of main blocks and repetitions within each block
nMainBlocks = 3#4  
blockReps   = 2  
#8*2*(3+1)=64
# -------------------------------------------------------------------------
# FixationOnTime = [random.uniform(1.5, 2.5) for _ in range(64)]#[random.uniform(1.5, 2.5) for _ in range(TotTrials)]
# PostTrialWaitTime = 0.5
PostTrialWaitTime = [random.uniform(3, 4) for _ in range(64)]
# -------------------------------------------------------------------------
# --------------------------- DIALOG / SETUP -------------------------------
# -------------------------------------------------------------------------
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
_thisDir = os.path.dirname(os.path.abspath(__file__)) #os.path.dirname(__file__)
os.chdir(_thisDir)# Now, the current working directory is the same as the script's directory,and you can access files and directories relative to this location.


expName = 'StopChangeTask'
from numpy.random import randint
expInfo = {
    'participant': f"{randint(0,999999):06d}",
    'session': '001',
    'doPractice': True  # set to False to skip practice
}
dlg = gui.DlgFromDict(dictionary=expInfo, sortKeys=False, title=expName)
if not dlg.OK:
    core.quit()

expInfo['date'] = datetime.now().strftime('%Y-%m-%d_%H%M%S.%f')
corTime = core.getTime() 
expInfo['coreTime'] =  datetime.fromtimestamp(corTime).strftime('%Y-%m-%d_%H%M%S.%f')


if isinstance(expInfo['doPractice'], str):
    expInfo['doPractice'] = (expInfo['doPractice'].lower() == 'true')

# filename = os.path.join(_thisDir, 'data',
#     f"{expInfo['participant']}_{expName}_{data.getDateStr()}")
filename = _thisDir + os.sep + u'data/%s_%s_%s' % (expInfo['participant'], expName, expInfo['date'])
logging.console.setLevel(logging.WARNING)

data_dir = "data"
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

# thisExp = data.ExperimentHandler(name=expName,
#                                  version='',
#                                  extraInfo=expInfo,
#                                  dataFileName=filename)
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    savePickle=True, saveWideText=True,
    dataFileName=filename)

# -------------------------------------------------------------------------
# --------------------------- WINDOW ---------------------------------------
# -------------------------------------------------------------------------
from psychopy import monitors
monitor = monitors.Monitor('testMonitor')
monitor.setWidth(40) 
monitor.setDistance(60)
monitor.save()
winSize=monitor.getSizePix()
win = visual.Window(
    size=winSize, fullscr=True, screen=1, 
    winType='pyglet', allowStencil=False,
    monitor='testMonitor', color='black', colorSpace='rgb',
    blendMode='avg', useFBO=True, units='height')
# win = visual.Window(
#     size=[1920, 1080], fullscr=True, screen=0,
#     winType='pyglet', monitor='testMonitor',
#     color=[-1, -1, -1], colorSpace='rgb',
#     units='height'
# )
win.mouseVisible = False

# -------------------------------------------------------------------------
# --------------------------- HELPER FUNCTIONS -----------------------------
# -------------------------------------------------------------------------
def check_for_esc():
    if 'escape' in event.getKeys():
        thisExp.saveAsWideText(filename+'.csv')
        thisExp.saveAsPickle(filename)
        win.close()
        core.quit()

def wait_for_space():
    event.clearEvents()
    while True:
        keys = event.getKeys(keyList=escapeKey+['space'])
        if keys:
            if 'escape' in keys:
                thisExp.saveAsWideText(filename+'.csv')
                thisExp.saveAsPickle(filename)
                win.close()
                core.quit()
            if 'space' in keys:
                break
        core.wait(0.01)

def log_on_flip(label):
    def callback():
        nowSec = core.getTime()
        nowStr = datetime.now().strftime('%Y-%m-%d_%H:%M:%S.%f')
        thisExp.addData(f"{label}_coreTime", nowSec)
        thisExp.addData(f"{label}_datetime", nowStr)
    return callback

# -------------------------------------------------------------------------
# --------------------------- STIMULI --------------------------------------
# -------------------------------------------------------------------------
planeStim = visual.ImageStim(
    win=win,
    image=None,  # will be set to PlaneLeft.png or PlaneRight.png
    pos=(0,0),
    size=(0.28,0.28)
)
planeLeftPath  = os.path.join(_thisDir, 'PlaneLeft.png')
planeRightPath = os.path.join(_thisDir, 'PlaneRight.png')

fuelStim = visual.ImageStim(
    win=win,
    image=os.path.join(_thisDir, 'fuel.png'),
    pos=(0,0),
    size=(0.15,0.15)
)

fixationCross = visual.TextStim(
    win=win,
    text='+',
    height=0.2,#0.07,
    color='white'
)


# instrText = visual.TextStim(
#     win=win,
#     text="",
#     wrapWidth=1.2,#height=0.05, 
#     color='white')
instrText = visual.TextStim(win=win,
    text="",
    font='Open Sans',
    pos=(0, 0), height=0.05, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-1.0)

# Square trigger (as in KidFlanker_runner.py)
square_size=0.1
square_position=(0.8 - square_size/2, -0.5 + square_size/2)
square = visual.Rect(
    win=win,
    width=square_size,
    height=square_size,
    fillColor='white',
    lineColor=None,
    pos=square_position
)

# Per-trial feedback (for practice)
feedback_correct   = visual.TextStim(win=win, text="Correct!",    color='lime', height=0.06)
feedback_incorrect = visual.TextStim(win=win, text="Incorrect",   color='red',  height=0.06)
feedback_timeout   = visual.TextStim(win=win, text="Respond faster!", color='white', height=0.06)

feedbackText = visual.TextStim(win=win, text="", height=0.05, color='white')
doneText     = visual.TextStim(win=win, text="Done!\nPress any key to exit.", height=0.05, color='white')

# Optional blink at start
# def doBlink(num=4, onTime=0.2, offTime=0.2):
#     for _ in range(num):
#         square.setAutoDraw(True)
#         win.flip()
#         core.wait(onTime)
#         square.setAutoDraw(False)
#         win.flip()
#         core.wait(offTime)

# doBlink()
# -------------------------------------------------------------------------
instrText.setText("Welcome to the task! Stay focused and respond as quickly and accurately as possible.\n\n Press Enter to start.")
# text_instr.setText("You will see five fish in a row, some facing left, some right.\n Your task is to identify the direction of the middle fish by pressing the corresponding key.\n\n Press Enter to continue.")
instrText.draw()
win.flip()
event.waitKeys()

# -------------------------------------------------------------------------
# --------------------------- INSTRUCTIONS ---------------------------------
# -------------------------------------------------------------------------
# if expInfo['doPractice']:
#     instr = ("On each trial:\n\n"
#              " - Plane points LEFT or RIGHT ⇒ press that arrow.\n\n"
#              " - If 'fuel gauge' appears ⇒ press DOWN arrow *instead*.\n\n"
#              "We'll do practice first (with feedback).\n\n"
#              "Press SPACE to begin practice.")
# else:
#     instr = ("On each trial:\n\n"
#              " - Plane points LEFT or RIGHT ⇒ press that arrow.\n\n"
#              " - If 'fuel gauge' appears ⇒ press DOWN arrow *instead*.\n\n"
#              "No practice. We'll go straight to main task.\n\n"
#              "Press SPACE to begin.")
# instrText.text = instr
# instrText.draw()
# win.flip()
# wait_for_space()
def show_text_with_blink(text, blink_count, blink_duration=0.2, inter_blink_interval=0.2):

    total_duration = blink_count * (blink_duration + inter_blink_interval)
    # Use a separate clock for the blinking routine.
    clock = core.Clock()
    # Clear any previous key events
    event.clearEvents()
    while True:
        # Draw the instruction text.
        instrText.setText(text)
        instrText.draw()
        
        # Determine whether to draw the square (blink effect).
        t = clock.getTime()
        if t < total_duration:
            cycle = blink_duration + inter_blink_interval
            # During the "on" phase of the blink cycle, draw the square.
            if (t % cycle) < blink_duration:
                square.draw()
        
        win.flip()
        # wait_for_space()
        keys = event.getKeys(keyList=['space'])
        if keys:
            break

if expInfo['doPractice']:
    instr = ("On each trial:\n\n"
             "If the plane points left or right, press the matching arrow key.\n\n"
             "If a fuel gauge appears, press the down arrow instead.\n\n"
             "We'll start with practice, with feedback on your answers.\n\n"
             "Press SPACE to begin practice.")
else:
    instr = ("On each trial:\n\n"
             "If the plane points left or right, press the matching arrow key.\n\n"
             "If a fuel gauge appears, press the down arrow instead.\n\n"
             "No practice. We'll go straight to main task.\n\n"
             "Press SPACE to begin.")

show_text_with_blink(instr, blink_count=4)

# -------------------------------------------------------------------------
# --------------------------- PRACTICE TRIALS ------------------------------
# -------------------------------------------------------------------------
p_nReps = practiceReps if expInfo['doPractice'] else 0
if p_nReps > 0 and not os.path.exists(practiceConditionsFile):
    logging.warning(f"Practice file {practiceConditionsFile} not found! Skipping practice.")
    p_nReps = 0

practiceTrials = data.TrialHandler(
    nReps=p_nReps, 
    method='random',
    trialList=data.importConditions(practiceConditionsFile) if os.path.exists(practiceConditionsFile) else [],
    name='practiceTrials'
)
thisExp.addLoop(practiceTrials)
practiceSSD = initialSSD

# p_goRTs       = []
# p_numGoOmit   = 0
# p_numGoResp   = 0
# p_numGoTotal  = 0
# p_numStop     = 0
# p_numStopFail = 0

# win.flip()
# core.wait(prepareBlockDur)

trial_num = 0
for trial in practiceTrials:
    trial_num = trial_num + 1
    arrowDirRaw = trial['arrowDirection'].strip().lower()  # 'left' or 'right'
    stopGoRaw   = trial['stopOrGo'].strip().lower()         # 'go' or 'stop'

    # 1) Fixation
    # fixationCross.setAutoDraw(True)
    # win.callOnFlip(log_on_flip("Fix_onset"))
    # win.flip()
    # core.wait(FixationOnTime[trial_num])
    # fixationCross.setAutoDraw(False)
    win.callOnFlip(log_on_flip("Blank_onset"))
    win.flip()
    core.wait(PostTrialWaitTime[trial_num])
    check_for_esc()

    # 2) Show plane and trigger square; if STOP trial, later show fuel cue.
    if arrowDirRaw == 'left':
        planeStim.image = planeLeftPath
    else:
        planeStim.image = planeRightPath

    #------------------------------------------------------
    planeStim.setAutoDraw(True)
    square.setAutoDraw(True)
    fuelStim.setAutoDraw(False)
    #-------------------------------------------------------

    # Clear any leftover key events from the keyboard
    kb.clearEvents()

    clock = core.Clock()
    kb.clock.reset()  # reset the keyboard clock
    win.callOnFlip(log_on_flip("PracticeTrial_onset"))
    win.callOnFlip(clock.reset)
    win.flip()

    responded  = False
    wasCorrect = False
    rt         = None
    shownFuel  = False
    pressed    = None

    # Use a while loop that polls for key responses with an explicit keyList and time stamp.
    while clock.getTime() < maxResponseTime:
        check_for_esc()
        t = clock.getTime()
        # For STOP trials, show fuel cue after SSD delay
        if (stopGoRaw == 'stop') and (not shownFuel) and (t >= practiceSSD):
            fuelStim.setAutoDraw(True)
            win.callOnFlip(log_on_flip("PracticeFuel_onset"))
            win.flip()
            shownFuel = True

        keys = kb.getKeys(keyList=allResp+escapeKey, waitRelease=False)
        if keys:
            thisKey = keys[0]
            key = thisKey.name
            rt = thisKey.rt
            if key in escapeKey:
                thisExp.saveAsWideText(filename+'.csv')
                thisExp.saveAsPickle(filename)
                win.close()
                core.quit()
            else:
                responded = True
                pressed = key
                break
        win.flip()

    planeStim.setAutoDraw(False)
    square.setAutoDraw(False)
    fuelStim.setAutoDraw(False)
    win.flip()

    practiceTrials.addData('SSD_used', practiceSSD if stopGoRaw=='stop' else 0)

    # 3) Determine correctness
    '''
    if stopGoRaw == 'go':
        # p_numGoTotal += 1
        if responded:
            if ((arrowDirRaw == 'left' and pressed in leftKeys) or 
                (arrowDirRaw == 'right' and pressed in rightKeys)):
                wasCorrect = True
            # p_numGoResp += 1
            # p_goRTs.append(rt)
        else:
            # p_numGoOmit += 1
            # p_goRTs.append(maxResponseTime)
    '''
    if stopGoRaw == 'go' and responded:
        if ((arrowDirRaw == 'left' and pressed in leftKeys) or 
            (arrowDirRaw == 'right' and pressed in rightKeys)):
            wasCorrect = True

    elif stopGoRaw == 'stop':#!= 'go':  # Stop condition
        # p_numStop += 1
        if responded and pressed in downKeys:
            wasCorrect = True
            practiceSSD += ssdIncrement
            # The SSD is increased by 50 ms for each stop trial in which the participant correctly stops; 
        else:
            practiceSSD = max(0, practiceSSD - ssdDecrement)
            # the SSD is decreased by 50 ms for each stop trial in which the participant incorrectly "goes"
            # p_numStopFail += 1
        
    # 4) Provide feedback (practice only)
    if wasCorrect:
        fbStim = feedback_correct
    else:
        fbStim = feedback_incorrect if responded else feedback_timeout

    # fbStim.setAutoDraw(True)
    # itidur = random.uniform(*ITIspan)
    # win.callOnFlip(log_on_flip("PracticeITI_onset"))
    # win.flip()
    # core.wait(itidur)
    # fbStim.setAutoDraw(False)
    # win.flip()
    fbStim.setAutoDraw(True)
    win.callOnFlip(log_on_flip("feedback_onset"))
    win.flip()
    core.wait(feedbackDuration)
    fbStim.setAutoDraw(False)
    win.flip() 

    # practiceTrials.addData('FixationOnTime', FixationOnTime[trial_num])
    practiceTrials.addData('PostTrialWaitTime', PostTrialWaitTime[trial_num])
    practiceTrials.addData('arrowDir', arrowDirRaw)
    practiceTrials.addData('stopOrGo', stopGoRaw)
    # practiceTrials.addData('SSD_new', practiceSSD if stopGoRaw=='stop' else 0)
    practiceTrials.addData('response', pressed)
    practiceTrials.addData('rt', rt)
    practiceTrials.addData('correct', wasCorrect)
    practiceTrials.addData('trial_num', trial_num)
    thisExp.nextEntry()


if (p_nReps > 0): #and (p_numGoTotal > 0):
    # meanGo = np.mean(p_goRTs) * 1000
    # pStopFailRate = (p_numStopFail / p_numStop) if (p_numStop > 0) else 0
    summ = (f"Practice done!\n\n"
            # f"Mean GO RT = {meanGo:.1f} ms\n"
            # f"GO omissions = {p_numGoOmit}\n"
            # f"STOP failures = {p_numStopFail} (p={pStopFailRate:.2f})\n\n"
            "Press SPACE to continue.")
    feedbackText.text = summ
    feedbackText.setAutoDraw(True)
    win.flip()
    wait_for_space()
    feedbackText.setAutoDraw(False)
    win.flip()

# -------------------------------------------------------------------------
# --------------------------- MAIN BLOCKS ----------------------------------
# -------------------------------------------------------------------------
if not os.path.exists(mainConditionsFile):
    logging.error(f"Main conditions file {mainConditionsFile} not found! No main blocks.")
    nMainBlocks = 0

mainBlocks = data.TrialHandler(
    nReps=nMainBlocks, 
    method='sequential',
    trialList=[None],
    name='mainBlocks'
)
thisExp.addLoop(mainBlocks)
SSD = initialSSD  # track SSD for main task

blockIdx = 0
for block in mainBlocks:
    blockIdx += 1

    # Optional block instruction
    feedbackText.text = f"Prepare for Block {blockIdx}. Press SPACE to continue."
    feedbackText.setAutoDraw(True)
    win.flip()
    wait_for_space()
    feedbackText.setAutoDraw(False)
    win.flip()
    # core.wait(prepareBlockDur)

    trials = data.TrialHandler(
        nReps=blockReps, 
        method='random',
        trialList=data.importConditions(mainConditionsFile) if os.path.exists(mainConditionsFile) else [],
        name='trialsBlock'
    )
    thisExp.addLoop(trials)

    #---- Block performance accumulators-----
    # b_goRTs       = []
    # b_numGoOmit   = 0
    # b_numGoResp   = 0
    # b_numGoTotal  = 0
    # b_numStop     = 0
    # b_numStopFail = 0
    #----------------------------------------

    for trl in trials:
        trial_num = trial_num + 1
        arrowDirRaw = trl['arrowDirection'].strip().lower()
        stopGoRaw   = trl['stopOrGo'].strip().lower()

        # Fixation
        # fixationCross.setAutoDraw(True)
        # win.callOnFlip(log_on_flip("Fix_onset"))
        # win.flip()
        # core.wait(FixationOnTime[trial_num])
        # fixationCross.setAutoDraw(False)
        win.callOnFlip(log_on_flip("Blank_onset"))
        win.flip()
        core.wait(PostTrialWaitTime[trial_num])
        check_for_esc()

        # Plane and square; display fuel cue for STOP trials after SSD delay
        if arrowDirRaw == 'left':
            planeStim.image = planeLeftPath
        else:
            planeStim.image = planeRightPath

        planeStim.setAutoDraw(True)
        square.setAutoDraw(True)
        fuelStim.setAutoDraw(False)
        #event.clearEvents()
        # Clear any leftover key events from the keyboard
        kb.clearEvents()


        clock = core.Clock()
        kb.clock.reset()  # reset the keyboard clock
        lblStart = f"Block{blockIdx}_Trial_onset"
        win.callOnFlip(log_on_flip(lblStart))
        win.callOnFlip(clock.reset)
        win.flip()

        responded  = False
        wasCorrect = False
        rt         = None
        shownFuel  = False
        pressed    = None

        while clock.getTime() < maxResponseTime:
            check_for_esc()
            t_current = clock.getTime()
            if (stopGoRaw == 'stop') and (not shownFuel) and (t_current >= SSD):
                fuelStim.setAutoDraw(True)
                lblFuel = f"Block{blockIdx}_Fuel_onset"
                win.callOnFlip(log_on_flip(lblFuel))
                win.flip()
                shownFuel = True

            keys = kb.getKeys(keyList=allResp+escapeKey, waitRelease=False)
            if keys:
                thisKey = keys[0]
                key = thisKey.name
                rt = thisKey.rt
                if key in escapeKey:
                    thisExp.saveAsWideText(filename+'.csv')
                    thisExp.saveAsPickle(filename)
                    win.close()
                    core.quit()
                else:
                    responded = True
                    pressed = key
                    break
            win.flip()

        planeStim.setAutoDraw(False)
        square.setAutoDraw(False)
        fuelStim.setAutoDraw(False)
        win.flip()

        trials.addData('SSD_used', SSD if stopGoRaw=='stop' else 0)
    
        # Determine correctness for main trials
        '''
        if stopGoRaw == 'go':
            #b_numGoTotal += 1
            if responded:
                if ((arrowDirRaw == 'left' and pressed in leftKeys) or
                    (arrowDirRaw == 'right' and pressed in rightKeys)):
                    wasCorrect = True
                #b_numGoResp += 1
                #b_goRTs.append(rt)
            #else:
                #b_numGoOmit += 1
                #b_goRTs.append(maxResponseTime)
        '''     
        if stopGoRaw == 'go' and responded:
            if ((arrowDirRaw == 'left' and pressed in leftKeys) or 
                (arrowDirRaw == 'right' and pressed in rightKeys)):
                wasCorrect = True

        elif stopGoRaw == 'stop':#!= 'go':  # Stop condition
            # p_numStop += 1
            if responded and pressed in downKeys:
                wasCorrect = True
                SSD += ssdIncrement
                # The SSD is increased by 50 ms for each stop trial in which the participant correctly stops; 
            else:
                SSD = max(0, SSD - ssdDecrement)
                # the SSD is decreased by 50 ms for each stop trial in which the participant incorrectly "goes"
                # p_numStopFail += 1

        # itidur = random.uniform(*ITIspan)
        # lblITI = f"Block{blockIdx}_ITI_onset"
        # win.callOnFlip(log_on_flip(lblITI))
        # win.flip()
        # core.wait(itidur)
        # win.flip()

        # trials.addData('FixationOnTime', FixationOnTime[trial_num])
        trials.addData('PostTrialWaitTime', PostTrialWaitTime[trial_num])
        trials.addData('arrowDir', arrowDirRaw)
        trials.addData('stopOrGo', stopGoRaw)
        #trials.addData('SSD_new', SSD if stopGoRaw=='stop' else 0)
        trials.addData('response', pressed)
        trials.addData('rt', rt)
        trials.addData('correct', wasCorrect)
        trials.addData('trial_num', trial_num)
        trials.addData('block_num', blockIdx)
        thisExp.nextEntry()

    # -------------------------------------------------------------------------
    # -----------Optionally show feedback here (if desired) ------------------
    # -------------------------------------------------------------------------
    #block_goMean = np.mean(b_goRTs) * 1000 if b_goRTs else 0
    #block_stopFailRate = (b_numStopFail / b_numStop) if b_numStop > 0 else 0
    # blockMsg = (f"Block {blockIdx} finished!\n\n"
    #             f"Mean GO RT: {block_goMean:.1f} ms\n"
    #             f"GO omissions: {b_numGoOmit}\n"
    #             f"STOP failures: {b_numStopFail} (p={block_stopFailRate:.2f})\n\n"
    #             "Press SPACE to continue.")
    blockMsg = (f"Block {blockIdx} finished!\n\n"
                "Press SPACE to continue.")
    feedbackText.text = blockMsg
    feedbackText.setAutoDraw(True)
    win.flip()
    wait_for_space()
    feedbackText.setAutoDraw(False)
    win.flip()

# -------------------------------------------------------------------------
# --------------------------- DONE -----------------------------------------
# -------------------------------------------------------------------------
doneText.draw()
win.flip()
event.waitKeys()

thisExp.saveAsWideText(filename+'.csv')
thisExp.saveAsPickle(filename)
win.close()
core.quit()
