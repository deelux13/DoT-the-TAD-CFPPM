# -*- coding: utf-8 -*-
"""
Created on Sun Nov  1 20:59:01 2020

@author: Glen
"""
from tesserocr import PyTessBaseAPI

images = ['as.png', 'Failed Aid.png', 'UBQ identify.png']

with PyTessBaseAPI() as api:
    for img in images:
        api.SetImageFile(img)
        print(api.GetUTF8Text())
        print(api.AllWordConfidences())

