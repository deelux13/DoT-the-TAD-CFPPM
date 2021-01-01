# -*- coding: utf-8 -*-
"""
Created on Fri Nov  6 09:56:44 2020

@author: Glen
"""

import pyautogui as pyg
from multiprocessing import Process
import LZutils
import time
import ErrorLZ
import GameInterface


class Brains(Process):
    """Process that contains all the clicking logic and possibly all
    the menu too.
    
    This only contains the brains of when to what. i think. that actual clicking logic  will be is contained in the game interface. 
    The interface knows where things are and clicks them. this process brains is the what to click when brains and monitors keyboard input.
    
    """

    def __init__(self, ThreadHandler):
        super(Brains, self).__init__()

        self.keyQueue = ThreadHandler.keyQueue
        pyg.PAUSE = 0

    def UBQask(self):

        self.UBQtodo = 0
        test = True

        while test:
            ubqs = pyg.prompt(text='How many UBQs?')
            if ubqs is None:
                test = False
                break
            try:
                self.UBQtodo = int(ubqs)
                test = False
            except ValueError:
                pyg.alert(text="Not a number")

        self.UBQgivers = int(pyg.confirm(text='How many quest givers?',buttons=['1', '2', '3']))


    def Hood(self):
        """"Pull yes/no for hood aid and populate aidtab list"""
        pyg.alert(text='Hood will not be aided')
        self.tabs = ["Guild", "Friend"]
        if pyg.prompt(text='Do you want to aid the available aids in your hood? type "YES" only if you\'re done being the TAD') == 'YES':
            self.tabs.append("Hood")
        # not sure how to add hood option, don't want it to accidentally trigger for DoT


    def data(self):
        self.DataCol = pyg.confirm(text='Do UBQ timing? aid is currently skipped if this is chosen', buttons=["Yes", "No"])

    def AidClickAll(self, image, confidence=0.9):
        """Clicking routine for the Aid method."""
        thing = pyg.locateOnScreen(image, confidence=confidence)
        if thing is None:
            return False
        hits = 0
        while thing is not None:
            pos = pyg.center(thing)
            LZutils.goClick(pos)
            time.sleep(0.8)
            hits += 1
            if hits > 10:
                LZutils.findClick("Page step right.png")
                time.sleep(0.3)
            if hits > 15:
                return True
            # TODO this really needs to be better.
            thing = pyg.locateOnScreen(image, confidence=confidence)
            # last thing in the loop is to prep it for next loop
        return True

    def Aid(self):
        """Go aid everyone you want to."""
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
                    LZutils.FindGoClickAll(self.tavernVisitimage,
                                           confidence=0.95, delay=0.8)

                edge = pyg.locateOnScreen(
                    'left edge of player aid board.png', confidence=0.85)
                end = pyg.locateOnScreen(
                    'Right edge of player aid board.png', confidence=0.85)
                # edge of top left in 10 down 5, to end
                if edge is None or end is None:
                    raise ErrorLZ.LZException("Aid board is not on screen")

                Checkregion = (edge[0]+10, edge[1]+5,
                               end[0], end[1]+end[3]-5-edge[1])
                # TODO what is this mess?

                im = pyg.screenshot(region=Checkregion)
                LZutils.findClick(self.moveRightpageimage)
                time.sleep(2)
                # TODO thses folowing iffs are useless since the failed aid
                # logic is in the ClickAll
                if pyg.locateOnScreen("Visit Not Possible.png",
                                            confidence=0.85) is not None:

                    LZutils.goClick("No Visit Okay button.png")

                if pyg.locateOnScreen("Failed polish.png",
                                            confidence=0.85) is not None:
                    LZutils.goClick("No Visit Okay button.png")

                if not Aided:
                    time.sleep(2)

                    testerDat = pyg.locateOnScreen(im,
                                                         confidence=0.95)
                    time.sleep(1)
                    # Cuz if we find the same shot, the end of the list
                    # has been reached and it hasn't scrolled
                    # Crap what about
                    if testerDat is not None:
                        loop = False

    def Collect(self):
        """Grab all the finished coins and supplies, then reset productions.

        Returns
        -------
        None.

        """
        time.sleep(3)
       # print("start")
        i = 0
        while i < 2:
            for Img in self.collections:
                LZutils.FindGoCollectAll(Img, confidence=0.57)
                time.sleep(1)
            time.sleep(5)
            LZutils.RestartProductions()
            i += 1

    


    def run(self):

        self.Hood()
        self.UBQask()
        self.data()
        print("Clicker process run")
        pyg.alert("Starting")
        tic = time.perf_counter()
        timeLoop = 0
        self.totalUBQ = self.UBQtodo #the wrong way to handle this. setting the objective one to the value of the one that changes.
        try:
            self.UBQ()
        except ErrorLZ.LZException:
            print("something went wrong in UBQ")


        # should make this be the not found error but didn't go dig to find it

        # runs however many ubqs were told in __INIT__
        toc = time.perf_counter()
        if self.DataCol == 'Yes':
            pyg.alert(text=f'{self.totalUBQ} UBQs took {toc - tic:0.4f} seconds i think', title=f'{(toc - tic)//60} minutes maybe')
        print(f'{self.totalUBQ} UBQs took {toc - tic:0.4f} seconds i think {(toc - tic)//60} minutes maybe')

        while True:
            self.Collect()
            if timeLoop % 13 == 0:
                try:
                    self.Aid()
                except ErrorLZ.LZException:
                    timeLoop -= 1


            ready = True
            while ready:
                time.sleep(15)
                if pyg.locateOnScreen("coin to collect.png", confidence=0.6) is not None or pyg.locateOnScreen("Supply collect.png", confidence=0.6) is not None:
                    ready = False

            timeLoop += 1
            time.sleep(15)
