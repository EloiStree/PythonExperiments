import asyncio
from bleak import BleakClient, BleakError

MICROBIT_ADDRESS = "EE:14:F0:AC:48:E6"

UART_SERVICE_UUID = "6e400001-b5a3-f393-e0a9-e50e24dcca9e"
UART_RX_CHAR_UUID = "6e400002-b5a3-f393-e0a9-e50e24dcca9e"
UART_TX_CHAR_UUID = "6e400003-b5a3-f393-e0a9-e50e24dcca9e"

# A characteristic that exists on your device (used to keep connection alive)
KEEP_ALIVE_CHAR = "e95d9775-251d-470a-a062-fa1922dfa9a8"


def notification_handler(sender, data):
    print(f"[notify] {sender}: {data}")


async def connect_and_run():
    while True:  # retry loop
        try:
            print("\nAttempting connection...")

            async with BleakClient(MICROBIT_ADDRESS, timeout=10.0) as client:
                print(f"Connected: {client.address}")

                # Give BLE stack time to stabilize
                await asyncio.sleep(1.5)

                if not client.is_connected:
                    print("Disconnected too early, retrying...")
                    continue

                # Start a notification to keep connection active
                try:
                    await client.start_notify(KEEP_ALIVE_CHAR, notification_handler)
                    print("Keep-alive notification started")
                except Exception:
                    print("Could not start keep-alive notify (not fatal)")

                # Give time for services to be fully available
                await asyncio.sleep(1)

                services = client.services

                print("\nServices:")
                for s in services:
                    print(s.uuid)

                uart_service = services.get_service(UART_SERVICE_UUID)

                if not uart_service:
                    print("UART service NOT found. This is not a timing issue.")
                    await asyncio.sleep(3)
                    continue

                print("UART service found")

                tx_char = uart_service.get_characteristic(UART_TX_CHAR_UUID)

                if not tx_char:
                    print("TX characteristic missing")
                    continue

                print("Sending loop started\n")

                while client.is_connected:
                    for c in ["a ", "b ", "c ", "d "]:
                        await client.write_gatt_char(tx_char, c.encode(), response=True)
                        print(f"Sent: .{c}.")
                        await asyncio.sleep(1)

                print("Disconnected during send loop")

        except BleakError as e:
            print(f"BLE error: {e}")

        except Exception as e:
            print(f"Unexpected error: {e}")

        print("Reconnecting in 3 seconds...\n")
        await asyncio.sleep(3)


if __name__ == "__main__":
    asyncio.run(connect_and_run())