import cv2 
import numpy as np
def cartoon_maker(img_enter):
    img = cv2.imread(f"./assets/imgs/{img_enter}")
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    gray=cv2.medianBlur(gray,5)
    edges=cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,9,9)
    color=cv2.bilateralFilter(img,9,250,250)
    cartoon=cv2.bitwise_and(color,color,mask=edges)
    cv2.imwrite(f"assets/imgs/cartoon-{img_enter}",cartoon)
    return f"cartoon-{img_enter}"