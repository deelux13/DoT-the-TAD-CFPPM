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


            