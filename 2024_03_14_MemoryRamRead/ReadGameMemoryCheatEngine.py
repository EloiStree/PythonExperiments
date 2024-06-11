import ctypes

# Define the process ID
process_id = 0x000424c

# Define the memory address
address = ctypes.c_void_p(0x1EB43923320)

# Open the process
process_handle = ctypes.windll.kernel32.OpenProcess(0x1F0FFF, False, process_id)

# Read the float value from the memory address
value = ctypes.c_float()

ctypes.windll.kernel32.ReadProcessMemory(process_handle, address, ctypes.byref(value), ctypes.sizeof(value), None)

# Close the process handle
ctypes.windll.kernel32.CloseHandle(process_handle)

# Print the value
print(value.value)
