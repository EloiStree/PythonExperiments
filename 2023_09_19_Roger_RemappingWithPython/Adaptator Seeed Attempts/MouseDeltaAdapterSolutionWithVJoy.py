import time
import sys
import pyvjoy
import pyautogui
from pynput import keyboard
import threading
from pynput import mouse
from pywinauto.mouse import move
import win32api
import win32con

# To simulate the adapater i am using this a Xbox and this tool:
## Gropher https://github.com/Tylemagne/Gopher360/releases/tag/v0.985
# The joystick is convert as a mouse
# I am using the arrow of the xbox as they are use as keyboard arrow.
# Left lock the game Down free the game Up move   right interact



# ###########  Public VARIABLE ########### ########### ########### ########### 
# change variable here if you need too.

# Keystroke to make the user move forward           
char_key_move="z"
# keystroke to interact with the object
char_key_interact="c"
# Switch from playing lock mode to holding mode 
char_key_switch_play_mode="h"
# Switch from playing lock mode  
char_key_switch_play_mode_on="j"
# Switch to holding mode 
char_key_switch_play_mode_off="k"
# Switch to holding mode 
char_key_request_quit="g"


# How many second before joystick is consider not moving. When release
reset_joystick_zero_time_second=0.05


# Is mouse but be hide when playing 
hide_mouse_in_playmode=True


# Allow to reduce the joystick range to speed down the in game move.
multiplicator_joy_x=0.1
multiplicator_joy_y=0.1

# Convert the distance of a delta moved in pixel to a joystickv -1.0 /1.0  valuz
# The pixel moved between each frame change between each software or hardware "mouse"
delta_per_second_to_joystick=1500.0






# ###########  Private VARIABLE ########### ########### ########### ########### 
# Avoid the methode to be call in loop and slow the python thread
avoid_spamming_move=False
avoid_spamming_interact=False

# Whhere the mouse must be locked too.
# In this code the middle of the screen
thread_x_mouse=0
thread_y_mouse=0


#The time tick between every frame
previousTick =0.0
currentTick =0.0
# The delta time in seconds past since last frame
timeBetweenFrameS=0
# The delta time in milli seconds past since last frame
timeBetweenFrameMS=0

# Is use to display in the console some log to debug the tool.
debugLogCountdown=0;

# The distance in pixel moved since the last reset
delta_x=0.0
delta_y=0.0
# Distance move per seconds based on the last reset compare to delta time
delta_x_per_second=0.0
delta_y_per_second=0.0
#  Convertion of the delta per seconds move to a joystick value
delta_x_joystick=0.0
delta_y_joystick=0.0

# The the time of since the delta was not moving at all.
not_moving_time_second =0
not_moving_time_second_previous=0


# Represent if the simulator must be running or on hold
running=True



# The game has bug with joystick 1, so you need to use the second one while the first is used as a bait.
joystick = pyvjoy.VJoyDevice(2)


current_mouse_pos=(0,0)
x_mouse, y_mouse =0.0,0.0
x_mouse_previous, y_mouse_previous =0.0,0.0


current_mouse_pos = pyautogui.position()
prev_mouse_pos = pyautogui.position()


quit_request=False
joystick_horizontal = 0
joystick_vertical = 0

running=False

keyPrevious=False
keyCurrent=False
switch_state=False


pyautogui.FAILSAFE = False











    
def refresh_mouse_position():
    global current_mouse_pos
    global x_mouse
    global y_mouse
    current_mouse_pos = pyautogui.position()
    x_mouse =current_mouse_pos.x
    y_mouse =current_mouse_pos.y


# ACTION TO DO IN GAME START ############
def crouch():
    pyautogui.keyDown(char_key_move)
    pyautogui.keyUp(char_key_move)
    pyautogui.keyDown(char_key_move)
    pyautogui.keyUp(char_key_move)
    

def action_interact_start():
    pyautogui.keyDown('ctrlleft')
    print(" action_interact_start")
    
def action_interact_stop():
    pyautogui.keyUp('ctrlleft')
    print(" action_interact_stop")

def action_interact():
    pyautogui.keyDown('ctrlleft')
    pyautogui.keyUp('ctrlleft')
    print(" action_interact")
    
def action_interact_stop():
    pyautogui.keyUp('ctrlleft')
    print(" action_interact_stop")
    
def action_move_start():
    joystick.set_button(1, 1)
    print(" action_move_start")

def action_move_stop():
    joystick.set_button(1, 0)
    print(" action_move_stop")
    
# ACTION TO DO IN GAME END ###########


    
def clamp(value, min_value, max_value):
    return max(min(value, max_value), min_value)




# Will switch be a lock mode to play and a hold move to interact with menu
def switch_running_state_onoff( runningState):
    global running
    running = runningState
    if hide_mouse_in_playmode:
        win32api.ShowCursor(not runningState)
        #pygame.mouse.set_visible(not runningState)

# Will switch be a lock mode to play and a hold move to interact with menu
def switch_running_state():
    global running
    running = not running  
    switch_running_state_onoff(running)


        

def quit_game():
    global quit_request, running
    quit_request=True
    running=False
    switch_running_state_onoff(False)


###################################### START KEY BOARD LISTENING ###############
    
def on_key_press(key):
    global running,avoid_spamming_move,avoid_spamming_interact
    try:
        if key == keyboard.Key.esc:
            quit_game()
        #elif key == keyboard.Key.space:
        #    print("Spacebar is pressed!")
        elif key == keyboard.Key.left:
            switch_running_state_onoff(True)
        elif key == keyboard.Key.down:
            switch_running_state_onoff(False)
        elif key == keyboard.Key.right:
            if avoid_spamming_interact == False:
                avoid_spamming_interact=True
                action_interact()
            
        elif key == keyboard.Key.up:
            if avoid_spamming_move == False:
                avoid_spamming_move=True
                action_move_start()
        

        
        
            
        else:
            print(f"Key pressed: {key.char}")
            if key.char==char_key_switch_play_mode:
                switch_running_state()
            if key.char==char_key_switch_play_mode_on:
                switch_running_state_onoff(True)
            if key.char==char_key_switch_play_mode_off:
                switch_running_state_onoff(False)
            if key.char==char_key_request_quit:
                quit_game()
                
               
            if key.char==char_key_move:
                if avoid_spamming_move == False:
                    avoid_spamming_move=True
                    action_move_start()
            if key.char==char_key_interact:
                if avoid_spamming_interact == False:
                    avoid_spamming_interact=True
                    action_interact()
            
    except AttributeError:
        print(f"Special key pressed: {key}")

def on_key_release(key):
    global running,avoid_spamming_move ,avoid_spamming_interact
    try:
        if key == keyboard.Key.right:
            avoid_spamming_interact=False
        elif key == keyboard.Key.up:
            avoid_spamming_move=False
            action_move_stop()
        else :
            print(f"Key released: {key.char}")
            if key.char==char_key_move:
                avoid_spamming_move=False
                action_move_stop()
            if key.char==char_key_interact:
                avoid_spamming_interact=False
    except AttributeError:
        print(f"Special key released: {key}")
        
###################################### END KEY BOARD LISTENING ###############vvvvvvv

# Use this methode to debug in print log once in N seconds
def LogState():
    print(f"Ping {timeBetweenFrameMS} / {timeBetweenFrameS} JX{round(joystick_horizontal, 2)} JY{round(joystick_vertical, 2)} D {delta_x} {delta_y} DS {int(delta_x_per_second)} {int(delta_y_per_second)} ")
    print(f"Ping JX{round(delta_x_joystick, 2)} JY{round(delta_y_joystick, 2)}  ")

# This function will reset the mouse at the center of the screen to allows to use delta move as input.
def ResetMouse():
    global x_mouse_previous, y_mouse_previous
    global thread_x_mouse, thread_y_mouse,requestToSetMousePosition
    global running
    screen_width, screen_height = pyautogui.size()
    requestToSetMousePosition=True
    thread_x_mouse =screen_width // 2
    thread_y_mouse = screen_height // 2
    win32api.SetCursorPos((thread_x_mouse,thread_y_mouse))
    if hide_mouse_in_playmode:
        win32api.ShowCursor(not running)
    
    refresh_mouse_position()
    # Reset the mouse to avoid having a "negatif" delta on recenter
    x_mouse =thread_x_mouse
    y_mouse =thread_y_mouse
    x_mouse_previous = x_mouse
    y_mouse_previous = y_mouse
    






    
# Start a thread that listen to keystroke of the keyboard.
listener_thread = threading.Thread(target=lambda: keyboard.Listener(on_press=on_key_press, on_release=on_key_release).start())
listener_thread.start()
listener_thread.join()

print("Start")
win32api.ShowCursor(False)

refresh_mouse_position()

while not quit_request:

    #Count the time passing between frame
    previousTick =currentTick
    currentTick=start_time_ms = int(time.time() * 1000)
    timeBetweenFrameMS = currentTick - previousTick
    timeBetweenFrameS = (currentTick - previousTick)/1000


    # Every n time debug log a print to see what is happening
    debugLogCountdown-=timeBetweenFrameS
    if debugLogCountdown < 0.0:
        debugLogCountdown=1.0
        LogState()
    
    vjoy_x=0 
    vjoy_y=0 
    if running:

        #Check what is the current position of the mouse to compute the delta
        refresh_mouse_position()

        # Delta of the mouse moving from the screen center
        delta_x = x_mouse - x_mouse_previous
        delta_y = - ( y_mouse - y_mouse_previous )


        # If it does not move we check since when to reset the joystick to Zero
        if delta_x==0 and  delta_y==0 :
            #print("Not Moving")
            not_moving_time_second_previous=not_moving_time_second
            not_moving_time_second+=timeBetweenFrameS
            if not_moving_time_second_previous < reset_joystick_zero_time_second and not_moving_time_second >= reset_joystick_zero_time_second :
                print("Not Moving Reset joystick")
                delta_x_per_second =0
                delta_y_per_second =0
                delta_x_joystick = 0
                delta_y_joystick = 0
                delta_x_joystick =0
                delta_y_joystick=0

        # If it did move, we compute the delta and convert it to a joystick value
        if delta_x!=0 or  delta_y!=0:
            not_moving_time_second=0
            # If yes we have a new mouse move detected.
            delta_x_per_second =delta_x / timeBetweenFrameS
            delta_y_per_second =delta_y / timeBetweenFrameS
            delta_x_joystick = delta_x_per_second / delta_per_second_to_joystick
            delta_y_joystick = delta_y_per_second / delta_per_second_to_joystick
            delta_x_joystick =clamp(delta_x_joystick,-1.0,1.0)
            delta_y_joystick=clamp(delta_y_joystick,-1.0,1.0)
        

        # Convert the joystick value to vJoy joystick value
        vjoy_x= int(((delta_x_joystick+1.0)/2.0)*32768.0)
        vjoy_y= int(((-delta_y_joystick+1.0)/2.0)*32768.0)
        
        # Set the virtual joystick to the want value
        joystick.set_axis(pyvjoy.HID_USAGE_X, vjoy_x)
        joystick.set_axis(pyvjoy.HID_USAGE_Y, vjoy_y)

        # Reset the mouse to the center of the screen and the global variable to ready for the next frame.
        ResetMouse()
        
    #Wait a bit to avoid over use of the thread    
    time.sleep(0.001)


# Code call if the user request to stop playing
print(f"///////////GAME QUIT////////////////")

# I should kill the thread hear but don't know how to do it.
''' pigame pygame.quit() pigame'''
sys.exit(0)
