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


def get_mouse_pos():
  while(True):
    print(pyautogui.position())

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

def findClickPositions(needle_img_path, haystack_img, threshold=0.5, debug_mode=None):

  # https://docs.opencv.org/4.2.0/d4/da8/group__imgcodecs.html
  # haystack_img = cv.imread(haystack_img_path, cv.IMREAD_UNCHANGED)
  needle_img = cv.imread(needle_img_path, cv.IMREAD_UNCHANGED)
  # Save the dimensions of the needle image
  needle_w = needle_img.shape[1]
  needle_h = needle_img.shape[0]

  # There are 6 methods to choose from:
  # TM_CCOEFF, TM_CCOEFF_NORMED, TM_CCORR, TM_CCORR_NORMED, TM_SQDIFF, TM_SQDIFF_NORMED
  method = cv.TM_CCOEFF_NORMED
  result = cv.matchTemplate(haystack_img, needle_img, method)

  # Get the all the positions from the match result that exceed our threshold
  locations = np.where(result >= threshold)
  locations = list(zip(*locations[::-1]))
  #print(locations)

  # You'll notice a lot of overlapping rectangles get drawn. We can eliminate those redundant
  # locations by using groupRectangles().
  # First we need to create the list of [x, y, w, h] rectangles
  rectangles = []
  for loc in locations:
      rect = [int(loc[0]), int(loc[1]), needle_w, needle_h]
      # Add every box to the list twice in order to retain single (non-overlapping) boxes
      rectangles.append(rect)
      rectangles.append(rect)
  # Apply group rectangles.
  # The groupThreshold parameter should usually be 1. If you put it at 0 then no grouping is
  # done. If you put it at 2 then an object needs at least 3 overlapping rectangles to appear
  # in the result. I've set eps to 0.5, which is:
  # "Relative difference between sides of the rectangles to merge them into a group."
  rectangles, weights = cv.groupRectangles(rectangles, groupThreshold=1, eps=0.5)
  #print(rectangles)

  points = []
  if len(rectangles):
      #print('Found needle.')

      line_color = (0, 255, 0)
      line_type = cv.LINE_4
      marker_color = (255, 0, 255)
      marker_type = cv.MARKER_CROSS

      # Loop over all the rectangles
      for (x, y, w, h) in rectangles:

          # Determine the center position
          center_x = x + int(w/2)
          center_y = y + int(h/2)
          # Save the points
          points.append((center_x, center_y))

          if debug_mode == 'rectangles':
              # Determine the box position
              top_left = (x, y)
              bottom_right = (x + w, y + h)
              # Draw the box
              cv.rectangle(haystack_img, top_left, bottom_right, color=line_color,
                            lineType=line_type, thickness=2)
          elif debug_mode == 'points':
              # Draw the center point
              cv.drawMarker(haystack_img, (center_x, center_y),
                            color=marker_color, markerType=marker_type,
                            markerSize=40, thickness=2)

      if debug_mode:
          cv.imshow('Matches', haystack_img)
          cv.waitKey()
          #cv.imwrite('result_click_point.jpg', haystack_img)

  return points


loop_time = time()
def run():
  global loop_time
  while(True):
    ss = get_ss()
    ss = np.array(ss)
    # cv.imshow('OpenCV', needle_im)

    pos = findClickPositions('test.png', ss, 0.5)
    print(pos)

    print(f'FPS: {1/(time() - loop_time)}')
    loop_time = time()


    if cv.waitKey(10000) == ord('q'):
      cv.destroyAllWindows()
      break



if __name__ == "__main__":
  # set_window_size(1000, 300)
  # moveWindow(0, 0)
  # run()
  # [(277, 187), (423, 223)]
  # get_ss()
  get_mouse_pos()