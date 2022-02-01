from ast import Str
import os
import socket as soc
import time
import random

HOST = "skarm.ludd.ltu.se"
PORT = 1337

# Size of the screen: 1024x576
SCREEN_MAX_X = 1024
SCREEN_MAX_Y = 576

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
age = 1
heading = 1     # 0 = up, 1 = right, 2 = down, 3 = left

def reset():
  age = 1
  snakeArray[:] = [SnakePart(SCREEN_MAX_X/2, SCREEN_MAX_Y/2, age)]

def tick():
  for (i, part) in enumerate(snakeArray):
    part.age()
    if part.life == 0:
      del snakeArray[i]

def move(direction):
  # Move snake forward by adding a new snakepart with age + 1 (to cancel out the coming tick)
  if direction == 0:
    snakeArray.insert(0, SnakePart(snakeArray[-1].x, snakeArray[-1].y - 1, age + 1))
  elif direction == 1:
    snakeArray.insert(0, SnakePart(snakeArray[-1].x + 1, snakeArray[-1].y, age + 1))
  elif direction == 2:
    snakeArray.insert(0, SnakePart(snakeArray[-1].x, snakeArray[-1].y + 1, age + 1))
  elif direction == 3:
    snakeArray.insert(0, SnakePart(snakeArray[-1].x - 1, snakeArray[-1].y, age + 1))

def renderPart(part):
  renderString = ""
  color = Str(random.randrange(0, 10))*6 # Random greyscale color
  # Make a square
  for x in range(0, 20):
    for y in range(0, 20):
      # Draw border white
      if x == 0 or y == 0 or x == 19 or y == 19:
        renderString += f"PX {part.x + x} {part.y + y} FFFFFF\n"
      else:
        renderString += f"PX {part.x + x} {part.y + y} {color}\n"

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
  for part in snakeArray:
    if part.x == snakeArray[0].x and part.y == snakeArray[0].y:
      # Reset and restart loop
      reset()
      continue

  # Check if snake has hit the screen border
  if snakeArray[0].x < 0 or snakeArray[0].x >= SCREEN_MAX_X or snakeArray[0].y < 0 or snakeArray[0].y >= SCREEN_MAX_Y:
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
  