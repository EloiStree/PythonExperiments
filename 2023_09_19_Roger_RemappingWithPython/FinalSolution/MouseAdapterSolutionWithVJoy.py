import pygame
import sys
import pyvjoy
import pyautogui
from pynput import keyboard
import threading
from pynput import mouse



hide_mouse = False

pygame.init()

# Initialize the joystick module
pygame.joystick.init()



# Initialize all connected joysticks
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
for joystick in joysticks:
    joystick.init()

# The game has bug with joystick 1, so you need to use the second one while the first is used as a bait.
joystick = pyvjoy.VJoyDevice(2)

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

clock = pygame.time.Clock()
running=False

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


def switch_running_state():
    global running
    running = not running  
    if hide_mouse:
        pygame.mouse.set_visible(not running)
    pygame.mouse.set_visible(running)
    reset_anchor_position_at_center()

def quit_game():
    quit_request=True
    running=False
    pygame.mouse.set_visible(True)

def on_key_press(key):
    try:
        if key == keyboard.Key.esc:
            print("Escape is pressed!")
            quit_game()
        elif key == keyboard.Key.space:
            print("Spacebar is pressed!")
            switch_running_state()
        else:
            print(f"Key pressed: {key.char}")
            if key.char=='x':
                action_move_start()
            if key.char=='z':
                action_interact()
            if key.char=='r':
                reset_anchor_position()
            if key.char=='c':
                reset_anchor_position_at_center()
            
    except AttributeError:
        print(f"Special key pressed: {key}")

def on_key_release(key):
    try:
        print(f"Key released: {key.char}")
        if key.char=='x':
            action_move_stop()
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

while not quit_request:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.JOYBUTTONDOWN:
            print(f"Joystick {event.joy} Button {event.button} pressed.")
            if event.button == 1:
                print("T2_");
                left_control_pressed = True
                pyautogui.keyDown('ctrlleft')
            if event.button == 2:
                print("T3_");
                vjoy_button_pressed = True
                vjoy_device.set_button(1, 1)
        elif event.type == pygame.JOYBUTTONUP:
            print(f"Joystick {event.joy} Button {event.button} released.")
            if event.button==1:
                print("T2-");
            if event.button==2:
                print("T3-");
            if event.button == 1 :
                left_control_pressed = False
                pyautogui.keyUp('ctrlleft')
                
            if event.button == 2 :
                vjoy_button_pressed = False
                vjoy_device.set_button(1, 0)
 
    delta_time = clock.tick(60)
    

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

