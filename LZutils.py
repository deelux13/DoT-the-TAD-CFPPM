# -*- coding: utf-8 -*-
"""
Created on Fri Nov  6 10:01:26 2020

@author: Glen
"""

import pyautogui
import time
import ErrorLZ
from statistics import mean


def swapVariables(a,b):
    return b, a


def findAndMove(file, confidence=.9):
    pyautogui.moveTo(pyautogui.center(pyautogui.locateOnScreen(file, confidence=confidence)))

def OverlapDetect(first, second, refImg):
  #  print("util first, ", first)
  #  print("util 2nd, ", second)
    Width, Height = refImg.size
    if second[0] - first[0] < Width and second[1] - first[1] < Height:
        return True
    else:
        return False


def waitfor(img, region, confidence=0.7):
    counter = 0
    while pyautogui.locateOnScreen(img, minSearchTime=0.05, confidence=confidence, region=region) is None:
        time.sleep(0.03)
        counter += 1
        if counter > 20:
            try:
                findClick("Abort button.png", confidence=0.9)
                time.sleep(3)
            except ErrorLZ.LZException:
                time.sleep(4)
    return

def waitforVanish(img, region, confidence=0.8):
    counter = 0
    while pyautogui.locateOnScreen(img, confidence=confidence, region=region):
        time.sleep(0.03)
        counter += 1
        if counter > 60:
            return False
    return

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

def findRGBarea():
    cursor = pyautogui.position()
    time.sleep(3)
    box = [cursor[0] - 10, cursor[1] - 10, 20, 20] # top left x,y and bottom right x,y
    img = pyautogui.screenshot(region=box)
    Color = [[], [], []] # color [0] Red, [1] Green, [2] Blue
    img.getpixel((2, 2))
    for x in range(0, box[2], 3):

        for y in range(0, box[3], 3):
            
            r, g, b = img.getpixel((x, y))
            Color[0].append(r)
            Color[1].append(g)
            Color[2].append(b)
    # TODO need like an average or something to view
    R = mean(Color[0])
    G = mean(Color[1])
    B = mean(Color[2])
    print(f'mean values R {R}, G {G}, B {B}')
    Rrange = set(Color[0])
    Grange = set(Color[1])
    Brange = set(Color[2])
    # red = (Rrange[0], Rrange[len(Rrange) - 2])
    # green = (Grange[0], Grange[len(Grange) - 2])
    # blue = (Brange[0], Brange[len(Brange) - 2])
    print(f'range of R {Rrange}, G {Grange}, B {Brange}')


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


def FindGoClickAll(image, confidence=0.9, delay=0.1, region=pyautogui.size()):
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


def addTuples(first, second):
    return tuple(map(sum, zip(first, second)))


def scroll(direction):
    '''
    scroll 
    direction is 1 or -1
    '''
    nm = 0 
    while nm < 7:
        pyautogui.scroll(direction * 10) # these scrolls may break it
        nm += 1


def FindGoCollectAll(image, confidence=0.8):
    thing = pyautogui.locateOnScreen(image, confidence=confidence)
    if thing is None:
        return False
    while thing is not None:
        pos = addTuples(pyautogui.center(thing), (0,40))
        goClick(pos)
        pyautogui.move(-100,-100, 0.1)
        time.sleep(0.1)
        thing = pyautogui.locateOnScreen(image, confidence=confidence)
    return True


def RestartProductions():
    thing = pyautogui.locateOnScreen("building sleeping.png", confidence=0.6)
    if thing is None:
        return False
    while thing is not None:
        pos = addTuples(pyautogui.center(thing), (0,45))
        goClick(pos)
        time.sleep(0.1)
        pyautogui.move(-30,-30)
        time.sleep(0.3)
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
    pos = addTuples(pyautogui.center(rect), offset)
   # print(pos)
    goClick(pos)

#i really don't think its worth my effort to make a function for 2 lines...
def goClick(pos):
    """takes location tuple"""

    pyautogui.moveTo(pos, None, 0.001, pyautogui.easeInOutQuad)
    # time.sleep(.3)
    #this is inconsisten idk if sleep helps

    pyautogui.click(        )


