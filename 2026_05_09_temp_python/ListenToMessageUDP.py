import socket

# Listen on all interfaces
UDP_IP = "0.0.0.0"
UDP_PORT = 3614  # Match your Godot port

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print(f"Listening for UDP packets on {UDP_IP}:{UDP_PORT}...")

while True:
    data, addr = sock.recvfrom(1024)  # buffer size 1024 bytes
    message = data.decode('utf-8')
    print(f"Received message from {addr}: {message}")
