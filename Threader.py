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
            raise AlreadyExisting("Threader has already been instanced")
            ## TODO do i care? cuz these are like individual modules
        self.Running[0] = 1

    def __enter__(self):
        return self






    def addProcess(self, Process):
        print("Processer add Process")
        Process.start()
        self.Processes.append(Process)


    def Trigger(self, target, args=()):
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
        wrapped =  Wrap(self, target, args)
        # I feel like the central process MAYBE could use a with.. but idk
        CentralProcess = target
        self.addProcess(CentralProcess)
        self.Listener = Interrupt(self)
        self.Listener.start()

    def stop(self):
        self.__exit__()




    def __exit__(self, problem, value, trace):
        print('Processer problem LZ', problem)
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

        if key == Key.esc and key == self.prevKey:
            print("aborting")
            self.listener.stop()
            self.Running = False
            self.Processer.stop()
# TODO use target.is_alive()
        self.prevKey = key

    def runn(self):
        print("Interrupt Start Listen()")

        with Listener(on_release=self.keyUp) as self.listener:
            self.listener.join()
        self.Running = True
        print('hellp')


    def Stop(self):
        self.listener.stop()
        self.Running = False








