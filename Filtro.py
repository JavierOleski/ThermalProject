import cv2
import numpy as np

def filtro(imagen):
    Aux = 55
    kernel55 = np.ones((5, 5), np.uint8)
    FeetMask = cv2.imread('FeetMasK.jpg')
    opening = cv2.morphologyEx((cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)), cv2.MORPH_OPEN, kernel55)
    ret2, thresh2 = cv2.threshold(opening, Aux, 255, cv2.THRESH_TOZERO)
    Mask = cv2.cvtColor(FeetMask, cv2.COLOR_BGR2GRAY)
    ret3, thresh3 = cv2.threshold(Mask, 20, 255, cv2.THRESH_BINARY)
    Foot = cv2.bitwise_and(thresh2, thresh2, mask=thresh3)
    ret4, Filtro = cv2.threshold(Foot, Aux, 255, cv2.THRESH_BINARY)
    Foot2 = cv2.bitwise_and((cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)), (cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)), mask=Filtro)
    return Foot2