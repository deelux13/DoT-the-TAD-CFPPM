# -*- coding: utf-8 -*-
"""
Created on Fri Nov  6 09:56:44 2020

@author: Glen
"""

import pyautogui
from multiprocessing import Process


class ClickerProcess(Process):
    """Process that contains all the clicking logic and possibly all
    the menu too."""

    def __init__(self):
        pass




"""

class Aid(Process):
    def __init__(self, Hood='No'):
        super(Aid, self).__init__()
        self.moveLeftallimage = "Skip left arrow.png"
        self.moveRightpageimage = "Page right arrow.png"
        self.aidimage = "Aid button.png"
        self.tavernVisitimage = "Visit Tavern.png"
        self.Hood = Hood
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


    def run(self):
        if self.Hood == 'No':
            tabs = ["Guild", "Friend"]
        elif self.Hood == 'Yes':
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


class collect(Process):
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

"""