import pyautogui


def get_mouse_pos():
  while(True):
    print(pyautogui.position())

get_mouse_pos()