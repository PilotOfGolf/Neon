import time
import requests
import adafruit_display_text.label
import board
import displayio
import framebufferio
import rgbmatrix
import terminalio

from adafruit_display_text import label
from datetime import datetime

import json

displayio.release_displays()

url = "https://api.n2yo.com/rest/v1/satellite/radiopasses/25544/40/85/100/1/45/&apiKey={API_KEY}"

try:
    apiData = requests.get(url).json()
    print("API Response:", apiData)
    # I FUCKING HATE JSON
    # WHY TF IS IT SO CONFUSING :SOB
    unixTime = apiData['passes'][0]['startUTC']
    
    pass_time = datetime.utcfromtimestamp(unixTime)
    
    current_time = datetime.utcnow()  # This gets the current UTC time
    
    # Calc time diff
    time_diff = pass_time - current_time
    time_diff_minutes = int(time_diff.total_seconds() / 60)
    
    # Format text
    display_text = f"{time_diff_minutes}min"
    print(f"Current time: {current_time}")
    print(f"Pass time: {pass_time}")
    print(f"Time until pass: {display_text}")

except Exception as e:
    print(f"Error processing data: {e}")
    display_text = "Error"

# Create matrix
matrix = rgbmatrix.RGBMatrix(
    width=64, height=32, bit_depth=1,
    rgb_pins=[board.D6, board.D5, board.D9, board.D11, board.D10, board.D12],
    addr_pins=[board.A5, board.A4, board.A3, board.A2],
    clock_pin=board.D13, latch_pin=board.D0, output_enable_pin=board.D1)

display = framebufferio.FramebufferDisplay(matrix, auto_refresh=False)

# Create display groups
group_root = displayio.Group()
group_text = displayio.Group()

# Create the "SS Rise In:" label
text_0 = label.Label(
    terminalio.FONT,
    color=0xff0000,
    text="SS Rise In:")
text_0.x = 1
text_0.y = 4

# Create the time differ label
text_1 = label.Label(
    terminalio.FONT,
    color=0xffff00,
    text=display_text)
text_1.x = 2
text_1.y = 16

# Add
group_text.append(text_0)
group_text.append(text_1)
group_root.append(group_text)

# Set root group and refresh
display.root_group = group_root
display.refresh(minimum_frames_per_second=0)

while True:
    try:
        current_time = datetime.utcnow()
        
        time_diff = pass_time - current_time
        time_diff_minutes = int(time_diff.total_seconds() / 60)
        
        text_1.text = f"{time_diff_minutes}min"
        
        display.refresh(minimum_frames_per_second=0)
        
        time.sleep(1)
        
    except Exception as e:
        print(f"Error updating : {e}")
        time.sleep(1)