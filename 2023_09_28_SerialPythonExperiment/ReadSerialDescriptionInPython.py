import serial
import serial.tools.list_ports
import socket
import threading
import time


print(f"\nHello\n")

use_custom_filter=True

char_as_value_numeric= ['0','1','2','3','4','|','5','6','7','8','9']
char_as_value_alpha= ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','|','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

def convert_char_value(char_value):

        print(f"\nLook for {char_value}")
        i=0.0;
        for  c in char_as_value_numeric:
            if char_value==c:
                #l=len(char_as_value_numeric)
                #rv=i/(len(char_as_value_numeric)-1)
                #print(f"\n{c}{char_value} -- {i}/{l-1}={rv}")
                return i/(len(char_as_value_numeric)-1)
            i+=1.0
            
        i=0.0;
        for  c in char_as_value_alpha:
            if char_value==c:
                return i/(len(char_as_value_alpha)-1)
            i+=1
    

def your_own_filtering(data_received):
    l = len(data_received)
    
    if l==1:
        if data_received=="A":
            data_received="bool:UnoDA:True"
        elif data_received=="a":
            data_received="bool:UnoDA:False"
        elif data_received=="B":
            data_received="bool:UnoDB:True"
        elif data_received=="b":
            data_received="bool:UnoDB:False"
        elif data_received=="C":
            data_received="bool:UnoDC:True"
        elif data_received=="c":
            data_received="bool:UnoDC:False"
            
        elif data_received=="D":
            data_received="bool:UnoDD:True"
        elif data_received=="d":
            data_received="bool:UnoDD:False"
            
        elif data_received=="E":
            data_received="bool:UnoDE:True"
        elif data_received=="e":
            data_received="bool:UnoDE:False"
            
        elif data_received=="F":
            data_received="bool:UnoDF:True"
        elif data_received=="f":
            data_received="bool:UnoDF:False"
        elif data_received=="G":
            data_received="bool:UnoDG:True"
        elif data_received=="g":
            data_received="bool:UnoDG:False"
        elif data_received=="H":
            data_received="bool:UnoDH:True"
        elif data_received=="h":
            data_received="bool:UnoDH:False"
        elif data_received=="I":
            data_received="bool:UnoDI:True"
        elif data_received=="i":
            data_received="bool:UnoDI:False"
        elif data_received=="J":
            data_received="bool:UnoDJ:True"
        elif data_received=="j":
            data_received="bool:UnoDJ:False"
        elif data_received=="K":
            data_received="bool:UnoDK:True"
        elif data_received=="k":
            data_received="bool:UnoDK:False"
        elif data_received=="L":
            data_received="bool:UnoDL:True"
        elif data_received=="l":
            data_received="bool:UnoDL:False"
        elif data_received=="M":
            data_received="bool:UnoDM:True"
        elif data_received=="m":
            data_received="bool:UnoDM:False"
            
    if l==2:
        name =""
        first_char = data_received[0].lower()
        value= convert_char_value(data_received[1])
        if first_char=='a':
            name="UnoAA"
        elif first_char=='b':
            name="UnoAB"
        elif first_char=='c':
            name="UnoAC"
        elif first_char=='d':
            name="UnoAD"
        elif first_char=='e':
            name="UnoAE"
        elif first_char=='f':
            name="UnoAF"
        elif first_char=='g':
            name="UnoAG"
        
        data_received=f"float:{name}:{value}"
    
        
    return data_received


use_manual_com_listener=True
com_ports_to_listen_manual_add = [
#"COM3",
    ]

device_description = [
    "USB Serial Device",
     "Arduino Mega 2560",
    ]


#parsing_tag_start="UnoRead|"
#parsing_tag_start="UR|"
parsing_tag_start=""
#parsing_tag_end="\n"
parsing_tag_end=""


# Define the UDP target information
UDP_TARGET_HOST = '25.38.254.222'  # Replace with the actual UDP target IP address or hostname
UDP_TARGET_PORT = 2506  # Replace with the actual UDP target port

# Function to send data to UDP target
def send_to_udp(data):
    if use_custom_filter:
        data= your_own_filtering(data)
    data= parsing_tag_start +data+parsing_tag_end
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.sendto(data.encode('utf-8'), (UDP_TARGET_HOST, UDP_TARGET_PORT))
    udp_socket.close()
    
    print(f"\nSent: {data}")

# Function to read and forward lines from a COM port to UDP
def read_and_forward(com_port):
    try:
        ser = serial.Serial(com_port, baudrate=9600, timeout=1)  # Adjust baudrate and timeout as needed
        while True:
            line = ser.readline().decode('utf-8').strip() # Read a line from the COM port
            if line:
                ## Dev note: I don't know why but if I don't use that, it will affect previous line instead of current...
                print(f"\nReceived: {line}")
                send_to_udp(line)
                
    except serial.SerialException as e:
        print(f"Error: {e}")
    finally:
        try:
            ser.close()
        except Exception as e:
            pass

# Get a list of available COM ports
available_com_ports = list(serial.tools.list_ports.comports())

if not available_com_ports:
    print("No COM ports found.")
else:
    # Initialize a separate list for the COM ports to listen to
    com_ports_to_listen = [
    ]


if use_manual_com_listener:
    for comNam in com_ports_to_listen_manual_add:
        com_ports_to_listen.append(comNam)
        



# Iterate through the list of COM ports and print their descriptions
for port_info in available_com_ports:
    port, desc, _ = port_info
    print(f"COM Port: {port}, Description: {desc}")
    for dev_desc in device_description:
        if dev_desc in desc.strip():
            com_ports_to_listen.append(port)

# Start a thread for each COM port to listen to
threads = []
for port in com_ports_to_listen:
    thread = threading.Thread(target=read_and_forward, args=(port,))
    threads.append(thread)
    thread.start()

# Wait for all threads to finish
for thread in threads:
    thread.join()
