# -*- coding: utf-8 -*-
import Threader as THd
import Brain
from os import getcwd
import pyautogui
import numpy
import multiprocessing
import time
from numpy import *

if __name__ == "__main__":
    multiprocessing.freeze_support()
    print(getcwd())
    
    with THd.ThreadHandler() as thd:
        print("in with")
        Process = Brain.Brains(thd)
        print("clicker initiated in with")
        thd.addProcess(Process)
        while True:
            time.sleep(400)







# I'm looking for people to help supply me with BA goods, i'm willing to trade you 2 IA goods for every bronze age good any of your choice, and put 10 FP on one of your GBs for every 50 BA goods, or help you get new GBs like ARC or Chateau. let me know if you're interested. 