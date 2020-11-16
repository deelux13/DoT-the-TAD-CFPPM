# -*- coding: utf-8 -*-
"""
Created on Fri Nov 13 14:25:25 2020

@author: Glen
"""
import pyautogui as pyg


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



    def ClickBottomAbort(self):
        """Literally just click the bottom abort, handles scrolling and all.

        Assumes that quest panel is open, cuz you dumb if you call this with
        it closed."""
        xSafe = self.topLeftX + 150
        yMid = self.topLeftY + 500
        xAbort = int(self.topLeftX) + 270
        pyg.moveTo(x=xSafe, y=yMid)
        pyg.scroll(-1000)
        # Scroll down so that the bottom abort is visible.
        for y in range(self.aidBoardTopY, 200, -4):
            r, g, b = pyg.pixel(xAbort, y)
            if r in range(111,240):
                pyg.moveTo(xAbort, y, 0.1)
                pyg.click()
                break

        return

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


