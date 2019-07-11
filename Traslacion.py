import cv2
import numpy as np

def traslacionX(Pie, cols, rows):
    image, contorno1, hierarchy = cv2.findContours(Pie, 1, 2)
    Contorno_Pie = contorno1[0]
    Momento_Pie = cv2.moments(Contorno_Pie)  # Momentos del contorno pie izquierdo
    Rx = int(Momento_Pie['m10'] / Momento_Pie['m00'])  # Eje x, centro de masa pie izquierdo
    T1 = np.float32([[1, 0, -(Rx - cols / 2)], [0, 1, 0]])
    Traslacion_Pie = cv2.warpAffine(Pie, T1, (cols, rows))
    return Traslacion_Pie


def traslacionY(Pie, cols, rows, rango1, rango2):
    RFTR = 0
    for TRAux in range(50):
        RFTT = np.float32([[1, 0, 0], [0, 1, -TRAux]])  # Right Foot Translation Test
        RightFootTT = cv2.warpAffine(Pie, RFTT, (cols, rows))  # Right Foot Translation Test
        for j in range(rango1, rango2):
            if RightFootTT[0, j] > 15:
                RFTR = TRAux
                break
        if RFTR != 0:
            break
    T1 = np.float32([[1, 0, 0], [0, 1, -RFTR]])
    Traslacion_Pie = cv2.warpAffine(Pie, T1, (cols, rows))  # Translation Right Foot
    return Traslacion_Pie