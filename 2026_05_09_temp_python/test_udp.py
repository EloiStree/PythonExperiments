import asyncio
from bleak import BleakScanner, BleakClient

MICROBIT_ADDRESS = "EE:14:F0:AC:48:E6"

async def discover_services():
    """Discover and display all services on the micro:bit"""
    
    print(f"Connecting to {MICROBIT_ADDRESS}...")
    
    async with BleakClient(MICROBIT_ADDRESS) as client:
        print(f"Connected: {await client.is_connected()}")
        
        # Get all services
        services = await client.get_services()
        
        print("\n" + "="*50)
        print("ALL SERVICES FOUND ON MICRO:BIT")
        print("="*50)
        
        for service in services:
            print(f"\nService: {service.uuid}")
            print(f"  Handle: {service.handle}")
            print(f"  Description: {service.description}")
            
            # List characteristics for this service
            for char in service.characteristics:
                print(f"  Characteristic: {char.uuid}")
                print(f"    Properties: {char.properties}")
                print(f"    Handle: {char.handle}")
                
                # Try to read the value if possible
                if 'read' in char.properties:
                    try:
                        value = await client.read_gatt_char(char.uuid)
                        print(f"    Value: {value}")
                    except:
                        print(f"    Value: (read failed)")
        
        print("\n" + "="*50)
        
        # Check specifically for Nordic UART
        uart_found = False
        for service in services:
            if "6E400001" in service.uuid.upper():
                uart_found = True
                print("✓ Nordic UART Service FOUND!")
                break
        
        if not uart_found:
            print("✗ Nordic UART Service NOT FOUND")
            print("\nThis means your micro:bit is NOT running a UART program.")
            print("\nPlease ensure:")
            print("1. You've programmed your micro:bit with Bluetooth UART")
            print("2. The micro:bit is powered on and not in sleep mode")
            print("3. You're using the correct MAC address")

if __name__ == "__main__":
    asyncio.run(discover_services())