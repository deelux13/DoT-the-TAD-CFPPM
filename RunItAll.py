# -*- coding: utf-8 -*-
import Threader as THd
import Clicker
from os import getcwd
import pyautogui
import numpy
import multiprocessing

if __name__ == "__main__":
    multiprocessing.freeze_support()
    print(getcwd())
    
    with THd.Threader() as thd:
        print("in with")
        Process = Clicker.ClickerProcess()
        print("clicker initiated in with")
        thd.Trigger(Process)


