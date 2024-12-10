import os
import socket as soc
import time
import random
from PIL import Image

HOST = "skarm.ludd.ltu.se"
PORT = 1337

socket = soc.socket(soc.AF_INET, soc.SOCK_STREAM)
socket.connect((HOST, PORT))

# Get screen size
SCREEN_MAX_X = 1024
SCREEN_MAX_Y = 576
data, _, _, _ = socket.recvmsg(100,100)
print(data)

# Load GIF image
img = Image.open("./nyancat.gif", "r")

# Convert GIF image to array of normal PIL images
frames = []

try:
    while True:
        frame = img.copy()
        frame = frame.convert("RGB")
        frame.thumbnail((128, 128))
        frames.append(frame)
        img.seek(len(frames))
except:
    pass

# Dunno how this works, converts pixel value to a valid color hex string
def pixelValToHex(pixel):
    return "%02x%02x%02x" % pixel

MAX_X, MAX_Y = frames[0].size

def genYPos():
    return random.randrange(0, SCREEN_MAX_Y - MAX_Y)


# Make cat move forward
x_pos = 900
y_pos = genYPos()
next_y_pos = genYPos()

while True:
    # Loop through the array and render the images
    for frame in frames:
        output = ""
        for y in range(0, MAX_Y):
            for x in range(0, MAX_X):
                color = pixelValToHex(frame.getpixel((x, y)))

                # If pixel has passed the x border, draw at next y height and from start of screen
                drawpos_x = (x + x_pos) % SCREEN_MAX_X
                drawpos_y = y_pos + y
                if (x + x_pos) > SCREEN_MAX_X:
                    drawpos_y = next_y_pos + y

                output += f"PX {drawpos_x} {drawpos_y} {color}\n"

        # Send output to screen
        socket.sendall(output.encode())

        # Update X/Y starting positions as necessary
        x_pos += 4
        if x_pos >= SCREEN_MAX_X:
            y_pos = next_y_pos
            next_y_pos = genYPos()
        x_pos %= SCREEN_MAX_X

        # Wait to save CPU and lower framerate to a more reasonable level
        time.sleep(1/12)