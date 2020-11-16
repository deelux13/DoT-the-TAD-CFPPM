# -*- coding: utf-8 -*-
"""
Created on Fri Nov  6 10:01:26 2020

@author: Glen
"""

import pyautogui
import time
import ErrorLZ


def swapVariables(a,b):
    return b, a


def findAndMove(file, confidence=.9):
    pyautogui.moveTo(pyautogui.center(pyautogui.locateOnScreen(file, confidence=confidence)))


def findAllList(file, confidence=0.92):
    """Find All, no overlap detection only safe with first and last.

    Parameters
    ----------
    file : Img to find
    confidence : float. The default is 0.92.

    Returns
    -------
    list of all regions found

    """
    gen = pyautogui.locateAllOnScreen(file, confidence=confidence)
    rect = next(gen, None)
    spots = []
    if rect is not None:
        spots.append(rect)
        next(gen, None)
        #this puts the first one on
    else:
        return None
    # returns that none were found

    while rect is not None:

        spots.append(rect)
        next(gen, None)
    return spots


def spotWithin(first, second):
    """


    Parameters
    ----------
    first : TYPE
        DESCRIPTION.
    second : TYPE
        DESCRIPTION.

    Returns
    -------
    Bool: true if they overlap

    """

def findRBGarea():
    cursor = pyautogui.position()
    box = [cursor[0] - 15, cursor[1] - 15, cursor[0]+15 , cursor[1] + 15] # top left x,y and bottom right x,y
    Color = [[], [], []] # color [0] Red, [1] Green, [2] Blue
    for x in range(box[0], box[2], 3):
        for y in range(box[1], box[3], 3):
            r, g, b = pyautogui.pixel(x, y)
            Color[0].append(r)
            Color[1].append(g)
            Color[2].append(b)
    # TODO need like an average or something to view


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
        raise ErrorLZ.LZException("Pull image aborted.")
    name = name + ".png"
    if name.startswith('.'):
        print("Empty input")
        raise ErrorLZ.LZException("No name inputted.")

    print(region)
    time.sleep(.02)
    im = pyautogui.screenshot(imageFilename=name, region=region)
    return im


class building():
    pass


def FindGoClickAll(image, confidence=0.9, delay=0.1):
    thing = pyautogui.locateOnScreen(image, confidence=confidence)
    if thing is None:
        return False
    found = 0
    while thing is not None:
        goClick(pyautogui.center(thing))
        time.sleep(delay)
        thing = pyautogui.locateOnScreen(image, confidence=confidence)
        found += 1

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
        except ErrorLZ.LZException:
            print("5 min not there")
        time.sleep(1.5)
        thing = pyautogui.locateOnScreen("building sleeping.png", confidence=0.5)
    return True




def findClick(image, confidence=.9, offset=(0,0)):
    rect = pyautogui.locateOnScreen(image, confidence=confidence)
    if rect == None:
        raise ErrorLZ.LZException("'{}' Not found on screen".format(image))
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


