# -*- coding: utf-8 -*-
"""
Created on Fri Nov  6 10:28:35 2020

@author: Glen
"""



class LZException(Exception):
    def __init__(self, context):
        self.context = context

class AlreadyExisting(Exception):
    def __init__(self, context):
        self.context = context
        print(context)

class InterruptLZ(Exception):
    pass


