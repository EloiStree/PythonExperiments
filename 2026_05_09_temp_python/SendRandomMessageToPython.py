import socket
import time
import random

PORT = 3614
BROADCAST_IP = "255.255.255.255"  # UDP broadcast address

messages = [
    "Hello, this is a random message!",
    "How are you doing today?",
    "Python is great for socket programming.",
    "This is a test message.",
    "Random message number 5.",
    "Did you know that Python was named after Monty Python?",
    "Sockets are a way to communicate between processes.",
]

# Create UDP socket
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    print(f"Broadcasting messages on UDP port {PORT} every 2 seconds")

    try:
        while True:
            message = random.choice(messages)
            s.sendto(message.encode("utf-8"), (BROADCAST_IP, PORT))
            print(f"Broadcasted: {message}")
            time.sleep(2)
    except KeyboardInterrupt:
        print("Exiting...")
