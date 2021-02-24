# -*- coding: utf-8 -*-
"""
Created on Fri Nov 13 14:25:25 2020

@author: Glen
"""
import pyautogui as pyg
import time
import LZutils
import ErrorLZ
from PIL import Image


def cycle():
    for y in range(0,120):
        print(pyg.pixel(66, y), " at y ", y)



class Interface():
    """The Game facing interface aka pixel finder and other utils."""
    def __init__(self, Brains):
        self.QuestOpenImg = "Story quest.png"
        self.collect = "Collect button.png"
        self.payImg = "Pay button.png"
        self.UBQImg = "UBQ identify2.png"
        self.abortImg = "Abort button.png"
        self.moveLeftallimage = "Skip left arrow.png"
        self.moveRightpageimage = "Page right arrow.png"
        self.aidimage = "Aid button.png"
        self.tavernVisitimage = "Visit Tavern.png"
        self.coinImg = "coin to collect.png"
        self.coinStarImg = "coin to collect motivated.png"
        self.suppliesImg = "Supply collect.png"
        self.buildingSleepImg = "building sleeping.png"
        self.min5Production = "5 min production.png"
        self.suppliesStarImg = "supplies motivated.png"
        self.QuestOpenImg = "Story quest.png"
        self.collect = "Collect button.png"
        self.payImg = "Pay button.png"
        self.UBQImg = "UBQ identify2.png"
        self.abortImg = "Abort button.png"
        self.supQuestImg = "Supplies quest identify.png"
        self.coinQuestImg = "Coin quest identify.png"
        self.UBQexitImg = 'UBQ exit button.png'
        self.closeImg = "Close button.png"
        self.BlueReward = "blueprint quest reward.png"
        
        self.collections = [self.coinImg, self.coinStarImg,
                            self.suppliesImg, self.suppliesStarImg]

        self.topLeft = pyg.locateOnScreen("Top Left corner.png", confidence=0.55)
        self.RightEdgeQuestX = self.topLeft[0] + 690
        self.QuestMiddle = self.RightEdgeQuestX//2
        self.topLeftX = self.topLeft[0]
        self.topLeftY = self.topLeft[1]
        self.aidBoardTopY = pyg.locateOnScreen("left edge of player aid board.png", confidence=0.9)[1]
        if self.topLeftX > 30:
            print("You really should maximize the screen...")
        print(pyg.PAUSE, "this is pyg default pause")
        self.screenReg = (0, 0, pyg.size()[0] -1, pyg.size()[1] - 1)
        pyg.PAUSE = 0
        # TODO i think i might need to add something here...

    def __enter__(self):
        return self




    def UBQmode(self, number,  givers):
        print("in ubq mode")
        self.givers = givers
        if number < 0 :
            infinite = True
        if number == 0 :
            print("none to do, 0 requested")
            return
        done = 0
        time.sleep(1)
        self.clickSpots = []
        self.clickTiming = []
        self.UBQsetup(givers) # should set it up.but doesn't leave it at a specific point in cycle
        
        center = pyg.locateCenterOnScreen(self.abortImg, confidence=0.7)
        Spots = self.BufferLocations("RQ banner.png")
        List = self.BufferLocations("Abort button.png")
        if len(List) < 1:
            time.sleep(1)
            return False
        button = List[len(List) - 1]
        
        importantBanner = Spots[len(Spots) - 1]
        Bookedge = pyg.locateCenterOnScreen("Questbook bottom corner.png", confidence=0.97)
        print(Bookedge)
        x = self.topLeftX
        y = importantBanner[1]
        width = Bookedge[0] - x
        height= Bookedge[1] - y
        reg = (x, y, width, height)
        print(reg)
        
        #start doing things
        self.UBQslow()
        try:
            LZutils.findClick(self.closeImg)
        except ErrorLZ.LZException:
            pass
        
        self.UBQfind(reg)
        try:
            LZutils.findClick(self.closeImg)
        except ErrorLZ.LZException:
            pass
        
        print(self.clickSpots)
        midPT = (self.screenReg[0]//2, self.screenReg[1]//2)
        cenBlueCheck = pyg.pixel(midPT[0], midPT[1])
        cycleNum = len(self.clickSpots)  # 1 for indexing not cuz less than in the while
        
        self.tic = time.perf_counter()
        # this reg is pretty clean using the top left castle, the RQ banner, and the bottom corner of the "book"
        while done / number < 1:
            # TODO this still needs help.... idk what i'm doing.
            questNum = 0
            while questNum < cycleNum:
                wait = 0
                PointI = self.clickSpots[questNum][0]
                ColorI = self.clickSpots[questNum][1]
                while not pyg.pixelMatchesColor(PointI[0], PointI[1], ColorI, tolerance=35):
                    wait += 1
                    if wait > 30:
                        try:
                            LZutils.findClick(self.closeImg)
                        except ErrorLZ.LZException:
                            pass
                        self.ClickBottomAbort(self.screenReg)
                        if wait > 45:
                            LZutils.FindGoClickAll(self.closeImg, confidence=0.8)
                            LZutils.FindGoClickAll(self.UBQexitImg, confidence=0.7)
                            return False
                    time.sleep(0.01)
                pyg.click(PointI[0], PointI[1])
                wait2 = 0
                while pyg.pixelMatchesColor(PointI[0], PointI[1], ColorI, tolerance=15):
                    time.sleep(0.05)
                    wait2 += 1
                    if wait2 > 15:
                        pyg.click(PointI[0], PointI[1])
                    if wait2 > 45:
                            LZutils.FindGoClickAll(self.closeImg, confidence=0.8)
                            LZutils.FindGoClickAll(self.UBQexitImg, confidence=0.7)
                            return False
                questNum += 1
                
            
            time.sleep(0.05)
            if pyg.pixelMatchesColor(midPT[0], midPT[1], cenBlueCheck, tolerance=20):
                try:
                    LZutils.findClick(self.closeImg)
                except ErrorLZ.LZException:
                    pass
            if LZutils.FindGoClickAll(self.collect, confidence=.85):
                self.UBQsetup(givers)
                self.UBQslow()
            if done % 7 == 0:
                toc = time.perf_counter()
                print(f'{done} of {number} still left to do {time.asctime( time.localtime(time.time()) )} || {(toc - self.tic)//60} minutes maybe.')
            done +=1
        return True    




## I really could do only a region check if its a performance issue
# seems like the FOE performance is the real hangup at least on ubu-dev
    def UBQslow(self):
        while True:
            time.sleep(3.5)
            if pyg.locateOnScreen(self.collect, confidence=0.8):
                if LZutils.FindGoClickAll(self.collect, region=self.screenReg) > 1:
                    self.UBQsetup(self.givers)
                    continue
                return
            if pyg.locateOnScreen(self.payImg, confidence=0.8):
                LZutils.FindGoClickAll(self.payImg, region=self.screenReg)
                continue
            self.ClickBottomAbort(self.screenReg)
            
            

    def UBQfind(self, reg):
        # could have a collect come in, but should be setup properly.
        while True:
            time.sleep(3.5)
            if pyg.locateOnScreen(self.collect, region=reg, confidence=0.8):
                if pyg.locateOnScreen("FP RQ reward.png", confidence=0.8):
                    LZutils.findClick(self.collect)
                    self.clickSpots = []
                    continue
                    # this is weird. but the collect button has like 10 pixel vertical shift and i make the pixel of interest 5 pixels lower, but the FP is the lowest so then it's too low.
                buttonC = pyg.locateCenterOnScreen(self.collect, region=reg, confidence=0.8)
                buttonC = (int(buttonC[0] - 30), int(buttonC[1]+5))
                color = pyg.pixel(buttonC[0], buttonC[1])
                print(color)
                self.clickSpots.append([buttonC, color])
                pyg.click(buttonC)
                
                return
            if pyg.locateOnScreen(self.payImg, region=reg, confidence=0.8):
                buttonC = pyg.locateCenterOnScreen(self.payImg, region=reg, confidence=0.8)
                buttonC = (int(buttonC[0]), int(buttonC[1]))
                color = pyg.pixel(buttonC[0], buttonC[1])
                print(color)
                self.clickSpots.append([buttonC, color])
                pyg.click(buttonC)
                continue
            if pyg.locateOnScreen(self.abortImg, region=reg, confidence=0.8):
                buttonC = pyg.locateCenterOnScreen(self.abortImg, region=reg, confidence=0.8)
                print(buttonC)
                buttonC = (int(buttonC[0] - 30), int(buttonC[1]))
                print(buttonC[0], " and ", buttonC[1])
                color = pyg.pixel(buttonC[0], buttonC[1])
                
                self.clickSpots.append([buttonC, color])
                pyg.click(buttonC)
                continue
            





    def BufferLocations(self, img):
        Img = Image.open(img)
        gen = pyg.locateAllOnScreen(Img, confidence=0.8)
        # need the size of the image to detect overlap
        Width, Height = Img.size
        List = []
        spot = next(gen, None)
        while spot is not None:
            List.append(spot)
            last = spot
            #stores previous

            spot = next(gen, None)
            if spot is None:
                return List
         #   print(last)
         #   print(spot)
            while LZutils.OverlapDetect(last, spot, Img): # cycles through new spots until one is found that doesn't overlap with last, or until end of generator.
                spot =  next(gen, None)
                if spot is None:
                    return List
                
                # need to check overlap. if overlap then we move to the next in the generator. if the generator runs out we just return what we have.
        return List # gen ran out without ending on an  overlap so we got this correctly.
            

# watchpay had to be added so it didn't abort too early befor the pay button was visible. especially becasuse the abort is oddly slow and triggers early. 
    def ClickBottomAbort(self, reg):
        """Literally just click the bottom abort, handles scrolling and all.
        
        This is rather slow. 

        Assumes that quest panel is open, cuz you dumb if you call this with
        it closed."""
        xSafe = self.topLeftX + 150
        yMid = self.topLeftY + 300
       # # print(self.topLeftY, "top offset")
        xAbort = int(self.topLeftX) + 270
        pyg.moveTo(xSafe, yMid, 0.3)
       # scroll does weird things
        ij = 0
        while ij < 5:
            ij += 1
            pyg.scroll(-20)
            
        List = self.BufferLocations("Abort button.png")
        if len(List) < 1:
            time.sleep(1)
            return False
        button = List[len(List) - 1]
        
        # Scroll down so that the bottom abort is visible.
        # if pyg.locateOnScreen('Pay button.png', confidence=0.9) and watchPay:
        #     return False
        # clicked = False
        #really not sure what i'm doing.
        # i think this just passes back false if the abort hasn't loaded  yet.
        
        # len - 1 give index of last on list
        
        center = pyg.center(button) + (0,5) 
        LZutils.goClick(center)
        time.sleep(3)
        # this offset totally doesn't work.
      #  print(center)
        #print(self.tic - time.perf_counter(), "pre click")
        
        
    def ClickAbortinReg(self, reg):
        center = pyg.locateCenterOnScreen("Abort button.png", confidence=0.8, region=reg)
        if center is None:
            return False
        LZutils.goClick(center)
        LZutils.waitforVanish("Abort button.png", reg)
        return True

# feels like iffy copypasta
    def ClickTopAbort(self, watchPay=False):
        xSafe = self.topLeftX + 150
        yMid = self.topLeftY + 500
        xAbort = self.topLeftX + 270
        pyg.moveTo(x=xSafe, y=yMid)
        
        ij = 0
        while ij < 5:
            ij += 1
            pyg.scroll(20)
        
        # Scroll down so that the bottom abort is visible.
        if pyg.locateOnScreen('Pay button.png', confidence=0.9) and watchPay:
            return False
        clicked = False
        #really not sure what i'm doing.
        # i think this just passes back false if the abort hasn't loaded  yet.
        List = self.BufferLocations("Abort button.png")
        if len(List) < 1:
            time.sleep(1)
            return False
        button = List[0]
        # len - 1 give index of last on list

        center = pyg.center(button) + (0,5) # this offset totally doesn't work.
      #  print(center)
        reg = (button[0] - 100, button[1] - 300, 300, 700)
        LZutils.goClick(center)
        time.sleep(0.2)
        while not pyg.locateOnScreen("Abort button.png", confidence=0.85, region=reg):
            time.sleep(0.2)
        time.sleep(1)
        return True
        


    def ClickSecondAbort(self, watchPay=False):
        xSafe = self.topLeftX + 150
        yMid = self.topLeftY + 500
        xAbort = self.topLeftX + 270
        pyg.moveTo(x=xSafe, y=yMid)
        
        ij = 0
        while ij < 5:
            ij += 1
            pyg.scroll(20)
        pyg.scroll(-20)
        
        # Scroll down so that the bottom abort is visible.
        if pyg.locateOnScreen('Pay button.png', confidence=0.9) and watchPay:
            return False
        clicked = False
        #really not sure what i'm doing.
        # i think this just passes back false if the abort hasn't loaded  yet.
        List = self.BufferLocations("Abort button.png")
        if len(List) < 2:
            time.sleep(1)
            return False
        button = List[1]
        # len - 1 give index of last on list

        center = pyg.center(button) + (0,5) # this offset totally doesn't work.
      #  print(center)
        reg = (button[0] - 100, button[1] - 300, 300, 700)
        LZutils.goClick(center)
        time.sleep(0.2)
        while not pyg.locateOnScreen("Abort button.png", confidence=0.85, region=reg):
            time.sleep(0.2)
        time.sleep(1)
        return True
        















    def UBQsetup(self, givers):
        """Put the supply and coin gather quests at the top.
    
        Returns
        -------
        None.

        """
        # print("starting setup, {} givers".format(self.UBQgivers))
        LZutils.findClick(self.QuestOpenImg, 0.6, (0, -5))
        time.sleep(0.1)
        LZutils.findClick(self.QuestOpenImg, 0.6, (0, -5))
        time.sleep(0.1)
        LZutils.findClick(self.QuestOpenImg, 0.6, (0, -5))
        time.sleep(0.1)
        times = givers - 1
        spots = [self.supQuestImg, self.coinQuestImg]
        if times == 0:# one giver
            nm = 0
            while nm < 5:
                pyg.scroll(-10)
                nm += 1
            return

        # 2 givers
        if times == 1:
            LZutils.findAndMove(self.abortImg, confidence=0.9)
            time.sleep(0.2)
            i = 0
            while i < 10:
                pyg.scroll(10) # these scrolls may break it
                i += 1
            check = None
            while check is None:

                check = pyg.locateOnScreen(self.coinQuestImg, confidence=0.9)
                # is the eone we are looking for on screen?
                if check is None:
                    self.ClickTopAbort() # if not, then click abort
                time.sleep(0.3)
                pyg.alert("found coin")
            # pyautogui.alert("coin found i think")
            if pyg.center(check)[1] > pyg.center(pyg.locateOnScreen(self.abortImg, confidence=0.95))[0]:
                '''then the bottom RQ is one we want, and we just abort the top
                if the center of the found one is lower (more positive) than the abort button, then the top abort doesn't belong to the 
                '''
                self.Face.ClickTopAbort()
                time.sleep(0.3)
            # now ours is the top one
            while i < 20:
                pyg.scroll(-10)
                i += 1
            print("2 giver setup end")
            return


        # not actually able to test 3 giver right now, TAD doesn't have it
        # 3 givers active
        if times == 2:
            # lock first quest
            LZutils.findAndMove(self.abortImg, confidence=0.8)
            time.sleep(0.2)
            while i < 10:
                pyg.scroll(10) # these scrolls may break it
                i += 1
            
            aborts = pyg.locateAllOnScreen(self.abortImg, confidence=0.7)
            check = None
            while check is None:
                """
                # get the first on on the screen
                # i figure i'm missing something, but i'm assuming that we don't
                have one of them in the bottom slot it shouldnt be normally, since
                we normally just finished a UBQ in the bottom slot
                """
                check = pyg.locateOnScreen(self.supQuestImg, confidence=0.9)
                if check is None:
                    check = pyg.locateOnScreen(self.coinQuestImg, confidence=0.9)
                if check is None:
                    LZutils.findClick(self.abortImg, confidence=0.7)
                time.sleep(0.3)
            #now we have one onscreen but might not be on top
            if pyg.center(check)[1] > pyg.center(pyg.locateOnScreen(self.abortImg, confidence=0.7))[1]:
                #then the bottom RQ is one we want, and we just abotrt the top
                LZutils.findClick(self.abortImg, confidence=0.7)
                time.sleep(0.3)
            # now the top one is the one we want
            i = 0
            while i < 100:
                if pyg.locateOnScreen(self.supQuestImg, confidence=0.7) and pyg.locateOnScreen(self.coinQuestImg, confidence=0.7):
                    while i < 10:
                        pyg.scroll(-10) # these scrolls may break it
                        i += 1
            
                    return
                aborts = pyg.locateAllOnScreen(self.abortImg, confidence=0.95)
                next(aborts)
                spot = next(aborts)

                LZutils.goClick(pyg.center(spot))
                time.sleep(0.3)


            raise ErrorLZ.LZException("Two quests not found")




    def refresh(self):
        
        time.sleep(5)
        pyg.hotkey('ctrl', 'r')
        time.sleep(10)
        while not pyg.locateOnScreen(self.QuestOpenImg, confidence=0.75):
            time.sleep(1)
            try:
                LZutils.findClick("FC birka button.png", confidence=0.7) # use findgoclickall cuz it doesn't throw error if button not found.
                time.sleep(5)
                continue
            except ErrorLZ.LZException:
                time.sleep(4)
            try:
                LZutils.findClick("play button.png", confidence=0.8)
                time.sleep(4)
                continue
            except ErrorLZ.LZException:
                time.sleep(4)
            try:
                LZutils.findClick("Birka button.png", confidence=0.8)
                time.sleep(4)
                continue
            except ErrorLZ.LZException:
                time.sleep(4)