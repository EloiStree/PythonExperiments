import time
import sys
import pyvjoy
import pyautogui
from pynput import keyboard
import threading
from pynput import mouse


            
char_key_move='z'
char_key_interact='c'
char_key_crouch='i'
char_key_switch_play_mode='s'
char_key_switch_play_mode_on='j'
char_key_switch_play_mode_off='k'
char_key_refresh_center_anchor='l'
char_key_refresh_current_anchor='m'

use_clamp_mouse=True

# Is mouse but be hide when playing
hide_mouse = False

# The game has bug with joystick 1, so you need to use the second one while the first is used as a bait.
joystick = pyvjoy.VJoyDevice(2)


current_mouse_pos=(0,0)
x_anchor, y_anchor =0.0,0.0
x_mouse, y_mouse =0.0,0.0
anchor_radius =150.0
anchor_radius_deathzone_percent=0.1





running = False  

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

def reset_anchor_position():
    global current_mouse_pos
    global x_anchor
    global y_anchor
    current_mouse_pos = pyautogui.position()
    x_anchor =current_mouse_pos.x
    y_anchor =current_mouse_pos.y
   
    print(f"Reset anchor at mouse position of the screen: ({x_anchor}, {y_anchor})")

def reset_anchor_position_at_center():
    global current_mouse_pos
    global x_anchor
    global y_anchor
    screen_width, screen_height = pyautogui.size()
    x_anchor =screen_width // 2
    y_anchor =screen_height // 2
    print(f"Middle of the screen: ({x_anchor}, {y_anchor})")
    
def refresh_mouse_position():
    global current_mouse_pos
    global x_mouse
    global y_mouse
    current_mouse_pos = pyautogui.position()
    x_mouse =current_mouse_pos.x
    y_mouse =current_mouse_pos.y

def set_mouse_positoin(x,y):
    pyautogui.moveTo(x, y, duration=0)

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
    #joystick.set_button(2, 1)
    #joystick.set_button(3, 1)
    joystick.set_button(1, 1)
    print(" action_move_start")

def action_move_stop():
    #joystick.set_button(3, 0)
    #joystick.set_button(2, 0)
    joystick.set_button(1, 0)
    print(" action_move_stop")
    
def clamp(value, min_value, max_value):
    return max(min(value, max_value), min_value)

reset_anchor_position()
refresh_mouse_position()

def display_mouse_position(e):
    if e.event_type == keyboard.KEY_DOWN and e.name == 'space':
        current_pos = pyautogui.position()
        print(f"Mouse position: x={current_pos[0]}, y={current_pos[1]}")


def switch_running_state():
    global running
    running = not running  
    #if hide_mouse:
        #pygame.mouse.set_visible(not running)
    #pygame.mouse.set_visible(running)

def switch_running_state_onoff( runningState):
    global running
    running = runningState  
    #if hide_mouse:
        #pygame.mouse.set_visible(not running)
    #pygame.mouse.set_visible(running)

def quit_game():
    global quit_request, running
    quit_request=True
    running=False
    pygame.mouse.set_visible(True)


avoid_spamming_move=False
avoid_spamming_interact=False
def on_key_press(key):
    global running,avoid_spamming_move,avoid_spamming_interact
    try:
        if key == keyboard.Key.esc:
            print("Escape is pressed!")
            quit_game()
        elif key == keyboard.Key.space:
            print("Spacebar is pressed!")
            switch_running_state()
        else:
            print(f"Key pressed: {key.char}")
            if key.char==char_key_crouch:
                crouch()
            if key.char==char_key_switch_play_mode:
                switch_running_state()
            if key.char==char_key_switch_play_mode_on:
                switch_running_state_onoff(True)
            if key.char==char_key_switch_play_mode_off:
                switch_running_state_onoff(False)
               
            if key.char==char_key_move:
                if avoid_spamming_move == False:
                    avoid_spamming_move=True
                    action_move_start()
            if key.char==char_key_interact:
                if avoid_spamming_interact == False:
                    avoid_spamming_interact=True
                    action_interact()
            if key.char==char_key_refresh_current_anchor:
                reset_anchor_position()
            if key.char==char_key_refresh_center_anchor:
                reset_anchor_position_at_center()
            
    except AttributeError:
        print(f"Special key pressed: {key}")

def on_key_release(key):
    global running,avoid_spamming_move ,avoid_spamming_interact
    try:
        print(f"Key released: {key.char}")
        if key.char==char_key_move:
            avoid_spamming_move=False
            action_move_stop()
        if key.char==char_key_interact:
            avoid_spamming_interact=False
    except AttributeError:
        print(f"Special key released: {key}")

def on_click(x, y, button, pressed):
    '''
    global left_button_pressed, right_button_pressed
    
    if button == mouse.Button.left and pressed:
        print("Left mouse button is pressed.")
        action_move_start()
    elif button == mouse.Button.left and not pressed:
        print("Left mouse button is release.")
        action_move_stop()
    elif button == mouse.Button.right and pressed:
        print("right mouse button is pressed.")
        action_interact_start()
    elif button == mouse.Button.right and not pressed:
        print("right mouse button is release.")
        action_interact_stop()
        '''


listener_thread = threading.Thread(target=lambda: keyboard.Listener(on_press=on_key_press, on_release=on_key_release).start())
listener_thread.start()
listener_thread.join()
mouse_listener = mouse.Listener(on_click=on_click)
mouse_thread = threading.Thread(target=mouse_listener.start)
mouse_thread.start()
mouse_thread.join()

#To Code use a mode that is choosable  by user PlayPref
reset_anchor_position_at_center()

while not quit_request:
    
    vjoy_x=0
    vjoy_y=0
    if running:
        refresh_mouse_position()

    

        joystick_horizontal = (x_mouse - x_anchor)/ anchor_radius
        joystick_vertical = -(y_mouse - y_anchor)/ anchor_radius

        joystick_horizontal =clamp(joystick_horizontal,-1.0,1.0)
        joystick_vertical=clamp(joystick_vertical,-1.0,1.0)

        vjoy_x= int(((joystick_horizontal+1.0)/2.0)*32768.0)
        vjoy_y= int(((-joystick_vertical+1.0)/2.0)*32768.0)
        
        #IF YOU NEED A DEATH ZONE FOR THE JOYSTICK
        #if joystick_horizontal>=-anchor_radius_deathzone_percent and joystick_horizontal<=anchor_radius_deathzone_percent:
        #    vjoy_x= 32767
        #if joystick_vertical>=-anchor_radius_deathzone_percent and joystick_vertical<=anchor_radius_deathzone_percent:
        #    vjoy_y= 32767

        xPixel = x_mouse-x_anchor
        yPixel = y_mouse-y_anchor
        newX = x_mouse
        newY = y_mouse
        if(xPixel<-anchor_radius):
            newX= -anchor_radius+x_anchor
        elif(xPixel>anchor_radius):
            newX= anchor_radius+x_anchor
        if(yPixel<-anchor_radius):
            newY= -anchor_radius+y_anchor
        elif(yPixel>anchor_radius):
            newY= anchor_radius+y_anchor

            
        #pygame.mouse.set_pos(x_anchor+xPixel,y_anchor+yPixel)
        joystick.set_axis(pyvjoy.HID_USAGE_X, vjoy_x)
        joystick.set_axis(pyvjoy.HID_USAGE_Y, vjoy_y)

        
        if use_clamp_mouse and (newX != x_mouse or newY != y_mouse) :
            pyautogui.moveTo(newX,newY)
    time.sleep(0.001)



print(f"///////////GAME QUIT////////////////")
''' pigame pygame.quit() pigame'''
sys.exit()
