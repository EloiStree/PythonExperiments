from inputs import get_gamepad
import threading
import pyvjoy
import pyautogui

import time


use_print_log_raw=False
use_print_log_xbox=False

joy_max_value=32767.0

joy_max_value_trigger=255.0

joy_left_x=0
joy_left_y=0
joy_right_x=0
joy_right_y=0
joy_trigger_right=0
joy_trigger_left=0
joy_bl=False
joy_br=False
joy_sbl=False
joy_sbr=False
joy_jl=False
joy_jr=False
joy_tl=False
joy_tr=False
joy_bd=False
joy_bu=False
joy_al=False
joy_ar=False
joy_ad=False
joy_au=False
joy_ml=False
joy_mc=False
joy_mr=False


previousBD=False

# Define the vJoy device ID you want to control
vjoy_device_id = 2  # You may need to change this to the desired vJoy device ID

# Initialize the vJoy device
joystick = pyvjoy.VJoyDevice(vjoy_device_id)



i=0;
while True:
    
    previousBD= joy_bd
    i+=1
    print("I "+str(i))

    if True:
        if i==1:
            events = get_gamepad()
        for event in events:
            if event.ev_type == 'Sync':
                continue


            if use_print_log_raw:
                print(f"Event Type: {event.ev_type}, Code: {event.ev_type}-{event.code}, Value: {event.state}")
            
            if event.code== "ABS_Y":
                joy_left_y= event.state / joy_max_value
                joystick.set_axis(pyvjoy.HID_USAGE_Y, int(((-joy_left_y+1)*0.5)*32767.0))    

            elif event.code== "ABS_X":
                joy_left_x= event.state /joy_max_value
                joystick.set_axis(pyvjoy.HID_USAGE_X, int(((joy_left_x+1)*0.5)*32767.0))
    

            elif event.code== "ABS_RX":
                joy_right_x = event.state / joy_max_value
            elif event.code== "ABS_RY":
                joy_right_y= event.state /joy_max_value

            elif event.code== "ABS_Z":
                joy_trigger_left = event.state / joy_max_value_trigger
            elif event.code== "ABS_RZ":
                joy_trigger_right= event.state / joy_max_value_trigger

            elif event.code== "BTN_WEST":
                joy_bl=event.state==1
                joystick.set_button(1, joy_bl)
            elif event.code== "BTN_EAST":
                joy_br=event.state==1
            elif event.code== "BTN_TL":
                joy_sbl=event.state==1
            elif event.code== "BTN_TR":
                joy_sbr=event.state==1
            elif event.code== "BTN_THUMBL":
                joy_jl=event.state==1
            elif event.code== "BTN_THUMBR":
                joy_jr=event.state==1
            elif event.code== "BTN_SOUTH":
                joy_bd=event.state==1
                if joy_bd:
                    pyautogui.keyDown('ctrlleft')
                else:
                    pyautogui.keyUp('ctrlleft')
            elif event.code== "BTN_NORTH":
                joy_bu=event.state==1
            elif event.code== "ABS_HAT0X":
                joy_al=event.state==-1
            elif event.code== "ABS_HAT0X":
                joy_ar=event.state==1
            elif event.code== "ABS_HAT0Y":
                joy_ad=event.state==1
            elif event.code== "ABS_HAT0Y":
                joy_au=event.state==-1
            elif event.code== "BTN_START":
                joy_ml=event.state==1
            elif event.code== "BTN_SELECT":
                joy_mr=event.state==1 

            joy_tl = joy_trigger_left > 0.1
            joy_tr = joy_trigger_right > 0.1
            #if use_print_log_xbox:
            #    print(f"LX {joy_left_x} LY {joy_left_y} RX {joy_right_x} RY {joy_right_y} LT {joy_trigger_left} RT {joy_trigger_right} ML{joy_ml} MR{joy_mr} BL{joy_bl} BR{joy_br}  BD{joy_bd}  BU{joy_bu}  AL{joy_al} AR{joy_ar}  AD{joy_ad}  AU{joy_au} SBL{joy_sbl}  SBR{joy_sbr} JL{joy_jl}  JR{joy_jr} ")
            #print(f"LX {joy_left_x} LY {joy_left_y} RX {joy_right_x} RY {joy_right_y} LT {joy_trigger_left} RT {joy_trigger_right} ML{joy_ml} MR{joy_mr} BL{joy_bl} BR{joy_br}  BD{joy_bd}  BU{joy_bu}  AL{joy_al} AR{joy_ar}  AD{joy_ad}  AU{joy_au} SBL{joy_sbl}  SBR{joy_sbr} JL{joy_jl}  JR{joy_jr} ")
    
            if previousBD!=joy_bd and joy_bd:
                pyautogui.keyDown('ctrlleft')
            else:
                pyautogui.keyUp('ctrlleft')


