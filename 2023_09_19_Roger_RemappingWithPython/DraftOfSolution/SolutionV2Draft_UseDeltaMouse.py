## This solution was in the good direction but it is a a bit hard to have something smooth with Delta.
# So I am going to go on a solution where I lock the mouse in a radius around screen center in next version



import pygame
import sys
import pyvjoy


hide_mouse = False

# Initialize Pygame
pygame.init()

# Initialize vJoy
joystick = pyvjoy.VJoyDevice(1)  # Adjust the device ID as needed

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Initial position of the vector2
x, y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2

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

delta_deathzone=10

while not quit_request:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    delta_time = clock.tick(60)
    # Check for key press to toggle the script on/off
    keys = pygame.key.get_pressed()
    keyPrevious = keyCurrent
    keyCurrent = keys[pygame.K_SPACE]

    if keyCurrent==True and keyPrevious==False:
        running = not running  # Toggle the script on/off when spacebar is pressed
        if hide_mouse:
            pygame.mouse.set_visible(not running)
        joystick.set_button(6, running)
        joystick.set_axis(pyvjoy.HID_USAGE_Z, running if 255 else 32768)
    if keys[pygame.K_ESCAPE]:
        quit_request=True
        running=False
        pygame.mouse.set_visible(True)

    if running:
        # Get the current mouse position
        current_mouse_pos = pygame.mouse.get_pos()
        # Calculate the delta of mouse movement
        delta_x = current_mouse_pos[0] - prev_mouse_pos[0]
        delta_y = current_mouse_pos[1] - prev_mouse_pos[1]


        if delta_x< delta_deathzone and delta_x > - delta_deathzone:
            delta_x=0
        if delta_y< delta_deathzone and delta_y > - delta_deathzone:
            delta_y=0
    
        

        if delta_x > 0:
            joystick_horizontal = -1
        elif delta_x < 0:
            joystick_horizontal = 1

        if delta_y > 0:
            joystick_vertical = 1
        elif delta_y < 0:
            joystick_vertical = -1

        if delta_x !=0 :
            back_to_zero_latency_timer_x=0
        else:
            back_to_zero_latency_timer_x+=delta_time;

        if  delta_y!=0:
            back_to_zero_latency_timer_y=0
        else:
            back_to_zero_latency_timer_y+=delta_time;

        if back_to_zero_latency_timer_x > back_to_zero_latency:
            joystick_horizontal=0
        if back_to_zero_latency_timer_y > back_to_zero_latency:
            joystick_vertical=0

        vjoy_x= int(((joystick_horizontal+1.0)/2.0)*32768.0)
        vjoy_y= int(((-joystick_vertical+1.0)/2.0)*32768.0)
        if joystick_horizontal==0:
            vjoy_x= 16384
        if joystick_vertical==0:
            vjoy_y= 16384
            
        joystick.set_axis(pyvjoy.HID_USAGE_X, vjoy_x)
        joystick.set_axis(pyvjoy.HID_USAGE_Y, vjoy_y)
        # Clear the screen
        screen.fill(WHITE)

        # Draw the vector2 at its new position
        pygame.draw.circle(screen, (0, 0, 255), ((SCREEN_WIDTH // 2) + joystick_horizontal * 10 , (SCREEN_HEIGHT // 2) + joystick_vertical * 10), 20)
        

        # Render and display joystick_horizontal and joystick_vertical values
        text_horizontal = font.render(f'Horizontal: {joystick_horizontal}', True, BLACK)
        text_vertical = font.render(f'Vertical: {joystick_vertical}', True, BLACK)
        text_lag = font.render(f'Lag:  {back_to_zero_latency_timer_x} {back_to_zero_latency_timer_y}', True, BLACK)
        text_delta = font.render(f'Delta: {delta_x} {delta_y}', True, BLACK)
        screen.blit(text_horizontal, (20, 20))
        screen.blit(text_vertical, (20, 60))
        screen.blit(text_lag, (20, 100))
        screen.blit(text_delta, (20, 140))

        # Store the current mouse position for the next iteration
        prev_mouse_pos = current_mouse_pos if running else prev_mouse_pos
        pygame.mouse.set_pos(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        pygame.time.delay(100)

    # Update the display
    pygame.display.flip()

