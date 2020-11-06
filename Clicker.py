# -*- coding: utf-8 -*-
"""
Created on Fri Nov  6 09:56:44 2020

@author: Glen
"""

import pyautogui
from multiprocessing import Process
import LZutils
import time
import ErrorLZ


class ClickerProcess(Process):
    """Process that contains all the clicking logic and possibly all
    the menu too."""

    def __init__(self):
        super(ClickerProcess, self).__init__()
        self.moveLeftallimage = "Skip left arrow.png"
        self.moveRightpageimage = "Page right arrow.png"
        self.aidimage = "Aid button.png"
        self.tavernVisitimage = "Visit Tavern.png"
        self.Hood()
        self.coinImg = "coin to collect.png"
        self.coinStarImg = "coin to collect motivated.png"
        self.suppliesImg = "Supply collect.png"
        self.buildingSleepImg = "building sleeping.png"
        self.min5Production = "5 min production.png"
        self.suppliesStarImg = "supplies motivated.png"
        self.collections = [self.coinImg, self.coinStarImg,
                            self.suppliesImg, self.suppliesStarImg]
        self.QuestOpenImg = "Story quest.png"
        self.collect = "Collect button.png"
        self.payImg = "Pay button.png"
        self.UBQImg = "UBQ identify2.png"
        self.abortImg = "Abort button.png"
        self.UBQask()

    def UBQask(self):
        pyautogui.alert(text='Really go fix the UBQask')
        self.UBQtodo = 0
        test = True

        while test:
            ubqs = pyautogui.prompt(text='How many UBQs?')
            if ubqs is None:
                test = False
                break
            try:
                self.UBQtodo = int(ubqs)
                test = False
            except ValueError:
                pyautogui.alert(text="Not a number")

    def Hood(self):
        """"Pull yes/no for hood aid and populate aidtab list"""
        pyautogui.alert(text='Seriously go do the logic for Hood init')


    def AidClickAll(self, image, confidence=0.9):
        thing = pyautogui.locateOnScreen(image, confidence=confidence)
        if thing is None:
            return False
        hits = 0
        while thing is not None:
            pos = pyautogui.center(thing)
            LZutils.goClick(pos)
            time.sleep(0.05)
            thing = pyautogui.locateOnScreen(image, confidence=confidence)
            hits += 1
            if hits > 7:
                LZutils.findClick("Page step right.png")
        return True



    def Aid(self):



        for place in self.tabs:  # this is the loop that goes over each tab
            LZutils.findClick("{} tab.png".format(place), confidence=0.9)
            time.sleep(1)
            LZutils.findClick(self.moveLeftallimage)
            time.sleep(1)
# The while is until the end of the list of people is reached
            loop = True
            while loop:
                Aided = self.AidClickAll(self.aidimage)

                if place == "Friend":
                    LZutils.FindGoClickAll(self.tavernVisitimage, confidence=0.95)



                edge = pyautogui.locateOnScreen(
                    'left edge of player aid board.png', confidence=0.85)
                end = pyautogui.locateOnScreen(
                    'Right edge of player aid board.png', confidence=0.85)
                # edge of top left in 10 down 5, to end
                if edge is None or end is None:
                    raise ErrorLZ.LZException("Aid board is not on screen")



                Checkregion = (edge[0]+10, edge[1]+5,
                               end[0], end[1]+end[3]-5-edge[1])

                im = pyautogui.screenshot(imageFilename='tempAidcheck.png',
                                          region=Checkregion)
                LZutils.findClick(self.moveRightpageimage)
                time.sleep(1)
                # TODO thses folowing iffs are useless since the failed aid logic is in the ClickAll
                if pyautogui.locateOnScreen("Visit Not Possible.png",
                                        confidence=0.85) is not None:

                    LZutils.goClick("No Visit Okay button.png")

                if pyautogui.locateOnScreen(
                                        "Failed polish.png", confidence=0.85) is not None:
                    LZutils.goClick("No Visit Okay button.png")


                if not Aided:

                    testerDat = pyautogui.locateOnScreen(im,
                                                 confidence=0.95)
                    time.sleep(1)
                        # Cuz if we find the same shot, the end of the list
                        # has been reached and it hasn't scrolled
                        # Crap what about
                    if testerDat != None:
                        loop = False


    def Collect(self):
        time.sleep(3)
        print("start")
        i = 0
        while i < 2:
            for Img in self.collections:
                LZutils.FindGoCollectAll(Img, confidence=0.57)
                time.sleep(1)
            time.sleep(5)
            LZutils.RestartProductions()
            i += 1



    def UBQ(self):
        print(self.UBQtodo)
        # DO i need to check that UBQtodo is a valid input? meh

        LZutils.findClick(self.QuestOpenImg, 0.6, (0,-5))

        while self.UBQtodo > 0:
            time.sleep(1)
            if pyautogui.locateOnScreen(self.UBQImg, confidence=0.6, minSearchTime=2) is not None:
                LZutils.FindGoClickAll(self.payImg)
                time.sleep(1)
                LZutils.findClick(self.collect, confidence=0.7)
                self.UBQtodo -= 1
            else:
                time.sleep(1)
                try:
                    LZutils.findClick(self.abortImg)
                except ErrorLZ.LZException:
                    break



    def run(self):


        print("Clicker process run")
        pyautogui.alert("Starting")
        timeLoop = 0
        self.UBQ()
        # runs however many ubqs were told in __INIT__

        # while True:
        #     self.Collect()
        #     if timeLoop % 13 == 0:
        #         try:
        #             self.Aid()
        #         except ErrorLZ.LZException:
        #             timeLoop -= 1


        #     ready = True
        #     while ready:
        #         time.sleep(15)
        #         if pyautogui.locateOnScreen("coin to collect.png", confidence=0.6) is not None or pyautogui.locateOnScreen("Supply collect.png", confidence=0.6) is not None:
        #             ready = False

        #     timeLoop += 1
        #     time.sleep(15)


"""









class UBQ():
    def __init__(self):


# thiss  just needs to be somewhere else so i can import everything from this file and then multiprocessing might work

"""