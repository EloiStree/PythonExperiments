import pygame
import pyvjoy
import pyautogui
import time

def main():
    pygame.init()

    # Initialize the joystick module
    pygame.joystick.init()

    # Check if any joysticks are connected
    if pygame.joystick.get_count() == 0:
        print("No joysticks found.")
        return

    # Initialize all connected joysticks
    joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
    for joystick in joysticks:
        joystick.init()

    print("Listening to pygame joystick 2 and 3. Press joystick 2 to simulate a left control keypress. Press joystick 3 to simulate vJoy button 0.")

    # Initialize vJoy
    vjoy_device = pyvjoy.VJoyDevice(1)  # Adjust the device ID as needed

    left_control_pressed = False
    vjoy_button_pressed = False
    
    vjoy_device.set_button(5, 1)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.JOYBUTTONDOWN:
                print(f"Joystick {event.joy} Button {event.button} pressed.")

                if event.button==2:
                    print("T2_");
                if event.button==3:
                    print("T3_");
                
                if event.button == 1:  # Adjust the button number as needed
                    left_control_pressed = True
                    pyautogui.keyDown('ctrlleft')  # Simulate left control keypress
                if event.button == 2:  # Joystick 3
                    vjoy_button_pressed = True
                    vjoy_device.set_button(1, 1)  # Simulate vJoy button 0 pressed
            elif event.type == pygame.JOYBUTTONUP:
                print(f"Joystick {event.joy} Button {event.button} released.")
                if event.button==2:
                    print("T2-");
                if event.button==3:
                    print("T3-");
                if event.button == 1 :  # Joystick 2
                    left_control_pressed = False
                    pyautogui.keyUp('ctrlleft')  # Simulate left control key release
                    
                if event.button == 2 :  # Joystick 3
                    vjoy_button_pressed = False
                    vjoy_device.set_button(1, 0)  # Simulate vJoy button 0 released

if __name__ == "__main__":
    main()
