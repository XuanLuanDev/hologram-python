import cv2
import numpy as np
from lib.hologram import hologram

if __name__ == '__main__' :
    #orig = cv2.imread(sys.argv[1])
    #orig = cv2.imread("4.png")
    #Reading an image (you can use PNG or JPG)
    img = cv2.imread("2.jpg")
   
    pad_img = hologram.pad_img(img)
    crop_img = hologram.crop_img(pad_img)
    holo = hologram.makeHologram(crop_img,scale=1.0)
    cv2.imwrite("holo.jpg",holo)
