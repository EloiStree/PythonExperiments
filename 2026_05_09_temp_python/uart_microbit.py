import asyncio
from bleak import BleakClient

# Your micro:bit's MAC address
MICROBIT_ADDRESS = "EE:14:F0:AC:48:E6"

# Nordic UART Service UUIDs (standard for micro:bit BLE)
UART_SERVICE_UUID = "6E400001-B5A3-F393-E0A9-E50E24DCCA9E"
UART_RX_CHAR_UUID = "6E400002-B5A3-F393-E0A9-E50E24DCCA9E"  # Characteristic for receiving data (write)
UART_TX_CHAR_UUID = "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"  # Characteristic for sending data (notify)

async def send_characters():
    """Connect to micro:bit and send a, b, c, d in a loop"""
    
    def handle_disconnect(client):
        print(f"Disconnected from {client.address}")
    
    def display_all_services_UUIDs(client):
        print("Services and Characteristics:")
        for service in client.services:
            print(f"Service: {service.uuid}")
            for char in service.characteristics:
                print(f"  Characteristic: {char.uuid} (Properties: {char.properties})")

    ## add methode that use  Characteristic: e95d5404-251d-470a-a062-fa1922dfa9a8 (Properties: ['write', 'write-without-response'])
    def write_to_characteristic(client, char_uuid, data):
        char = client.services.get_characteristic(char_uuid)
        if char and 'write' in char.properties:
            asyncio.create_task(client.write_gatt_char(char_uuid, data, response=False))
            print(f"Written to {char_uuid}: {data}")
        else:
            print(f"Characteristic {char_uuid} not found or not writable")

    async with BleakClient(MICROBIT_ADDRESS, disconnected_callback=handle_disconnect) as client:
        print(f"Connected to micro:bit: {client.address}")

        display_all_services_UUIDs(client)

        
        # Verify UART service exists
        uart_service = client.services.get_service(UART_SERVICE_UUID)
        if not uart_service:
            print("UART service not found on micro:bit")
            return
        
        # Verify RX characteristic exists
        rx_char = uart_service.get_characteristic(UART_RX_CHAR_UUID)
        if not rx_char:
            print("RX characteristic not found")
            return
        
        print("Ready to send characters. Press Ctrl+C to stop.\n")
        
        # Loop through characters a, b, c, d continuously
        characters = ['a', 'b', 'c', 'd']
        
        try:
            while True:
                for char in characters:
                    # Convert character to bytes and send
                    data = char.encode('utf-8')
                    await client.write_gatt_char(UART_RX_CHAR_UUID, data, response=False)
                    print(f"Sent: {char}")
                    await asyncio.sleep(1)  # 1 second delay between sends
                    
        except KeyboardInterrupt:
            print("\nStopped by user")

if __name__ == "__main__":
    asyncio.run(send_characters())