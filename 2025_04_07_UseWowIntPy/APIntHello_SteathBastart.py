
# https://pypi.org/project/iid42/
from iid42 import *
# https://pypi.org/project/wowint/
from wowint import WowIntegerTarget, WowIntegerKeyboard

import socket
import struct
import time

target_udp = "127.0.0.1"
target_port = 7073
player_index =0

key_left = WowIntegerKeyboard.arrow_left
key_right = WowIntegerKeyboard.arrow_right
key_up = WowIntegerKeyboard.arrow_up
key_down = WowIntegerKeyboard.arrow_down
key_jump = WowIntegerKeyboard.key_a
key_carry = WowIntegerKeyboard.key_z
key_gadget = WowIntegerKeyboard.key_e
key_restart = WowIntegerKeyboard.key_r
key_enter = WowIntegerKeyboard.enter
sender = SendUdpIID(target_udp, target_port,True)

time.sleep(1)
sender.push_index_integer( player_index,key_enter)
time.sleep(1)
sender.push_index_integer(player_index,key_enter+1000)
time.sleep(1)
sender.push_index_integer( player_index,key_restart)
time.sleep(1)
sender.push_index_integer(player_index,key_restart+1000)
time.sleep(1)

while True:
    time.sleep(1)
    sender.push_index_integer( player_index,key_right)
    time.sleep(1)
    sender.push_index_integer(player_index,key_right+1000)

    time.sleep(1)
    sender.push_index_integer( player_index,key_left)
    time.sleep(1)
    sender.push_index_integer(player_index,key_left+1000)






