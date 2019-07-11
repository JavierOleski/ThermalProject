import cv2
import numpy as np
import time
from matplotlib import pyplot as plt
from Filtro import filtro
from Recorte import recorte
from Traslacion import traslacionX
from Rotacion import rotacion
from Traslacion import traslacionY
from Escalamiento import escalamiento
from Escalamiento import factor
from Deteccion import puntos


st = time.time()

img = cv2.imread('171.jpg')
filas, columnas = (cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)).shape


Feet = filtro(img)


Pie_izquierdo = recorte(filtro(img), 0, round(columnas/2), filas)
Pie_derecho = recorte(filtro(img), round(columnas/2), columnas, filas)


Pie_izquierdo_trasladadoX = traslacionX(Pie_izquierdo, columnas, filas)
Pie_derecho_trasladadoX = traslacionX(Pie_derecho, columnas, filas)


Pie_izquierdo_rotado = rotacion(Pie_izquierdo_trasladadoX, 0, 21, columnas, filas, 110, columnas-50)
Size_pie_izquierdo = Pie_izquierdo_rotado[0, 1]
Pie_izquierdo_rotado[0, 1] = 0

Pie_derecho_rotado = rotacion(Pie_derecho_trasladadoX, 340, 361, columnas, filas, 40, columnas-40)
Size_pie_derecho = Pie_derecho_rotado[0, 1]
Pie_derecho_rotado[0, 1] = 0


Pie_izquierdo_trasladadoY = traslacionY(Pie_izquierdo_rotado, columnas, filas, 100, 230)
Pie_derecho_trasladadoY = traslacionY(Pie_derecho_rotado, columnas, filas, 100, 230)


Pie_izquierdo_escalado = escalamiento(Pie_izquierdo_trasladadoY, columnas, filas)
Pie_derecho_escalado = escalamiento(Pie_derecho_trasladadoY, columnas, filas)

Factor_escalamiento_pie_izquierdo = factor(Pie_izquierdo_trasladadoY, columnas, filas)
Factor_escalamiento_pie_derecho = factor(Pie_derecho_trasladadoY, columnas, filas)


Pie_izquierdo_escalado = cv2.flip(Pie_izquierdo_escalado, 1)


Pie_punteado_izquierdo = puntos(Pie_izquierdo_escalado, columnas, filas, Size_pie_izquierdo, Factor_escalamiento_pie_izquierdo)
Pie_punteado_derecho = puntos(Pie_derecho_escalado, columnas, filas, Size_pie_derecho, Factor_escalamiento_pie_derecho)
print("----%.2f----"%(time.time()-st))

while True:
    plt.subplot(1, 2, 1), plt.imshow(Pie_punteado_izquierdo, cmap='gray'); plt.title('Daniel es...'), plt.xticks([]), plt.yticks([])
    plt.subplot(1, 2, 2), plt.imshow(Pie_punteado_derecho, cmap='gray'); plt.title('...cabro'), plt.xticks([]), plt.yticks([])
    # plt.subplot(5, 2, 3), plt.imshow(Pie_izquierdo_trasladadoY, cmap='gray'); plt.title('Daniel es...'), plt.xticks([]), plt.yticks([])
    # plt.subplot(5, 2, 4), plt.imshow(Pie_derecho_trasladadoX, cmap='gray'); plt.title('...cabro'), plt.xticks([]), plt.yticks([])
    # plt.subplot(5, 2, 5), plt.imshow(Pie_izquierdo_rotado, cmap='gray'); plt.title('Daniel es...'), plt.xticks([]), plt.yticks([])
    # plt.subplot(5, 2, 6), plt.imshow(Pie_derecho_rotado, cmap='gray'); plt.title('...cabro'), plt.xticks([]), plt.yticks([])
    # plt.subplot(5, 2, 7), plt.imshow(Pie_izquierdo_trasladadoY, cmap='gray'); plt.title('Daniel es...'), plt.xticks([]), plt.yticks([])
    # plt.subplot(5, 2, 8), plt.imshow(Pie_derecho_trasladadoY, cmap='gray'); plt.title('...cabro'), plt.xticks([]), plt.yticks([])
    # plt.subplot(5, 2, 9), plt.imshow(Pie_izquierdo_escalado, cmap='gray'); plt.title('Daniel es...'), plt.xticks([]), plt.yticks([])
    # plt.subplot(5, 2, 10), plt.imshow(Pie_derecho_escalado, cmap='gray'); plt.title('...cabro'), plt.xticks([]), plt.yticks([])
    plt.show()
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()