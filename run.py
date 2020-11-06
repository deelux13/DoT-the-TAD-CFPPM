# -*- coding: utf-8 -*-
"""
Created on Fri Nov  6 12:27:24 2020

@author: Glen
"""

import Threader as THd
import Clicker

with THd.Threader() as thd:
    thd.Trigger(Clicker.ClickerProcess())