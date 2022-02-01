from ast import Str
import math
import os
import socket as soc
import time
import random
from xml.etree.ElementTree import tostring

HOST = "skarm.ludd.ltu.se"
PORT = 1337

# Size of the screen: 1024x576
SCREEN_MAX_X = 1024
SCREEN_MAX_Y = 576
SCALE = 64
MAX_X = math.floor(SCREEN_MAX_X/SCALE)
MAX_Y = math.floor(SCREEN_MAX_Y/SCALE)

# Snake is an array of snakeparts
class SnakePart:
  def __init__(self, x, y, life):
      self.x = x
      self.y = y
      self.life = life

  def age(self):
    self.life -= 1

# Setup snake
snakeArray = []
age = 5
heading = 1     # 0 = up, 1 = right, 2 = down, 3 = left

def reset():
  age = 1
  snakeArray[:] = [SnakePart(math.floor(MAX_X/2), math.floor(MAX_Y/2), age)]

def tick():
  for (i, part) in enumerate(snakeArray):
    part.age()
  if (snakeArray[0].life <= 0):
    snakeArray.pop(0)

def move(direction):
  # Move snake forward by adding a new snakepart with age + 1 (to cancel out the coming tick)
  if direction == 0:
    snakeArray.append(SnakePart(snakeArray[-1].x,     snakeArray[-1].y - 1, age + 1))
  elif direction == 1:
    snakeArray.append(SnakePart(snakeArray[-1].x + 1, snakeArray[-1].y,     age + 1))
  elif direction == 2:
    snakeArray.append(SnakePart(snakeArray[-1].x,     snakeArray[-1].y + 1, age + 1))
  elif direction == 3:
    snakeArray.append(SnakePart(snakeArray[-1].x - 1, snakeArray[-1].y,     age + 1))

def renderPart(part):
  print(part.x, part.y, part.life)
  renderString = ""
  color = str(random.randrange(0, 10))*6 # Random greyscale color
  # Make a square
  for x in range(0, SCALE):
    for y in range(0, SCALE):
      # Draw border white
      if x == 0 or y == 0 or x == SCALE-1 or y == SCALE-1:
        renderString += f"PX {part.x*SCALE + x} {part.y*SCALE + y} FFFFFF\n"
      else:
        renderString += f"PX {part.x*SCALE + x} {part.y*SCALE + y} {color}\n"
  
  return renderString

socket = soc.socket(soc.AF_INET, soc.SOCK_STREAM)
socket.connect((HOST, PORT))

reset()

while True:
  # Decide a new direction
  if random.randrange(0, 100) < 50:
    # 50% chance of changing direction (includes forward)
    heading = (heading + random.randrange(-1, 2)) % 4
  else:
    # 50% chance of staying in the same direction
    pass

  # Move snake
  move(heading)

  # Check if snake has hit itself
  collided = False
  for part in snakeArray:
    if part.life != snakeArray[-1].life and part.x == snakeArray[-1].x and part.y == snakeArray[-1].y:
      # Reset and restart loop
      reset()
      collided = True
      break
    
  if collided:
    print("collided")
    continue

  # Check if snake has hit the screen border
  if snakeArray[-1].x < 0 or snakeArray[-1].x >= MAX_X or snakeArray[-1].y < 0 or snakeArray[-1].y >= MAX_Y:
    # Reset and restart loop
    reset()
    continue

  # Age snake
  tick()

  # Render the screen
  output = ""
  for part in snakeArray:
    output += renderPart(part)

  # Send output to screen
  socket.sendall(output.encode())

  time.sleep(.5)
  