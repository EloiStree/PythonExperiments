import pygame
import sys
import pyvjoy
import pyautogui
from pynput import keyboard
import threading



hide_mouse = False

pygame.init()

# Initialize the joystick module
pygame.joystick.init()



# Initialize all connected joysticks
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
for joystick in joysticks:
    joystick.init()

# Initialize vJoy
joystick = pyvjoy.VJoyDevice(2)  # Adjust the device ID as needed

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Initial position of the vector2
x, y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2

current_mouse_pos=(0,0)
x_anchor, y_anchor =0.0,0.0
x_mouse, y_mouse =0.0,0.0
anchor_radius =100.0
anchor_radius_deathzone_percent=0.1



# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Move Vector2 with Mouse Delta")

# Create a font object for displaying text
font = pygame.font.Font(None, 36)  # You can specify the font and size here

# Main game loop
running = False  # Initially, the script is off
prev_mouse_pos = pygame.mouse.get_pos()

quit_request=False
joystick_horizontal = 0
joystick_vertical = 0

back_to_zero_latency=1000
back_to_zero_latency_timer_x=0.3
back_to_zero_latency_timer_y=0.3
clock = pygame.time.Clock()


keyPrevious=False
keyCurrent=False
switch_state=False

current_mouse_pos

def reset_anchor_position():
    global current_mouse_pos
    global x_anchor
    global y_anchor
    current_mouse_pos = pyautogui.position()
    x_anchor =current_mouse_pos.x
    y_anchor =current_mouse_pos.y
def refresh_mouse_position():
    global current_mouse_pos
    global x_mouse
    global y_mouse
    current_mouse_pos = pyautogui.position()
    x_mouse =current_mouse_pos.x
    y_mouse =current_mouse_pos.y

def set_mouse_positoin(x,y):
    pyautogui.moveTo(x, y, duration=0)

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
    joystick.set_button(2, 1)
    joystick.set_button(3, 1)
    joystick.set_button(1, 1)
    print(" action_move_start")

def action_move_stop():
    joystick.set_button(3, 0)
    joystick.set_button(2, 0)
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



# Define the on_key_press and on_key_release functions
def on_key_press(key):
    try:
        print(f"Key pressed: {key.char}")
        if key.char=='x':
            action_move_start()
        if key.char=='z':
            action_interact()
            
    except AttributeError:
        print(f"Special key pressed: {key}")

def on_key_release(key):
    try:
        print(f"Key released: {key.char}")
        if key.char=='x':
            action_move_stop()
    except AttributeError:
        print(f"Special key released: {key}")

# Create a listener thread
listener_thread = threading.Thread(target=lambda: keyboard.Listener(on_press=on_key_press, on_release=on_key_release).start())

# Start the listener thread
listener_thread.start()

# Your main application code can run here, and the listener will run in the background

# Wait for the listener thread to finish (if needed)
listener_thread.join()

# Your main application code can run here, and the listener will run in the background


#listener_thread.join()



while not quit_request:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                left_button_pressed = True
                action_move_start()
                
            elif event.button == 3:  # Right mouse button
                right_button_pressed = True
                action_interact_start()

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left mouse button
                left_button_pressed = False
                action_move_stop()
                
            elif event.button == 3:  # Right mouse button
                right_button_pressed = False
                action_interact_stop()

            elif event.type == pygame.JOYBUTTONDOWN:
                print(f"Joystick {event.joy} Button {event.button} pressed.")
              
                if event.button == 1:  # Adjust the button number as needed
                    print("T2_");
                    left_control_pressed = True
                    pyautogui.keyDown('ctrlleft')  # Simulate left control keypress
                if event.button == 2:  # Joystick 3
                    print("T3_");
                    vjoy_button_pressed = True
                    vjoy_device.set_button(1, 1)  # Simulate vJoy button 0 pressed
                    
            elif event.type == pygame.JOYBUTTONUP:
                print(f"Joystick {event.joy} Button {event.button} released.")
              
                if event.button == 1 :  # Joystick 2
                    print("T2-");
                    left_control_pressed = False
                    pyautogui.keyUp('ctrlleft')  # Simulate left control key release
                    
                if event.button == 2 :  # Joystick 3
                    print("T3-");
                    vjoy_button_pressed = False
                    vjoy_device.set_button(1, 0)  # Simulate vJoy button 0 released
 
    delta_time = clock.tick(60)
    # Check for key press to toggle the script on/off
    keys = pygame.key.get_pressed()
    keyPrevious = keyCurrent
    keyCurrent = keys[pygame.K_SPACE]

    if keyCurrent==True and keyPrevious==False:
        running = not running  # Toggle the script on/off when spacebar is pressed
        if hide_mouse:
            pygame.mouse.set_visible(not running)
        
        reset_anchor_position()
        joystick.set_button(6, running)
        joystick.set_axis(pyvjoy.HID_USAGE_Z, running if 255 else 32768)
    if keys[pygame.K_ESCAPE]:
        quit_request=True
        running=False
        pygame.mouse.set_visible(True)
    if keys[pygame.K_r]:
        reset_anchor_position()

    if running:
        refresh_mouse_position()

        joystick_horizontal = (x_mouse - x_anchor)/ anchor_radius
        joystick_vertical = -(y_mouse - y_anchor)/ anchor_radius

        joystick_horizontal =clamp(joystick_horizontal,-1.0,1.0)
        joystick_vertical=clamp(joystick_vertical,-1.0,1.0)

        vjoy_x= int(((joystick_horizontal+1.0)/2.0)*32768.0)
        vjoy_y= int(((-joystick_vertical+1.0)/2.0)*32768.0)
        #65535 32768
         
        #if joystick_horizontal>=-anchor_radius_deathzone_percent and joystick_horizontal<=anchor_radius_deathzone_percent:
        #    vjoy_x= 32767
        #if joystick_vertical>=-anchor_radius_deathzone_percent and joystick_vertical<=anchor_radius_deathzone_percent:
        #    vjoy_y= 32767

        xPixel = x_mouse-x_anchor
        yPixel = y_mouse-y_anchor
        if(xPixel<-anchor_radius):
            xPixel= -anchor_radius
        elif(xPixel>anchor_radius):
            xPixel= anchor_radius
        if(yPixel<-anchor_radius):
            yPixel= -anchor_radius
        elif(yPixel>anchor_radius):
            yPixel= anchor_radius
        pygame.mouse.set_pos(x_anchor+xPixel,y_anchor+yPixel)
            
            
        joystick.set_axis(pyvjoy.HID_USAGE_X, vjoy_x)
        joystick.set_axis(pyvjoy.HID_USAGE_Y, vjoy_y)
        # Clear the screen
        screen.fill(WHITE)

        # Draw the vector2 at its new position
        pygame.draw.circle(screen, (0, 0, 255), ((SCREEN_WIDTH // 2) + joystick_horizontal * 10 , (SCREEN_HEIGHT // 2) + -joystick_vertical * 10), 20)
        

        # Render and display joystick_horizontal and joystick_vertical values
        text_horizontal = font.render(f'Horizontal: {joystick_horizontal}', True, BLACK)
        text_vertical = font.render(f'Vertical: {joystick_vertical}', True, BLACK)
        text_lag = font.render(f'Anchor X:  {x_anchor} {x_mouse} {y_anchor} {y_mouse}', True, BLACK)
        text_delta = font.render(f'Raw: {vjoy_x} {vjoy_y}', True, BLACK)
        screen.blit(text_horizontal, (20, 20))
        screen.blit(text_vertical, (20, 60))
        screen.blit(text_lag, (20, 100))
        screen.blit(text_delta, (20, 140))

        # Store the current mouse position for the next iteration
        #pygame.mouse.set_pos(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        pygame.time.delay(100)

    # Update the display
    pygame.display.flip()

