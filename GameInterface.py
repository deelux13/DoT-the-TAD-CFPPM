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
        
        self.collections = [self.coinImg, self.coinStarImg,
                            self.suppliesImg, self.suppliesStarImg]

        self.topLeft = pyg.locateOnScreen("Top Left corner.png", confidence=0.55)
        self.RightEdgeQuestX = self.topLeft[0] + 690
        self.QuestMiddle = self.RightEdgeQuestX//2
        self.topLeftX = self.topLeft[0]
        self.topLeftY = self.topLeft[1]
        self.aidBoardTopY = pyg.locateOnScreen("left edge of player aid board.png", confidence=0.9)[1]
        if self.topLeftX > 30:
            pyg.alert("You really should maximize the screen...")
        # TODO i think i might need to add something here...

    def __enter__(self):
        return self




    def UBQmode(self, number,  givers):
        if number < 0 :
            infinite = True
        if number == 0 :
            print("none to do, 0 requested")
            return
        done = 0
        time.sleep(1)
        self.UBQsetup(givers) # should set it up.
        center = pyg.locateCenterOnScreen(self.abortImg, confidence=0.7)
        while (number + 1)/(done + 1) - 1 > 0:
            # TODO this still needs help.... idk what i'm doing.




## I really could do only a region check if its a performance issue
# seems like the FOE performance is the real hangup at least on ubu-dev
    def UBQ(self):
        time.sleep(1)
        center = pyg.locateCenterOnScreen(self.abortImg, confidence=0.7)
        print("pre UBQ setup")
        self.UBQsetup()
        print("post UBQ setup")
        while self.UBQtodo > 0:
            time.sleep(0.5)
            LZutils.scroll(-1)
                #safety scroll

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
                       # print('tried')
                        LZutils.findClick(self.closeImg)
                        pyg.moveTo(center)
                    except ErrorLZ.LZException:
                        pass
                    finally:
                        i -= 1
                        j = 0
                        while j < 5:
                            pyg.scroll(10) # these scrolls may break it
                            j += 1
                        
                        if self.UBQtodo % 7 == 0:
                            print(f'{self.UBQtodo} of {self.totalUBQ} still left to do {time.asctime( time.localtime(time.time()) )}.')

                self.UBQtodo -= 1
                time.sleep(0.3)
                nm = 0 
                while nm < 7:
                    pyg.scroll(-10) # these scrolls may break it
                    nm += 1
                
            else:

                try:
                    self.Face.ClickBottomAbort()
                    # should click the bottom abort button
                    # returns false if it doesn't click. but i don't care right now.

                except ErrorLZ.LZException:
                    pyg.alert(text='no abort found')
                    continue
                except OSError or TypeError:
                    print("issues with UBQ finding abort button")

                    continue
        LZutils.findClick(self.UBQexitImg, confidence=0.8)








    def BufferLocations(self, img):
        Img = Image.open(img)
        gen = pyg.locateAllOnScreen(Img, confidence=0.9)
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
    def ClickBottomAbort(self, watchPay=True):
        """Literally just click the bottom abort, handles scrolling and all.
        
        This is rather slow. 

        Assumes that quest panel is open, cuz you dumb if you call this with
        it closed."""
        xSafe = self.topLeftX + 150
        yMid = self.topLeftY + 300
       # print(self.topLeftY, "top offset")
        xAbort = int(self.topLeftX) + 270
        pyg.moveTo(xSafe, yMid, 0.3)
        # scroll does weird things
        # ij = 0
        # while ij < 5:
        #     ij += 1
        #     pyg.scroll(-20)
        
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
        button = List[len(List) - 1]
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
                    self.Face.ClickTopAbort() # if not, then click abort
                time.sleep(0.3)
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
