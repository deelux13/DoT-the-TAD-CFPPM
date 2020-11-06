# -*- coding: utf-8 -*-
"""
Created on Fri Nov  6 10:01:26 2020

@author: Glen
"""

import pyautogui


def swapVariables(a,b):
    return b, a


def findAndMove(file, confidence=.9):
    pyautogui.moveTo(pyautogui.center(pyautogui.locateOnScreen(file, confidence=confidence)))


def pullMousebox():
    """Return of user generated box.

    Uses an alert to allow the user to position it


    Returns
    -------
    4 int tuple of the box in region how pyauto uses
    left, top, width, height

    """
    Screen_size = pyautogui.size()
    pyautogui.alert("start Pos")
    x1, y1 = pyautogui.position()
    print(x1, ", ", y1)
    pyautogui.alert("end Pos")
    x2, y2 = pyautogui.position()
    print(x2, ', ', y2)
    if x1 > x2:
        x1, x2 = swapVariables(x1, x2)
    if y1 > y2:
        y1, y2 = swapVariables(y1, y2)
    return x1, y1, x2-x1, y2-y1


def pullImage():
    """Literally pulls a screenshot.

    returns the image, also saves it.
    """
    region = pullMousebox()

    name = pyautogui.prompt(text='What is this?')
    test = name
    print(name)
    print("\'", test, "\'")
    print("\'",  "\'")
    if name is None:
        print("cancelled")
        raise LZException("Pull image aborted.")
    name = name + ".png"
    if name.startswith('.'):
        print("Empty input")
        raise LZException("No name inputted.")

    print(region)
    time.sleep(.02)
    im = pyautogui.screenshot(imageFilename=name, region=region)
    return im


class building():
    pass


def FindGoClickAll(image, confidence=0.9):
    thing = pyautogui.locateOnScreen(image, confidence=confidence)
    if thing is None:
        return False
    while thing is not None:
        goClick(pyautogui.center(thing))
        time.sleep(0.05)
        thing = pyautogui.locateOnScreen(image, confidence=confidence)
    return True


def FindGoCollectAll(image, confidence=0.8):
    thing = pyautogui.locateOnScreen(image, confidence=confidence)
    if thing is None:
        return False
    while thing is not None:
        pos = pyautogui.center(thing) + (0,40)
        goClick(pos)
        pyautogui.move(-100,-100, 0.02)
        time.sleep(0.05)
        thing = pyautogui.locateOnScreen(image, confidence=confidence)
    return True


def RestartProductions():
    thing = pyautogui.locateOnScreen("building sleeping.png", confidence=0.6)
    if thing is None:
        return False
    while thing is not None:
        pos = pyautogui.center(thing) + (0,40)
        goClick(pos)
        pyautogui.move(-300,-300)
        time.sleep(0.5)
        try:
            findClick("5 min production.png")
        except LZException:
            print("5 min not there")
        time.sleep(1.5)
        thing = pyautogui.locateOnScreen("building sleeping.png", confidence=0.5)
    return True




def findClick(image, confidence=.9, offset=(0,0)):
    rect = pyautogui.locateOnScreen(image, confidence=confidence)
    if rect == None:
        raise LZException("'{}' Not found on screen".format(image))
    pos = pyautogui.center(rect)
    pos = pos + offset
    pyautogui.moveTo(pos, None, 0.3, pyautogui.easeInOutQuad)
    pyautogui.click(        )


#i really don't think its worth my effort to make a function for 2 lines...
def goClick(pos):
    """takes location tuple"""

    pyautogui.moveTo(pos, None, 0.2, pyautogui.easeInOutQuad)
    time.sleep(.5)

    pyautogui.click(        )


