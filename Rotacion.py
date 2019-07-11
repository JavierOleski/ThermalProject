import cv2
def rotacion(Pie, angulo1, angulo2, columnas, filas, rango1, rango2):
    Cont1 = 0; Cont2 = 0; Cont3 = 0
    for DRaux in range(angulo1, angulo2):
        RM = cv2.getRotationMatrix2D((columnas/2, filas/2), DRaux, 1)
        RFT = cv2.warpAffine(Pie, RM, (columnas, filas))
        for i in range(30, 210, 2):
            for j in range(rango1, rango2):
                if RFT[i, j] > 20:
                    Cont1 += 1
                    #INTENTAR USAR UN BREAK PARA QUE DEJE DE ITERAR DE MANERA INNECESARIA
            if Cont1 > Cont2:
                Cont2 = Cont1
            Cont1 = 0
        if Cont3 < 1:
            Cont3 = Cont2
            Angulo_rotacion = DRaux
        if Cont2 < Cont3:
            Cont3 = Cont2
            Angulo_rotacion = DRaux
        Cont2 = 0
    Matriz = cv2.getRotationMatrix2D((columnas/2, filas/2), Angulo_rotacion, 1)
    Pie_rotado = cv2.warpAffine(Pie, Matriz, (columnas, filas))
    Pie_rotado[0, 1] = Cont3
    return Pie_rotado