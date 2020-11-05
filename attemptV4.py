# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 21:12:16 2020

@author: Glen
"""


import pyautogui
import multiprocessing
import time
import sys
from pynput.keyboard import Key, Listener

class Threader():
    """Makes a new thread to listen for a double esc and stops thread

    """
    Running = [0]
    Threads = []
    Interrupts = []

    def __init__(self):
        print("threader init")
        if self.Running[0] > 0:
            raise AlreadyExisting("Threader has already been instanced")
        self.Running[0] = 1

    def __enter__(self):
        return self


    def addThread(self, Thread):
        print("Threader add thread")
        Thread.start()
        self.Threads.append(Thread)


    def Trigger(self, target, args=None):
        print("Threader trigger cent")
        print("target = ", target)
        # I feel like the central process MAYBE could use a with.. but idk
        CentralProcess = multiprocessing.Process(target=target, daemon=True)
        self.addThread(CentralProcess)
        Int = Interrupt(CentralProcess)
        Int.Listen()




    def __exit__(self, problem, value, trace):
        print('Threader problem LZ', problem)
        self.Running[0] = 0
        for thing in self.Threads:
            thing.terminate()



class Interrupt():
    def __init__(self, target):
        self.prevKey = Key.enter
        self.target = target

    def keyUp(self, key):
        print(key)
        # pyautogui.move(100,100)

        if key == Key.esc and key == self.prevKey:
            print("aborting")
            self.listener.stop()
            self.Running = False
            self.target.terminate()
# TODO use target.is_alive()
        self.prevKey = key

    def Listen(self):
        print("Interrupt Start Listen()")

        with Listener(on_release=self.keyUp) as self.listener:
            self.listener.join()
        self.Running = True
        print('hellp')


    def Stop(self):
        self.listener.stop()
        self.Running = False
        self.Thread.stop()









class LZException(Exception):
    def __init__(self, context):
        self.context = context

class AlreadyExisting(Exception):
    def __init__(self, context):
        self.context = context
        print(context)

class InterruptLZ(Exception):
    pass


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



class Aid():
    def __init__(self):
        self.moveLeftallimage = "Skip left arrow.png"
        self.moveRightpageimage = "Page right arrow.png"
        self.aidimage = "Aid button.png"
        self.tavernVisitimage = "Visit Tavern.png"
        # these are not all of the images used...


    def AidClickAll(image, confidence=0.9):
        thing = pyautogui.locateOnScreen(image, confidence=confidence)
        if thing is None:
            return False
        hits = 0
        while thing is not None:
            pos = pyautogui.center(thing)
            goClick(pos)
            time.sleep(0.05)
            thing = pyautogui.locateOnScreen(image, confidence=confidence)
            hits += 1
            if hits > 7:
                findClick("Page step right.png")
        return True


    def go(self, Hood='No'):
        if Hood == 'No':
            tabs = ["Guild", "Friend"]
        elif Hood == 'Yes':
            tabs = ["Hood", "Guild", "Friend"]
        else:
            raise LZException("Aid.Go improper hood arg")



        for place in tabs:  # this is the loop that goes over each tab
            findClick("{} tab.png".format(place), confidence=0.9)
            time.sleep(1)
            findClick(self.moveLeftallimage)
            time.sleep(1)
# The while is until the end of the list of people is reached
            loop = True
            while loop:
                Aided = self.AidClickAll(self.aidimage)

                if place == "Friend":
                    FindGoClickAll(self.tavernVisitimage, confidence=0.95)
# TODO need some sort of timeout for the Failed to Aid problem...


                edge = pyautogui.locateOnScreen(
                    'left edge of player aid board.png', confidence=0.85)
                end = pyautogui.locateOnScreen(
                    'Right edge of player aid board.png', confidence=0.85)
                # edge of top left in 10 down 5, to end
                if edge is None or end is None:
                    raise LZException("Aid board is not on screen")



                Checkregion = (edge[0]+10, edge[1]+5,
                               end[0], end[1]+end[3]-5-edge[1])

                im = pyautogui.screenshot(imageFilename='tempAidcheck.png',
                                          region=Checkregion)
                findClick(self.moveRightpageimage)
                time.sleep(1)
                if pyautogui.locateOnScreen("Visit Not Possible.png",
                                        confidence=0.85) is not None:

                    goClick("No Visit Okay button.png")

                if pyautogui.locateOnScreen(
                                        "Failed polish.png", confidence=0.85) is not None:
                    goClick("No Visot Okay button.png")


                if not Aided:

                    testerDat = pyautogui.locateOnScreen(im,
                                                 confidence=0.95)
                    time.sleep(1)
                        # Cuz if we find the same shot, the end of the list
                        # has been reached and it hasn't scrolled
                        # Crap what about
                    if testerDat != None:
                        loop = False


class collect():
    def __init__(self):
        self.coinImg = "coin to collect.png"
        self.coinStarImg = "coin to collect motivated.png"
        self.suppliesImg = "Supply collect.png"
        self.buildingSleepImg = "building sleeping.png"
        self.min5Production = "5 min production.png"
        self.suppliesStarImg = "supplies motivated.png"
        self.collections = [self.coinImg, self.coinStarImg,
                            self.suppliesImg, self.suppliesStarImg]

    def Go(self):
        time.sleep(3)
        print("start")
        i = 0
        while i < 2:
            for Img in self.collections:
                FindGoCollectAll(Img, confidence=0.57)
                time.sleep(1)
            time.sleep(5)
            RestartProductions()
            i += 1


class UBQ():
    def __init__(self):
        self.QuestOpenImg = "Story quest.png"
        self.collect = "Collect button.png"
        self.payImg = "Pay button.png"
        self.UBQImg = "UBQ identify.png"
        self.abortImg = "Abort button.png"


    def go(self, loops):
        print(loops)
        if loops is None:
            return False

        findClick(self.QuestOpenImg, 0.6, (0,-5))
        i = 0
        while i < loops:
            time.sleep(1)
            if pyautogui.locateOnScreen(self.UBQImg, confidence=0.8, minSearchTime=1) is not None:
                FindGoClickAll(self.payImg)
                time.sleep(1)
                findClick(self.collect, confidence=0.7)
                i += 1
            else:
                time.sleep(1)
                findClick(self.abortImg)

def CentralProcessLZ():


        print("central Main")
        #pyautogui.alert("Starting")
        timeLoop = 0

        while True:
            collect().Go()
            if timeLoop % 13 == 0:
                try:
                    Aid().go()
                except LZException:
                    timeLoop -= 1


            ready = True
            while ready:
                time.sleep(10)
                if pyautogui.locateOnScreen("coin to collect.png", confidence=0.6) is not None or pyautogui.locateOnScreen("Supply collect.png", confidence=0.6) is not None:
                    ready = False

            timeLoop += 1
            time.sleep(15)

# thiss  just needs to be somewhere else so i can import everything from this file and then multiprocessing might work
