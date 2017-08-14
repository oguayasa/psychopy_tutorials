# -*- coding: utf-8 -*-
"""
Presenting subject instructions in psychopy.

@author: Olivia Guayasamin
"""

# -----Initializing Steps-----
# import psychopy
from psychopy import core as pcore
from psychopy import visual, gui, data, event
from psychopy.iohub import launchHubServer
# import ordered dictionary functionality
import collections


# ----- Start psychopy ioHub for creating and monitoring devices -----

# start io hub process 
io = launchHubServer()

# create keyboard and mouse devices
keyboard = io.devices.keyboard
mouse = io.devices.mouse
# Hide the mouse cursor
mouse.setSystemCursorVisibility(False)

# check that devices are connected
# keyboard
if io.getDevice('keyboard') is None:
    print ("Keyboard is not connected")
else: 
    print("Keyboard is connected")

# mouse
if io.getDevice('mouse') is None:
    print ("Mouse is not connected")
else: 
    print("Mouse is connected")

# make sure they are not actively collecting input until called to do so
keyboard.reporting = False
mouse.reporting = False


# ----- Create psychopy stimuli for presenting instructions -----

# make psychopy window
introWin = visual.Window(size = (3840, 2160),  # use YOUR screen dimensions
                       pos = [0, 0],
                       units = 'pix',
                       fullscr = False,
                       allowGUI = True,
                       monitor = None,  # find and calibrate YOUR monitor
                       winType = 'pyglet',
                       color = [0.4, 0.4, 0.4])  

# make training text
introText = visual.TextStim(introWin,
                           color = [1.0, 1.0, 1.0],
                           units = 'norm', 
                           height = 0.07, 
                           pos = (0.0, 0.0))

# put training text into a dictionary, using pre-calibration instructions
# as an example
introInstruct = [('0', ('Welcome to the experiment. Before we begin, we need to ' 
             'teach the computer about your eyes. To do this, we need to '
             'complete a brief calibration process.\n\nPress "c" to continue.')),
             ('1', ('Once the calibration is finished, it is important that '
             'you do not change your position or make any large head/body '
             'movements. Large movements will confuse the computer and make '
             'it difficulty to correctly give you points during the experiment.'
             '\n\nPress "c" to continue, or "x" to see the previous page.')), ('2', 
            ('During the first part of calibration process, please try to find '
             'a position that:\n- Is comfortable for you. \n- Shows your '
             'eyes in a GREEN color.\n- Consistenly shows your eyes. \n\nIf '
             'you have any questions, please ask now. When you are ready, '
             'press "c" to begin the calibration, or "x" to see the previous'
             ' page.'))]
                   
# change to an ordered dictionary
introInstruct = collections.OrderedDict(introInstruct)

# create variables to facilitate back and forth screen changes
introList = introInstruct.keys()
introNum = 0

# turn keyboard recording on
keyboard.reporting = True 

# set while loop control variable
runLoop = True        

# run through the instructions
while runLoop:

    # update text stim using text from dictionary
    introText.text = introInstruct.get(introList[introNum])    
    # draw text
    introText.draw()
    # show text
    introWin.flip()
    
    # wait for user input before going to next instruction
    for event in keyboard.getReleases(clear = True):
        # if user wants quit 
        if event.key in ['q']:
            introWin.close()  # close window
            pcore.quit()  # close all psychopy elements
            keyboard.reporting = False  # turn off keyboard
        # if user is ready to move to the next screen
        elif event.key in ['c'] and introNum < 2:
            introWin.flip
            introNum += 1  # advance to the next text in the dictionary
        # if user is at last instruction element and is ready to move on
        elif event.key in ['c'] and introNum == 2:
            keyboard.reporting = False  # turn off keyboard
            runLoop = False  # break out of the loop
        # if user wants to review previous instruction page
        elif event.key in ['x'] and introNum > 0 and introNum < 3:
            introWin.flip
            introNum -= 1  # return to the previous text in the dictionary
            
        # clear keyboard and mouse events not accessed this iteration
        io.clearEvents()
        
# close the window after loop is finished
introWin.close()

# turn off devices. this is only included here so that this code may be easily
# re-run. if you will be continuing to use keyboard and mouse input later in
# your code, do NOT shut off the ioHub connection.
io.quit()

# move on to the next part of your study
