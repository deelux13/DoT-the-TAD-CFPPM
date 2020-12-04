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
import GameInterface


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
        self.supQuestImg = "Supplies quest identify.png"
        self.coinQuestImg = "Coin quest identify.png"
        self.UBQexitImg = 'UBQ exit button.png'
        self.closeImg = "Close button.png"
        self.data()
        pyautogui.PAUSE = 0

    def UBQask(self):

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

        self.UBQgivers = int(pyautogui.confirm(text='How many quest givers?',buttons=['1', '2', '3']))


    def Hood(self):
        """"Pull yes/no for hood aid and populate aidtab list"""
        pyautogui.alert(text='Hood will not be aided')
        self.tabs = ["Guild", "Friend"]
        if pyautogui.prompt(text='Do you want to aid the available aids in your hood? type "YES" only if you\'re done being the TAD') == 'YES':
            self.tabs.append("Hood")
        # not sure how to add hood option, don't want it to accidentally trigger for DoT


    def data(self):
        self.DataCol = pyautogui.confirm(text='Do UBQ timing? aid is currently skipped if this is chosen', buttons=["Yes", "No"])

    def AidClickAll(self, image, confidence=0.9):
        """Clicking routine for the Aid method."""
        thing = pyautogui.locateOnScreen(image, confidence=confidence)
        if thing is None:
            return False
        hits = 0
        while thing is not None:
            pos = pyautogui.center(thing)
            LZutils.goClick(pos)
            time.sleep(0.8)
            hits += 1
            if hits > 10:
                LZutils.findClick("Page step right.png")
                time.sleep(0.3)
            if hits > 15:
                return True
            # TODO this really needs to be better.
            thing = pyautogui.locateOnScreen(image, confidence=confidence)
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

                edge = pyautogui.locateOnScreen(
                    'left edge of player aid board.png', confidence=0.85)
                end = pyautogui.locateOnScreen(
                    'Right edge of player aid board.png', confidence=0.85)
                # edge of top left in 10 down 5, to end
                if edge is None or end is None:
                    raise ErrorLZ.LZException("Aid board is not on screen")

                Checkregion = (edge[0]+10, edge[1]+5,
                               end[0], end[1]+end[3]-5-edge[1])
                # TODO what is this mess?

                im = pyautogui.screenshot(region=Checkregion)
                LZutils.findClick(self.moveRightpageimage)
                time.sleep(2)
                # TODO thses folowing iffs are useless since the failed aid
                # logic is in the ClickAll
                if pyautogui.locateOnScreen("Visit Not Possible.png",
                                            confidence=0.85) is not None:

                    LZutils.goClick("No Visit Okay button.png")

                if pyautogui.locateOnScreen("Failed polish.png",
                                            confidence=0.85) is not None:
                    LZutils.goClick("No Visit Okay button.png")

                if not Aided:
                    time.sleep(2)

                    testerDat = pyautogui.locateOnScreen(im,
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
        print("start")
        i = 0
        while i < 2:
            for Img in self.collections:
                LZutils.FindGoCollectAll(Img, confidence=0.57)
                time.sleep(1)
            time.sleep(5)
            LZutils.RestartProductions()
            i += 1

    def UBQsetup(self):
        """Put the supply and coin gather quests at the top.
        
        Please only call this with quest already open.

        This is very much not set up to do 2 quests, but this is the harder
        implementation.The other one can be added via some copypasta.

        Returns
        -------
        None.

        """
        # print("starting setup, {} givers".format(self.UBQgivers))
        LZutils.findClick(self.QuestOpenImg, 0.6, (0, -5))
        times = self.UBQgivers - 1
        spots = [self.supQuestImg, self.coinQuestImg]
        if times == 0:# one giver
            nm = 0
            while nm < 5:
                pyautogui.scroll(-10)
                nm += 1
            return

        # 2 givers
        if times == 1:
            LZutils.findAndMove(self.abortImg, confidence=0.9)
            time.sleep(0.2)
            i = 0
            while i < 10:
                pyautogui.scroll(10) # these scrolls may break it
                i += 1
            check = None
            while check is None:

                check = pyautogui.locateOnScreen(self.coinQuestImg, confidence=0.9)
                # is the eone we are looking for on screen?
                if check is None:
                    self.Face.ClickTopAbort() # if not, then click abort
                time.sleep(0.3)
            pyautogui.alert("coin found i think")
            if pyautogui.center(check)[1] > pyautogui.center(pyautogui.locateOnScreen(self.abortImg, confidence=0.95))[0]:
                '''then the bottom RQ is one we want, and we just abort the top
                if the center of the found one is lower (more positive) than the abort button, then the top abort doesn't belong to the 
                '''
                self.Face.ClickTopAbort()
                time.sleep(0.3)
            # now ours is the top one
            while i < 20:
                pyautogui.scroll(-10)
                i += 1
            print("2 giver setup end")
            return



        # 3 givers active
        if times == 2:
            # lock first quest
            LZutils.findAndMove(self.abortImg, confidence=0.8)
            time.sleep(0.2)
            while i < 10:
                pyautogui.scroll(10) # these scrolls may break it
                i += 1
            
            aborts = pyautogui.locateAllOnScreen(self.abortImg, confidence=0.7)
            check = None
            while check is None:
                """
                # get the first on on the screen
                # i figure i'm missing something, but i'm assuming that we don't
                have one of them in the bottom slot it shouldnt be normally, since
                we normally just finished a UBQ in the bottom slot
                """
                check = pyautogui.locateOnScreen(self.supQuestImg)
                if check is None:
                    check = pyautogui.locateOnScreen(self.coinQuestImg)
                if check is None:
                    LZutils.findClick(self.abortImg, confidence=0.7)
                time.sleep(0.3)
            #now we have one onscreen v vb
            if pyautogui.center(check)[1] > pyautogui.center(pyautogui.locateOnScreen(self.abortImg, confidence=0.7))[1]:
                #then the bottom RQ is one we want, and we just abotrt the top
                LZutils.findClick(self.abortImg, confidence=0.7)
                time.sleep(0.3)
            # now the top one is the one we want
            i = 0
            while i < 100:
                if pyautogui.locateOnScreen(self.supQuestImg, confidence=0.7) and pyautogui.locateOnScreen(self.coinQuestImg, confidence=0.7):
                    while i < 10:
                        pyautogui.scroll(-10) # these scrolls may break it
                        i += 1
            
                    return
                aborts = pyautogui.locateAllOnScreen(self.abortImg, confidence=0.95)
                next(aborts)
                spot = next(aborts)

                LZutils.goClick(pyautogui.center(spot))
                time.sleep(0.3)


            raise ErrorLZ.LZException("Two quests not found")


## I really could do only a region check if its a performance issue
# seems like the FOE performance is the real hangup at least on ubu-dev
    def UBQ(self):
        # DO i need to check that UBQtodo is a valid input? should already be
        try:
            LZutils.findClick(self.UBQexitImg, confidence=0.8)
            print("try")
        except ErrorLZ.LZException:
            pass # not needed for now?
        finally:
            self.Face = GameInterface.Interface()
            LZutils.findClick(self.QuestOpenImg, 0.6, (0,-5)) #think that offsets broken.
            print("finally")
        print("onnly open")
        time.sleep(1)
        center = pyautogui.locateCenterOnScreen(self.abortImg, confidence=0.7)
        print("pre UBQ setup")
        self.UBQsetup()
        print("post UBQ setup")
        while self.UBQtodo > 0:
            time.sleep(0.5)

            if LZutils.FindGoClickAll(self.payImg):
                time.sleep(0.3)
                i = 1
                while i >= 0:
                    # checks twice and scrolls
                    found = LZutils.FindGoClickAll(self.collect,
                                                   confidence=0.8)
                    if found > i:
                        time.sleep(0.3)
                        self.UBQsetup()
                        break
                    # first collect expects one, any more triggers the setup
                    # second scrolls up but expects none.
                    try:
                        print('tried')
                        LZutils.findClick(self.closeImg)
                        pyautogui.moveTo(center)
                    except ErrorLZ.LZException:
                        pass
                    finally:
                        i -= 1
                        j = 0
                        while j < 5:
                            pyautogui.scroll(10) # these scrolls may break it
                            j += 1
                    

                self.UBQtodo -= 1
                time.sleep(0.3)
                nm = 0 
                while nm < 7:
                    pyautogui.scroll(-10) # these scrolls may break it
                    nm += 1
                
            else:

                try:
                    self.Face.ClickBottomAbort()
                    # should click the bottom abort button
                    # returns false if it doesn't click. but i don't care right now.

                except ErrorLZ.LZException:
                    pyautogui.alert(text='no abort found')
                    continue
                except OSError or TypeError:
                    print("issues with UBQ finding abort button")

                    continue
        LZutils.findClick(self.UBQexitImg, confidence=0.8)



    def run(self):

        print("Clicker process run")
        pyautogui.alert("Starting")
        tic = time.perf_counter()
        timeLoop = 0
        totalUBQ = self.UBQtodo
        try:
            self.UBQ()
        except ErrorLZ.LZException:
            print("something went wrong in UBQ")


        # should make this be the not found error but didn't go dig to find it

        # runs however many ubqs were told in __INIT__
        toc = time.perf_counter()
        if self.DataCol == 'Yes':
            pyautogui.alert(text=f'{totalUBQ} UBQs took {toc - tic:0.4f} seconds i think', title=f'{(toc - tic)//60} minutes maybe')

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
                if pyautogui.locateOnScreen("coin to collect.png", confidence=0.6) is not None or pyautogui.locateOnScreen("Supply collect.png", confidence=0.6) is not None:
                    ready = False

            timeLoop += 1
            time.sleep(15)
