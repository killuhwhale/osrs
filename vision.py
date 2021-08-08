import cv2 as cv
from time import time
import numpy as np
import os
import pyautogui
import subprocess

import mss
import mss.tools





window_title = 'RuneLite'
get_window_cmd = f'xdotool search --name {window_title}'


def c(cmd):
  '''Runs a bash command.'''
  return subprocess.run(cmd.split(' '), check=True, encoding='utf-8', capture_output=True).stdout.strip()

def getRunliteWindow():
  res = c(get_window_cmd)
  return [int(item) for item in res.split("\n")][-1]

WIN = getRunliteWindow()

def get_region():
  return c(f'xdotool getwindowgeometry {WIN}')

def set_window_size(w, h):
  c(f'xdotool windowsize {WIN} {w} {h}')

def moveWindow(x, y):
  c(f'xdotool windowmove {WIN} {x} {y}')


def get_ss():
  screen, region = extract_region_data(get_region())
  print(f'Screen: {screen}')

  # return pyautogui.screenshot(region=region)
  with mss.mss() as sct:
    # The screen part to capture
    monitor = {"top": region[0], "left": region[1], "width": region[2], "height": region[3]}
    # output = "sct-{top}x{left}_{width}x{height}.png".format(**monitor)

    # Grab the data
    return sct.grab(monitor)


def extract_region_data(data):
  lines = data.split('\n')
  pos_screen = lines[1].split(" ")
  screen = pos_screen[-1].replace(")","")

  x, y = pos_screen[3].split(',')
  w, h = lines[2].split(' ')[-1].split('x')

  return [int(screen), (int(x), int(y), int(w), int(h),) ]

loop_time = time()
def run():
  global loop_time
  while(True):
    ss = get_ss()
    ss = np.array(ss)
    # ss = cv.cvtColor(ss, cv.COLOR_RGB2BGR)

    cv.imshow('OpenCV', ss)
    print(f'FPS: {1/(time() - loop_time)}')
    loop_time = time()

    if cv.waitKey(1) == ord('q'):
      cv.destroyAllWindows()
      break



if __name__ == "__main__":
  run()
  # set_window_size(1000, 300)
  # moveWindow(0, 0)
  # get_ss()
