# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 21:12:16 2020

@author: Glen
"""


import pyautogui
from multiprocessing import Process
import time
import sys
from pynput.keyboard import Key, Listener
from functools import wraps
import ErrorLZ

# def Wrap(self, func):
#     @wraps(func)
#     def inner():
#         try:
#             func()
#         except:
#             raise LZException("Threader target error i think")
#         self.__exit__()
#     return inner


# class LZprocess(Process):
#     def __init__(self):
#         super(LZprocess, self).__init__()


class Threader():
    """Makes a new Process to listen for a double esc and stops Process

    """
    Running = [0]
    Processes = []
    Interrupts = []

    def __init__(self):
        print("Processer init")
        if self.Running[0] > 0:
            raise ErrorLZ.AlreadyExisting("Threader has already been instanced")
            ## TODO do i care? cuz these are like individual modules
        self.Running[0] = 1

        self.Listener = Interrupt(self)
        # in _init so that errors don't kill it as hard?.. also only need one listener.

    def __enter__(self):
        return self






    def addProcess(self, Process):
        print("Processer add Process")
        Process.start()
        print('Process started')
        self.Processes.append(Process)


    def Trigger(self, target):
        """Runs a callable with a key listener for esc x2 to exit


        Parameters
        ----------
        target : Process object
            to be run.
        args : tuple, optional
            args for the callable. The default is ().

        Returns
        -------
        None.

        """


        print("Processer trigger cent")
        print("target = ", target)

        # I feel like the central process MAYBE could use a with.. but idk
        CentralProcess = target
        self.addProcess(CentralProcess)
        print("addprocess call completed")
        self.Listener.run()
        # self.Listener.join()
        # this is not needed if run is called, but then the main thread is locked to the listener. don't think i mind
        print("listener started")

    def stop(self):
        self.__exit__("Stopped by self.Stop()", "fake", "fake")
        # feels like a hack to keep exit in the main call from killing the threads




    def __exit__(self, problem, value, trace):
        print('Processer problem LZ', problem)
        if problem is not None:
            self.Running[0] = 0
            for thing in self.Processes:
                thing.terminate()
            self.Listener.Stop()



class Interrupt(Process):
    def __init__(self, Processer):
        """Needs the Parent Processere object, will call Processer.stop

        Parameters
        ----------
        target : TYPE
            DESCRIPTION.
        Processer : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        super(Interrupt, self).__init__()
        self.prevKey = Key.enter

        self.Processer = Processer

    def keyUp(self, key):
        print(key)
        # pyautogui.move(100,100)
        # if key == Key.enter:
        #     pyautogui.alert(text='running, enter was pressed')


        if key == Key.esc and key == self.prevKey:
            print("aborting")
            self.listener.stop()
            self.Running = False
            self.Processer.stop()
# TODO use target.is_alive()
        self.prevKey = key

    def run(self):
        print("Interrupt Start Listen()")

        with Listener(on_release=self.keyUp) as self.listener:
            self.listener.join()
        self.Running = True
        print('hellp')


    def Stop(self):
        self.listener.stop()
        self.Running = False








