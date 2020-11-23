# -*- coding: utf-8 -*-
"""
Created on Fri Nov 13 14:25:25 2020

@author: Glen
"""
import pyautogui as pyg
import time
import LZutils
from PIL import Image


def cycle():
    for y in range(0,120):
        print(pyg.pixel(66, y), " at y ", y)



class Interface():
    """The Game facing interface aka pixel finder and other utils."""
    def __init__(self):
        self.topLeft = pyg.locateOnScreen("Top Left corner.png", confidence=0.8)
        self.RightEdgeQuestX = self.topLeft[0] + 690
        self.QuestMiddle = self.RightEdgeQuestX//2
        self.topLeftX = self.topLeft[0]
        self.topLeftY = self.topLeft[1]
        self.aidBoardTopY = pyg.locateOnScreen("left edge of player aid board.png", confidence=0.9)[1]
        if self.topLeftX > 30:
            pyg.alert("You really should maximize the screen...")
        # TODO i think i might need to add something here...

    def __enter__(self):
        pass


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
            print(last)
            print(spot)
            while LZutils.OverlapDetect(last, spot, Img):
                spot =  next(gen, None)
                if spot is None:
                    return List
                
                # need to check overlap. if overlap then we move to the next in the generator. if the generator runs out we just return what we have.
        return List # gen ran out without ending on an  overlap so we got this correctly.
            


    def ClickBottomAbort(self):
        """Literally just click the bottom abort, handles scrolling and all.
        
        This is rather slow. 

        Assumes that quest panel is open, cuz you dumb if you call this with
        it closed."""
        xSafe = self.topLeftX + 150
        yMid = self.topLeftY + 300
        print(self.topLeftY, "top offset")
        xAbort = int(self.topLeftX) + 270
        pyg.moveTo(xSafe, yMid, 0.3)
        # scroll does weird things
        ij = 0
        while ij < 5:
            ij += 1
            pyg.scroll(-20)
        
        # Scroll down so that the bottom abort is visible.
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
        print(center)
        
        LZutils.goClick(center)
        time.sleep(3.2)
        return True

    def ClickTopAbort(self):
        xSafe = self.topLeftX + 150
        yMid = self.topLeftY + 500
        xAbort = self.topLeftX + 270
        pyg.moveTo(x=xSafe, y=yMid)
        pyg.scroll(1000)
        for y in range(self.topLeftY, self.aidBoardTopY, 4):
            # Moving top to bottom
            r, g, b = pyg.pixel(xAbort, y)
            if r in range(111,240):
                pyg.moveTo(xAbort, y, 0.1)
                pyg.click()
                break


    def ClickSecondAbort(self):
        xSafe = self.topLeftX + 150
        yMid = self.topLeftY + 500
        xAbort = self.topLeftX + 270
        pyg.moveTo(x=xSafe, y=yMid)
        pyg.scroll(1000)
        y = self.topLeftY
        go = False
        while y < self.aidBoardTopY:
            # Moving top to bottom
            r, g, b = pyg.pixel(xAbort, y)
            if r in range(111,240) and go == True:
                if go == True:
                    pyg.moveTo(xAbort, y, 0.1)
                    pyg.click()
                    break


            y += 4

