# -*- coding: utf-8 -*-
"""
Created on Thu Nov  5 12:34:25 2020

@author: Glen
"""

"""
TODO

1 Threader wrapper to kill listener on error or task finished

comment stuff


UBQ 2 giver hold coin quest

exit out of UBQ

make the start a little more robust

settlement

optimize speed and pixel specific, region looking

record UBQ collections

ubq abort finding is rough. needs an LZutil probably that returns a list.

make the findClick or something return # so that UBQ logic can just check for
pay image or pay pixels and then be faster


2 givers is not working

aid isnt screenshotting only the small part...

pull specific pixels?

pyautogui.PAUSE = 0


the interface needs a wait function that just grabs a pixel or 4 and waits until it shifts back... 
cuz most things when they load, black the background. so pull maybe 20 pixels that normally should show
doesn't apply to UBQ the same way. will watch for the background going from light to not.
but others watch for dark to light. 

need to make the temp be just a pil saved image not a saved stored image. 

maybe i could make clicker be a wrapper and wrap the run function so there'd be more flexibility..'

screenshotting region...?
"""

"""
TO DONE

UBQ blueprin

aid not possible exception
"""