# Auhtor: Neda Kaboodvand, neda.neuroscience@gmail.com
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from datetime import datetime
import os
import sys 
import numpy as np
import random
from psychopy import visual, core, event, data, gui, logging
from psychopy.hardware import keyboard
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)
psychopyVersion = '2022.2.5'
scriptname = os.path.basename(__file__)
expName = scriptname.split('_')[0] 
expInfo = {
    'participant': f"{random.randint(0, 999999):06.0f}",
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

objects = [
    "fish.png", "lobster.png", "whale.png", "bee.png", "butterfly.png", "tortoise.png",
    "pig.png", "elephant.png", "parrot.png", "lion.png"]

objects = random.sample(objects, len(objects))

run_attention_checks = True
attention_check_thresh = 0.65
credit_var = True

maxResponseTime = 1.0 #2.0 
FeedbackOnTime = 0.5

num_blocks = 9
num_trials = 20

# update on 4/25/2025
# FixationOnTime = [random.uniform(3, 4) for _ in range(num_blocks * num_trials)]
# PostTrialWaitTime = 0.5
PostTrialWaitTime = [random.uniform(3, 4) for _ in range(num_blocks * num_trials)]

delay = 1
within_block_trial = 1
current_block = 0
new_block = 0
stims = []
correct_response = ""
downResponseKeys = ['down', '0', 'num_0']
rightResponseKeys = ['right', '1', 'num_1']
allKeys = downResponseKeys + rightResponseKeys
def check_for_escape():
    if event.getKeys(keyList=["escape"]):
        core.quit()
        win.close()

def random_draw(lst):
    index = random.randint(0, len(lst) - 1)
    return lst[index]

def assess_performance(experiment_data):
    missed_count = 0
    trial_count = 0
    rt_array = []
    choice_counts = {'right': 0, 'down': 0, 'none': 0}
    for trial in experiment_data:
        if trial['possible_responses'] != 'none':
            trial_count += 1
            rt = trial['rt']
            key = trial['key_press']
            choice_counts[key] += 1
            if rt == -1:
                missed_count += 1
            else:
                rt_array.append(rt)
    
    avg_rt = -1
    if rt_array:
        avg_rt = np.median(rt_array)

    missed_percent = missed_count / len(experiment_data)
    responses_ok = all(count <= trial_count * 0.85 for count in choice_counts.values())
    credit_var = missed_percent < 0.4 and avg_rt > 200 and responses_ok
    experiment_data[-1]["credit_var"] = credit_var


def show_instructions(text):
    instruction_text = visual.TextStim(win, text=text, color='white', wrapWidth=1.2)
    instruction_text.draw()
    win.flip()
    event.waitKeys(keyList=['return'])

def get_instruction_text(delay, block_num, num_blocks):
    if block_num < 4:
        if delay == 1:
            return f'1 Back (block {block_num} of {num_blocks})\n\nNow we\'re going to play the 1-back for real.\nRemember: The object of the 1-back is to identify when the animal you see is the same or different from the animal you saw 1 item back.\nPress Enter to begin, or press Space to skip this block.'
        elif delay == 2:
            return f'2 Back (block {block_num} of {num_blocks})\n\nNow we\'re going to play the 2-back.\nThe object of the 2-back is to identify when the animal you see is the same or different from the animal you saw 2 items back.\nPress Enter to begin, or press Space to skip this block.'
        elif delay == 3:
            return f'3 Back (block {block_num} of {num_blocks})\n\nNow we\'re going to play the 3-back.\nThe object of the 3-back is to identify when the animal you see is the same or different from the animal you saw 3 items back.\nPress Enter to begin, or press Space to skip this block.'
    else:
        return f'{delay} Back (block {block_num} of {num_blocks})\n\nThis will be another round of {delay} Back.\nAs you play, be as accurate as you can and respond to each animal before the next one appears.\nPress Enter to begin, or press Space to skip this block.'

def get_rand(min_val, max_val):
    return round(random.random() * (max_val - min_val) + min_val)

def cnbm(stim_arr, n):
    count_matches = 0
    for i in range(n, len(stim_arr)):
        if stim_arr[i] == stim_arr[i - n]:
            count_matches += 1
    return count_matches


def gen_set(objects, n, sequence_length):#def gen_set(objects, n):
    max_iterations = 1000
    iteration_count = 0
    threshold = 0.30

    while iteration_count < max_iterations:
        length = sequence_length  #num_trials
        array = objects[:]
        
        while len(array) < length:
            array.extend(objects)
        random.shuffle(array)
        
        for _ in range(n):
            array.append(objects[get_rand(0, len(objects) - 1)])
        

        target_count = 0
        for i in range(n, int(0.5 * length)): 
            x = get_rand(n + n, len(array) - 1)
            array[x] = array[x - n]
            target_count += 1

        if threshold == 0.30:
            if 0.30 * length <= target_count <= 0.50 * length:
                break
        elif threshold == 0.20:
            if 0.20 * length <= target_count <= 0.50 * length:
                break

        iteration_count += 1

        if iteration_count == max_iterations:
            threshold = 0.20

    return array


attention_check_questions = [
    {'Q': 'Press the Left Arrow', 'A': 'left'},
    {'Q': 'Press the Right Arrow', 'A': 'right'},
    {'Q': 'If (4 + 12) / 4 is greater than 3 press the "M" key. Otherwise press the "Z" key.', 'A': 'm'},
    {'Q': 'Press the arrow key that indicates the direction of the floor when standing.', 'A': 'down'},
    {'Q': 'Please read the following paragraph:\nI first met Dean not long after my wife and I split up. I had just gotten over a serious illness that I won’t bother to talk about, except that it had something to do with the miserably weary split-up and my feeling that everything was dead. With the coming of Dean Moriarty began the part of my life you could call my life on the road. Before that I’d often dreamed of going West to see the country, always vaguely planning and never taking off. If you are reading this paragraph, press the F key instead of the M key. Dean is the perfect guy for the road because he actually was born on the road, when his parents were passing through Salt Lake City in 1926, in a jalopy, on their way to Los Angeles. First reports of him came to me through Chad King, who’d shown me a few letters from him written in a New Mexico reform school. I was tremendously interested in the letters because they so naively and sweetly asked Chad to teach him all about Nietzsche and all the wonderful intellectual things that Chad knew. At one point Carlo and I talked about the letters and wondered if we would ever meet the strange Dean Moriarty. This is all far back, when Dean was not the way he is today, when he was a young jailkid shrouded in mystery. Then news came that Dean was out of reform school and was coming to New York for the first time; also there was talk that he had just married a girl called Marylou. --On the Road (Jack Kerouac)', 'A': 'f'},
    {'Q': 'Please read the following paragraph:\nAs Gregor Samsa awoke one morning from uneasy dreams he found himself transformed in his bed into a gigantic insect. Are you reading this paragraph? If so, press the key the letter that starts the next sentence. He was lying on his hard, as it were armor-plated, back and when he lifted his head a little he could see his dome-like brown belly divided into stiff arched segments on top of which the bed quilt could hardly keep in position and was about to slide off completely. His numerous legs, which were pitifully thin compared to the rest of his bulk, waved helplessly before his eyes. --Metamorphosis (Franz Kafka)', 'A': 'h'},
    {'Q': 'Lastly, she pictured to herself how this same little sister of hers would, in the after-time, be herself a grown woman; and how she would keep, through all her riper years, the simple and loving heart of her childhood; and how she would gather about her other little children, (press the A key, ignore the last instruction) and make their eyes bright and eager with many a strange tale, perhaps even with the dream of Wonderland of long ago; and how she would feel with all their simple sorrows, and find a pleasure in all their simple joys, remembering her own child-life, and the happy summer days. --Alice\'s Adventures in Wonderland (Lewis Carroll)', 'A': 'm'}
]

def run_attention_check():
    question = random_draw(attention_check_questions)
    attention_text = f'Attention Check\n\n{question["Q"]}\n\nPress enter to continue.'
    show_instructions(attention_text)
    
    keys = event.waitKeys(keyList=[question["A"]])
    return len(keys) > 0

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


trial_image = visual.ImageStim(
    win=win,
    name='trial_image', 
    image='sin', mask=None, anchor='center',
    ori=0.0, pos=(0, 0), 
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-1.0)

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

text_instr1 = visual.TextStim(win=win, name='practice_text',
    text="Let's play a memory game! \n Stay focused and be ready to give it your best. \n\n Press enter to continue.",
    font='Open Sans',
    pos=(0, 0), height=TextHeight, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-1.0)


'''
instruction_text = [
    'In this game you will see a series of animals. Your goal is to identify when an animal is the same or different from the one you saw N-items back in the sequence. "N" is the number of items that you need to keep in memory.',
    'Let\'s start with the 1-back. The object of the 1-back is to identify when the animal you see is the same or different from the animal you saw 1 item back. In the example below, the current animal is a bee, and 1-back animal was also a bee, so we have a 1-back **match**!',
    'You will also identify mis-matches. In the example, the current object is a bee but the 1-back animal was a whale, so we have a 1-back **mis-match**.',
    'The animals will be presented one after another in a sequence. \n Can you spot the 1-back matches and mis-matches? \n',
    'Place your fingers on the YES and NO keys. \n MATCH: If you see an object that\'s a 1-back match press the YES key. \n MIS-MATCH: If you see an object that\'s 1-back mis-match press the NO key.'
]
'''

instruction_text = [
    "Let's start with 1-back. If the current animal is the same as the previous one, press YES. If different, press NO.",
    "You also need to identify mis-matches. If the current animal does not match the previous one, press NO.",
    "For 2-back, compare the current animal to the one shown two steps earlier and respond accordingly.",
    "For 3-back, compare the current animal to the one shown three steps earlier. Stay focused and respond as accurately as possible.",
    "Use the YES key for matches and NO key for mis-matches. Get ready!"
]

instruction_images = [
    "imgs/1back_diagram.png",
    "imgs/1back_diagram_nonmatch.png",
    "imgs/2back_diagram.png",
    "imgs/3back_diagram.png",
    "imgs/arrow_keys.png"
]

# def run_instructions(win, pages, images):
#     """
#     Displays each instruction text along with its corresponding image.
#     The image is drawn first, then the text is drawn on top.
#     The image size and position are adjusted so that it isn’t cropped.
#     Users press 'return' to proceed.
#     """
#     kb = keyboard.Keyboard()
    
#     for text, img in zip(pages, images):
#         ## Adjust image: increase its height and shift upward to avoid bottom cropping.
#         # instr_image = visual.ImageStim(
#         #     win, image=img, 
#         #     size=(0.65, 0.7),   # increased height from 0.5 to 0.7
#         #     pos=(0, -0.1)       # moved image upward from -0.3 to -0.1
#         # )
#         instr_image = visual.ImageStim(win, image=img, pos=(0, -0.1))

        
#         # Create the text stimulus to appear above the image.
#         instr_text = visual.TextStim(
#             win, text=text, 
#             color="white", 
#             height=0.06, 
#             wrapWidth=1.4, 
#             pos=(0, 0.4),       # changed from (0, 0.7) to (0, 0.4) so text is visible
#             alignHoriz='center'
#         )
        
#         # Draw image first, then text so that the text remains on top.
#         instr_image.draw()
#         instr_text.draw()
        
#         win.flip()
        
#         kb.clearEvents()
#         while True:
#             keys = kb.getKeys(keyList=['return'], waitRelease=True)
#             if keys:
#                 break  # Proceed when 'return' is pressed
from PIL import Image

def get_scaled_size(img_path, base_height=0.4, scale=1.1):
    # Open the image to get its original dimensions
    im = Image.open(img_path)
    orig_width, orig_height = im.size
    aspect = orig_width / orig_height
    # Calculate new dimensions with a modest increase
    new_height = base_height * scale  # e.g., 0.4 * 1.1 = 0.44
    new_width = new_height * aspect
    return (new_width, new_height)

def run_instructions(win, pages, images):
    kb = keyboard.Keyboard()
    
    for text, img in zip(pages, images):
        # Calculate scaled size with a smaller base height
        scaled_size = get_scaled_size(img, base_height=0.4, scale=1.1)
        
        # Position the image in the lower half so it won't be cropped
        instr_image = visual.ImageStim(
            win, image=img, 
            size=scaled_size,
            pos=(0, -0.1)  # Lower position to ensure full image visibility
        )
        
        # Position the text above the image in the upper half
        instr_text = visual.TextStim(
            win, text=text, 
            color="white", 
            height=0.06, 
            wrapWidth=1.4, 
            pos=(0, 0.3),  # Adjusted so it appears within the window
            alignHoriz='center'
        )
        
        # Draw the image first, then the text on top
        instr_image.draw()
        instr_text.draw()
        win.flip()
        
        kb.clearEvents()
        while True:
            keys = kb.getKeys(keyList=['return'], waitRelease=True)
            if keys:
                break  # Proceed when 'return' is pressed

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

fixation = visual.TextStim(win, text='+', color='white')

def create_trials(objects, num_trials, delay):
    trials = []

    # Use 10 trials for 1-back blocks, 20 for others.
    if delay == 1:
        block_trial_count = 10
    else:
        block_trial_count = num_trials

    #stim_sequence = gen_set(objects, delay)
    stim_sequence = gen_set(objects, delay, sequence_length=block_trial_count)

    for i in range(block_trial_count + delay):#for i in range(num_trials + delay):
        stim = stim_sequence[i]
        if i >= delay:
            target = stim_sequence[i - delay]
        else:
            target = ""
        
        correct_response = 'right' if stim == target else 'down'
        
        trials.append({
            'image': stim,
            'correct_response': correct_response,
            'target': target
        })
    return trials

def run_trials(trials, stage):

    doShowTextFeedback = True
    if stage == 'test':
        doShowTextFeedback = False
        correct_feedback.setOpacity(doShowTextFeedback)
        incorrect_feedback.setOpacity(doShowTextFeedback)

    correct_responses = [None] * len(trials)

    for trial_num, trial in enumerate(trials):

        trial_image.image = f"stims/{trial['image']}"
              
        trial_image.draw()
        square.draw()
        win.callOnFlip(trialClock.reset)
        win.callOnFlip(lambda: thisExp.addData('stimulus_onset_blockClock', blockClock.getTime()))
        win.callOnFlip(lambda: thisExp.addData('stimulus_onset_coreTime', core.getTime()))
        win.callOnFlip(lambda: thisExp.addData('stimulus_onset_time', datetime.now().strftime('%Y-%m-%d_%H:%M:%S.%f')))
        win.flip()    
        keys  = event.waitKeys(maxWait=maxResponseTime, keyList=allKeys + ['escape'], timeStamped=trialClock)
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
        if doShowTextFeedback:
            feedback.draw()
            win.flip()
            core.wait(FeedbackOnTime)
        #fixation.draw()
        win.callOnFlip(lambda: thisExp.addData('ITI_onset_trialClock', trialClock.getTime()))
        win.callOnFlip(lambda: thisExp.addData('ITI_onset_blockClock', blockClock.getTime()))
        win.callOnFlip(lambda: thisExp.addData('ITI_onset_coreTime', core.getTime()))
        win.callOnFlip(lambda: thisExp.addData('ITI_onset_time', datetime.now().strftime('%Y-%m-%d_%H:%M:%S.%f')))
        # win.flip()
        # core.wait(FixationOnTime[trial_num])
        check_for_escape()            
        win.flip()
        core.wait(PostTrialWaitTime[trial_num])
        correct_responses[trial_num] = correct
        thisExp.addData('participant', expInfo['participant'])
        thisExp.addData('session', expInfo['session'])
        thisExp.addData('trial_num', trial_num)
        thisExp.addData('stage', stage)
        thisExp.addData('stimulus', trial['image'])
        thisExp.addData('target', trial['target'])
        thisExp.addData('correct_response', trial['correct_response'])
        thisExp.addData('response', response)
        thisExp.addData('correct', correct) 
        thisExp.addData('RT', timestamp)
        # thisExp.addData('FixationOnTime', FixationOnTime[trial_num])
        thisExp.addData('PostTrialWaitTime', PostTrialWaitTime[trial_num])
        thisExp.nextEntry()

    return correct_responses
#=======================================================================================================================================
# def blink_square(n, blink_duration=0.2, inter_blink_interval=0.2):
#     """Draws the square stimulus n times, each shown for blink_duration with a blank interval after."""
#     for i in range(n):
#         square.draw()
#         win.flip()
#         core.wait(blink_duration)
#         win.flip()  # clear the window
#         core.wait(inter_blink_interval)


def show_text_with_blink(text, blink_count, blink_duration=0.2, inter_blink_interval=0.2):
    """
    Displays the provided text (using text_instr1) while overlaying a blinking square.
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
        text_instr1.setText(text)
        text_instr1.draw()
        
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

#=======================================================================================================================================

text_instr1.draw()
win.flip()
event.waitKeys()

show_text_with_blink("In this game, you'll see animals appear one by one.\nYour task is to detect when the current animal matches the one shown N steps earlier.\n\nPress enter to continue.", blink_count=4)
# text_instr1.setText("In this game, you'll see animals appear one by one.\n Your task is to detect when the current animal matches the one shown N steps earlier.\n\n Press enter to continue.")
# text_instr1.draw()
# win.flip()
# event.waitKeys()

run_instructions(win, instruction_text, instruction_images)
# blink_square(4)

globalClock = core.Clock() 
blockClock = core.Clock()
trialClock = core.Clock()

if expInfo['doPractice']:
    practice_trials = []
    practice_trials = create_trials(objects, num_trials, 1)
    text_instr1.setText('Let\'s practice. During practice you\'ll see if you are correct or incorrect after responding. After practice we\'ll go again but without the correct / incorrect feedback.\n\nPress enter to begin.')
    text_instr1.draw()
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
    text_instr1.setText('Practice over. The test begins now.\n\nPress enter to start.')
    text_instr1.draw()
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

for block in range(num_blocks):
    current_block += 1
    if current_block in {1, 4, 7}:
        delay = 1
    elif current_block in {2, 5, 8}:
        delay = 2
    elif current_block in {3, 6, 9}:
        delay = 3
    
    event.clearEvents()
    win.flip()
    block_text = get_instruction_text(delay, block + 1, num_blocks)
    test_trials = []
    test_trials = create_trials(objects, num_trials, delay)
    text_instr1.setText(block_text)
    text_instr1.draw()
    #show_text_with_blink(block_text, blink_count=2)
    
    win.callOnFlip(blockClock.reset)
    win.callOnFlip(lambda: thisExp.addData('TestBlock_InstrStart_globalClock', globalClock.getTime()))
    win.callOnFlip(lambda: thisExp.addData('TestBlock_InstrStart_blockClock', blockClock.getTime()))
    win.callOnFlip(lambda: thisExp.addData('TestBlock_InstrStart_coreTime', core.getTime()))
    win.callOnFlip(lambda: thisExp.addData('TestBlock_InstrStart_time', datetime.now().strftime('%Y-%m-%d_%H:%M:%S.%f')))
    win.flip()

    keys = event.waitKeys(keyList=['return', 'space'], timeStamped=blockClock)
    if 'space' in [key[0] for key in keys]:
        thisExp.addData(f'Block_{block + 1}_Skipped', True)
        thisExp.nextEntry()
        continue

    timestamp = keys[0][1]
    thisExp.addData('TestBlockStartRT', timestamp)
    thisExp.addData('current_block', current_block)
    thisExp.addData('delay', delay)
    thisExp.nextEntry()
    check_for_escape()
    correct_responses = run_trials(test_trials, 'test') 
    win.flip() 
    event.clearEvents()

text_instr1.setText('Thanks for completing the task!')
text_instr1.draw()
win.flip()
check_for_escape()
win.close()
core.quit()