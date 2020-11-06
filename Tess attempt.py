# -*- coding: utf-8 -*-
"""
Created on Sun Nov  1 20:59:01 2020

@author: Glen
"""
from tesserocr import PyTessBaseAPI
import tesserocr
from PIL import Image

images = ['as.png', 'Failed Aid.png', 'UBQ identify.png']

with PyTessBaseAPI() as api:
    for img in images:
        api.SetImageFile(img)
        print(api.GetUTF8Text())
        print(api.AllWordConfidences())

image = Image.open('Failed Aid.png')
print(tesserocr.image_to_text(image))


from PIL import Image
from tesserocr import PyTessBaseAPI, RIL

image = Image.open('as.png')
with PyTessBaseAPI() as api:
    api.SetImage(image)
    boxes = api.GetComponentImages(RIL.TEXTLINE, True)
    print('Found {} textline image components.'.format(len(boxes)))
    for i, (im, box, _, _) in enumerate(boxes):
        # im is a PIL image object
        # box is a dict with x, y, w and h keys
        api.SetRectangle(box['x'], box['y'], box['w'], box['h'])
        ocrResult = api.GetUTF8Text()
        conf = api.MeanTextConf()
        print(u"Box[{0}]: x={x}, y={y}, w={w}, h={h}, "
              "confidence: {1}, text: {2}".format(i, conf, ocrResult, **box))