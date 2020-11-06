# -*- coding: utf-8 -*-
import Threader as THd
import Clicker

def main():
    if __name__ == "__main__":
        with THd.Threader() as thd:
            Process = Clicker.ClickerProcess()
            thd.Trigger(Process)


def UBQz():
    #if __name__ == "__main__":
    test = True

    while test:
        ubqs = LZ.pyautogui.prompt(text='How many UBQs?')
        if ubqs is None:
            test = False
            break
        try:
            ubqs = int(ubqs)
            test = False
        except ValueError:
            LZ.pyautogui.alert(text="Not a number")
         ##### THIS needs a failsafe or a
    # Gets the number of UBQ loops to do

    collect = LZ.pyautogui.confirm(text='Collect coins and do 5 min productions after?', buttons=['Yes', 'No'])



    LZ.UBQ().go(ubqs)
    if collect == 'Yes':
        main()

