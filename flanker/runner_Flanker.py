# Auhtor: Neda Kaboodvand, neda.neuroscience@gmail.com

from datetime import datetime
import os  # handy system and path functions
import sys  # to get file system encoding
import numpy as np
import random
from psychopy import visual, core, event, data, gui, logging

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
_thisDir = os.path.dirname(os.path.abspath(__file__)) #os.path.dirname(__file__)
os.chdir(_thisDir)# Now, the current working directory is the same as the script's directory,and you can access files and directories relative to this location.
try:
    from PIL import Image
except ImportError:
    import Image

psychopyVersion = '2022.2.5'
scriptname = os.path.basename(__file__)
expName = scriptname.split('_')[0] 
expInfo = {
    'participant': f"{random.randint(0, 999999):06.0f}",#'participant': f"{randint(0, 999999):06.0f}",
    'session': '001',
    'doPractice': True,
}

dlg = gui.DlgFromDict(dictionary=expInfo, sortKeys=False, title=expName)
if dlg.OK == False:
    core.quit()

expInfo['date'] = datetime.now().strftime('%Y-%m-%d_%H%M%S.%f')
expInfo['expName'] = expName
expInfo['psychopyVersion'] = psychopyVersion
corTime = core.getTime() 
expInfo['coreTime'] =  datetime.fromtimestamp(corTime).strftime('%Y-%m-%d_%H%M%S.%f')

filename = _thisDir + os.sep + u'data/%s_%s_%s' % (expInfo['participant'], expName, expInfo['date'])
logFile = logging.LogFile(filename+'.log', level=logging.INFO)

data_dir = "data"
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

if not expInfo['doPractice']:
    logging.exp('Skipping practice')
    practice_len = 0

thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    savePickle=True, saveWideText=True,
    dataFileName=filename)

leftResponseKeys = ['left', '1', 'num_1']
rightResponseKeys = ['right', '2', 'num_2']
escapeKey = ['escape']
allKeys = leftResponseKeys + rightResponseKeys + escapeKey

test_stimuli = [
    {'image': 'images/rrlrr.png', 'correct_response': leftResponseKeys, 'condition': 'incongruent', 'trial_id': 'stim'},
    {'image': 'images/llrll.png', 'correct_response': rightResponseKeys, 'condition': 'incongruent', 'trial_id': 'stim'},
    {'image': 'images/lllll.png', 'correct_response': leftResponseKeys, 'condition': 'congruent', 'trial_id': 'stim'},
    {'image': 'images/rrrrr.png', 'correct_response': rightResponseKeys, 'condition': 'congruent', 'trial_id': 'stim'}
]
correct_responses = {'images/rrlrr.png': 'left', 'images/llrll.png': 'right', 'images/lllll.png': 'left', 'images/rrrrr.png': 'right'}

StimuliPool =  ['images/rrlrr.png', 'images/llrll.png', 'images/lllll.png', 'images/rrrrr.png']
# -------------------------------------------------------------------------
# imgSize = (0.1, 0.1) # 10 % of screen height
desired_height   = 0.05          # 10 % of screen height
orig_w, orig_h   = Image.open('images/lllll.png').size
aspect           = orig_w / orig_h
imgSize     = (desired_height * aspect, desired_height)
# -------------------------------------------------------------------------
attention_check_thresh = 0.65
maxResponseTime = 1 # update on 4/22/2025: 2.0 decreased to 0.7
FeedbackOnTime = 0.5 
practice_len = 5
num_blocks = 3
num_trials = 20
exp_len = 60
# -------------------------------------------------------------------------
#update on 4/22/2025: VB suggested Removing fixation, increasing blank screen duration to the mean of 3.5 sec.
# FixationOnTime = [random.uniform(1.5, 2.5) for _ in range(exp_len + practice_len )]
# PostTrialWaitTime = 0.5
# -------------------------------------------------------------------------
PostTrialWaitTime = [random.uniform(3, 4) for _ in range(exp_len + practice_len )]
# -------------------------------------------------------------------------

within_block_trial = 1
current_block = 0
new_block = 0
stims = []
correct_response = ""
# -------------------------------------------------------------------------
def check_for_escape():
    if 'escape' in event.getKeys():
        thisExp.saveAsWideText(filename+'.csv', delim='auto')
        thisExp.saveAsPickle(filename)
        win.close()
        core.quit()
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
win.mouseVisible = False
# -------------------------------------------------------------------------
preloadedImages = {}
for stimulus in test_stimuli:
    image_path = stimulus['image']
    if os.path.exists(image_path):
        try:
            preloadedImages[image_path] = Image.open(image_path)
            logging.exp(f'Preloaded image {image_path}')
        except Exception as e:
            logging.exp(f'Failed to preload image {image_path}: {e}')
    else:
        logging.exp(f'Image path {image_path} does not exist')
del image_path
# -------------------------------------------------------------------------
practice_nReps = (practice_len // len(test_stimuli)) + 1
practice_stimuli_with_reps = test_stimuli * practice_nReps
random.shuffle(practice_stimuli_with_reps)
practice_stimuli_with_reps = practice_stimuli_with_reps[:practice_len]
practice_trials = data.TrialHandler(practice_stimuli_with_reps, 1, method='sequential')

test_nReps = (exp_len // len(test_stimuli)) + 1
test_stimuli_with_reps = test_stimuli * test_nReps
random.shuffle(test_stimuli_with_reps)

block1_trials = test_stimuli_with_reps[:20]
block2_trials = test_stimuli_with_reps[20:40]
block3_trials = test_stimuli_with_reps[40:60]
block1 = data.TrialHandler(trialList=block1_trials, nReps=1, method='sequential')
block2 = data.TrialHandler(trialList=block2_trials, nReps=1, method='sequential')
block3 = data.TrialHandler(trialList=block3_trials, nReps=1, method='sequential')

thisExp.addLoop(practice_trials) 
thisExp.addLoop(block1)
thisExp.addLoop(block2)
thisExp.addLoop(block3)

# trial_image = visual.ImageStim(
#     win=win,
#     name='trial_image', 
#     image='sin', mask=None, anchor='center',
#     ori=0.0, pos=(0, 0), 
#     color=[1,1,1], colorSpace='rgb', opacity=None,
#     flipHoriz=False, flipVert=False,
#     texRes=128.0, interpolate=True, depth=-1.0)
trial_image = visual.ImageStim(
    win=win,
    name='trial_image',
    image='sin',
    size=imgSize,          # <-- keeps aspect ratio
    anchor='center',
    ori=0.0, pos=(0, 0),
    color=[1,1,1], colorSpace='rgb', interpolate=True, units='height')

square_size = 0.1 
square_position = (0.8 - square_size / 2, -0.5 + square_size / 2)
square = visual.Rect(
    win=win,
    width=square_size, 
    height=square_size, 
    fillColor='white',
    lineColor=None,
    pos=square_position
)

correct_feedback = visual.TextStim(win=win, name='feedback_text',
    text='Correct!',color='green',
    font='Open Sans',
    pos=(0, 0), height=0.05, wrapWidth=None, ori=0.0, 
    colorSpace='rgb', opacity=1.0, 
    languageStyle='LTR',
    depth=-4.0)

incorrect_feedback = visual.TextStim(win=win, name='feedback_text',
    text='Incorrect',color='red',
    font='Open Sans',
    pos=(0, 0), height=0.05, wrapWidth=None, ori=0.0, 
    colorSpace='rgb', opacity=1.0, 
    languageStyle='LTR',
    depth=-4.0)

timeout_feedback = visual.TextStim(win=win, name='feedback_text',
    text='Respond faster!',
    font='Open Sans',
    pos=(0, 0), height=0.05, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=1.0, 
    languageStyle='LTR',
    depth=-4.0)

TextHeight = 0.05#0.035
text_instr = visual.TextStim(win=win, name='text_instr',
    text='',
    font='Open Sans',
    pos=(0, 0), height=TextHeight, wrapWidth=None, ori=0.0, #wrapWidth=1.4
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-1.0)

text_end = visual.TextStim(win=win, #name='text_instr',
    text='Thanks for completing the task! \n Press any key to exit.',
    font='Open Sans',
    pos=(0, 0), height=TextHeight, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-1.0)

fixation = visual.TextStim(win, text='+', color='white')

def run_trials(trials, stage):

    doShowTextFeedback = True
    if stage == 'test':
        doShowTextFeedback = False
        correct_feedback.setOpacity(doShowTextFeedback)
        incorrect_feedback.setOpacity(doShowTextFeedback)

    for trial_num, trial in enumerate(trials):

        correct_response0 = correct_responses[trial['image']]
        preloaded_image = preloadedImages.get(trial['image'])
        trial_image.image = preloaded_image

        trial_image.draw() 
        square.draw()  
        win.callOnFlip(trialClock.reset)
        win.callOnFlip(lambda: thisExp.addData('stimulus_onset_blockClock', blockClock.getTime()))
        win.callOnFlip(lambda: thisExp.addData('stimulus_onset_coreTime', core.getTime()))
        win.callOnFlip(lambda: thisExp.addData('stimulus_onset_time', datetime.now().strftime('%Y-%m-%d_%H:%M:%S.%f')))
        win.flip()      
        keys  = event.waitKeys(maxWait=maxResponseTime, keyList=allKeys, timeStamped=trialClock, clearEvents=True) #clearEvents=True was added on 4/22/2025

        if keys:
            response, timestamp = keys[0]
            if 'escape' in keys:
                thisExp.saveAsWideText(filename+'.csv', delim='auto')
                thisExp.saveAsPickle(filename)
                win.close()
                core.quit()
            correct = response in trial['correct_response']
            feedback = correct_feedback if correct else incorrect_feedback     
        else:
            response = None
            timestamp = None
            correct = False
            feedback = timeout_feedback
        if doShowTextFeedback: # practice only
            feedback.draw()
            win.flip()
            core.wait(FeedbackOnTime) 
        # fixation.draw()

        win.callOnFlip(lambda: thisExp.addData('ITI_onset_trialClock', trialClock.getTime()))
        win.callOnFlip(lambda: thisExp.addData('ITI_onset_blockClock', blockClock.getTime()))
        win.callOnFlip(lambda: thisExp.addData('ITI_onset_coreTime', core.getTime()))
        win.callOnFlip(lambda: thisExp.addData('ITI_onset_time', datetime.now().strftime('%Y-%m-%d_%H:%M:%S.%f')))
        # win.flip()
        # core.wait(FixationOnTime[trial_num])
        # check_for_escape()  
        win.flip() 
        core.wait(PostTrialWaitTime[trial_num])#core.wait(PostTrialWaitTime)
        check_for_escape() 
        trials.addData('stimulus', trial['image'])
        trials.addData('stage', stage)
        thisExp.addData('participant', expInfo['participant'])
        thisExp.addData('session', expInfo['session'])
        thisExp.addData('trial_num', trial_num)
        thisExp.addData('stage', stage)
        thisExp.addData('stimulus', trial['image'])
        thisExp.addData('condition', trial['condition'])
        thisExp.addData('correct_response', trial['correct_response'])
        thisExp.addData('correct_response0', correct_response0)
        thisExp.addData('response', response)
        thisExp.addData('correct', correct) 
        thisExp.addData('RT', timestamp)
        # thisExp.addData('FixationOnTime', FixationOnTime[trial_num])
        thisExp.addData('PostTrialWaitTime', PostTrialWaitTime[trial_num])
        thisExp.nextEntry()

#--------------------------------------------------------------------------------------------------------------
def show_text_with_blink(text, blink_count, blink_duration=0.2, inter_blink_interval=0.2):
    """
    Displays the provided text (using text_instr) while overlaying a blinking square.
    The square will blink for a total duration determined by blink_count cycles.
    The routine runs continuously until the participant presses 'return'.
    """
    total_duration = blink_count * (blink_duration + inter_blink_interval)
    # Use a separate clock for the blinking routine.
    clock = core.Clock()
    # Clear any previous key events
    event.clearEvents()
    while True:
        # Draw the instruction text.
        text_instr.setText(text)
        text_instr.draw()
        
        # Determine whether to draw the square (blink effect).
        t = clock.getTime()
        if t < total_duration:
            cycle = blink_duration + inter_blink_interval
            # During the "on" phase of the blink cycle, draw the square.
            if (t % cycle) < blink_duration:
                square.draw()
        
        win.flip()
        
        # Check if the participant pressed 'return'
        keys = event.getKeys(keyList=['return'])
        if keys:
            break

text_instr.setText("You'll see five fish in a row. Your goal is to identify the direction of the middle fish.\n\n Press Enter to continue.")
# text_instr.setText("You will see five fish in a row, some facing left, some right.\n Your task is to identify the direction of the middle fish by pressing the corresponding key.\n\n Press Enter to continue.")
text_instr.draw()
win.flip()
event.waitKeys()


# show_text_with_blink("You will see five fish in a row, some facing left, some right.\n Your task is to identify the direction of the middle fish by pressing the corresponding key.\n\n Press Enter to continue.", blink_count=4)
show_text_with_blink("Press the key that matches the middle fish’s direction. Ignore the other fish.\n\n Press Enter to continue.", blink_count=4)
#---------------------------------------------------------------------------------------------------------------
# text_instr.setText("You will see five fish in a row, some facing left, some right.\n Your task is to identify the direction of the middle fish by pressing the corresponding key.\n\n Press Enter to continue.")
# text_instr.draw()
# win.flip()
# event.waitKeys()
#---------------------------------------------------------------------------------------------------------------

def get_instruction_text(block_num, num_blocks):
    if block_num == 1:
        return f'block {block_num} of {num_blocks}\n\nPress Enter to begin.'
    elif block_num == 2:
        return f'block {block_num} of {num_blocks}\n\nPress Enter to begin.'
    elif block_num == 3:
        return f'block {block_num} of {num_blocks}\n\nPress Enter to begin.'

globalClock = core.Clock()
blockClock = core.Clock()
trialClock = core.Clock() 

if expInfo['doPractice']:

    #show_text_with_blink("Let\'s practice. \n During practice you\'ll see if you are correct or incorrect after responding. \n After practice we\'ll go again but without the correct / incorrect feedback.\n\nPress enter to begin.", blink_count=4)
    text_instr.setText('Let\'s practice. \n During practice you\'ll see if you are correct or incorrect after responding. \n After practice we\'ll go again but without the feedback.\n\nPress enter to begin.')
    text_instr.draw()

    win.callOnFlip(globalClock.reset)
    win.callOnFlip(lambda: thisExp.addData('Practice_InstrStart_globalClock', globalClock.getTime()))
    win.callOnFlip(lambda: thisExp.addData('Practice_InstrStart_coreTime', core.getTime()))
    win.callOnFlip(lambda: thisExp.addData('Practice_InstrStart_time', datetime.now().strftime('%Y-%m-%d_%H:%M:%S.%f')))
    win.flip()
    keys  = event.waitKeys(keyList=['return'], timeStamped=globalClock)
    timestamp = keys[0][1]
    thisExp.addData('PracticeStartRT', timestamp)
    thisExp.nextEntry()

    run_trials(practice_trials, 'practice')
    check_for_escape()
    text_instr.setText('Practice over. The test begins now.\n\nPress enter to start.')
    text_instr.draw()
    win.callOnFlip(blockClock.reset)
    win.callOnFlip(lambda: thisExp.addData('Test_InstrStart_globalClock', globalClock.getTime()))
    win.callOnFlip(lambda: thisExp.addData('Test_InstrStart_blockClock', blockClock.getTime())) 
    win.callOnFlip(lambda: thisExp.addData('Test_InstrStart_coreTime', core.getTime()))
    win.callOnFlip(lambda: thisExp.addData('Test_InstrStart_time', datetime.now().strftime('%Y-%m-%d_%H:%M:%S.%f')))
    win.flip()
    keys  = event.waitKeys(keyList=['return'], timeStamped=blockClock, clearEvents=True)
    timestamp = keys[0][1]
    thisExp.addData('TestStartRT', timestamp)
    thisExp.nextEntry()

for block_trials in [block1, block2, block3]:
    current_block += 1
    event.clearEvents()
    win.flip()
    block_text = get_instruction_text(current_block, num_blocks)
    text_instr.setText(block_text)
    text_instr.draw()
    win.callOnFlip(blockClock.reset)
    win.callOnFlip(lambda: thisExp.addData('TestBlock_InstrStart_globalClock', globalClock.getTime()))
    win.callOnFlip(lambda: thisExp.addData('TestBlock_InstrStart_blockClock', blockClock.getTime()))
    win.callOnFlip(lambda: thisExp.addData('TestBlock_InstrStart_coreTime', core.getTime()))
    win.callOnFlip(lambda: thisExp.addData('TestBlock_InstrStart_time', datetime.now().strftime('%Y-%m-%d_%H:%M:%S.%f')))
    win.flip()
    keys  = event.waitKeys(keyList=['return'], timeStamped=blockClock)
    timestamp = keys[0][1]
    thisExp.addData('TestBlockStartRT', timestamp)
    thisExp.addData('current_block', current_block)
    thisExp.nextEntry()
    check_for_escape()
    run_trials(block_trials, 'test')
    win.flip() 
    event.clearEvents()
  
text_end.draw()
win.flip()
event.waitKeys()
check_for_escape()

thisExp.saveAsWideText(filename+'.csv', delim='auto')
thisExp.saveAsPickle(filename)
thisExp.abort()

win.close()
core.quit()