import pywinusb.hid as hid
import threading

# Vendor and product IDs for Xbox controller (XInput compatible)
XBOX_VENDOR_ID = 0x045e
XBOX_PRODUCT_ID = 0x028e

# Define the callback function to handle controller input events
def on_xbox_controller_event(event):
    if event.event_type == hid.HID_EVT_IN_REPORT:
        # Parse the input report for button and axis states
        data = event.data
        buttons = data[1] | (data[2] << 8)
        left_thumb_x = data[3] | (data[4] << 8)
        left_thumb_y = data[5] | (data[6] << 8)
        right_thumb_x = data[7] | (data[8] << 8)
        right_thumb_y = data[9] | (data[10] << 8)

        # Print the button and axis states
        print(f"Buttons: {buttons}")
        print(f"Left Thumbstick X: {left_thumb_x}, Y: {left_thumb_y}")
        print(f"Right Thumbstick X: {right_thumb_x}, Y: {right_thumb_y}")

# Find and open the Xbox controller device
devices = hid.HidDeviceFilter(vendor_id=XBOX_VENDOR_ID, product_id=XBOX_PRODUCT_ID).get_devices()
if devices:
    xbox_controller = devices[0]
    xbox_controller.open()

    # Set up a thread to listen for events
    event_thread = threading.Thread(target=xbox_controller.listen, args=(on_xbox_controller_event,))
    event_thread.daemon = True
    event_thread.start()

    try:
        # Keep the program running
        event_thread.join()
    except KeyboardInterrupt:
        pass
else:
    print("Xbox controller not found.")
