import cv2

def escalamiento(Pie, columnas, filas):
    Factor_escalamiento = 2
    for RVAux in range(60):
        LAux = 1 + (RVAux / 200)
        RightFootST = cv2.resize(Pie, None, fx=LAux, fy=LAux, interpolation=cv2.INTER_CUBIC)
        for j in range(columnas):
            if RightFootST[filas - 1, j] != 0:
                if Factor_escalamiento > LAux:
                    Factor_escalamiento = LAux
    Pie_escalado = cv2.resize(Pie, None, fx=Factor_escalamiento, fy=Factor_escalamiento, interpolation=cv2.INTER_CUBIC)
    Pie_escalado = Pie_escalado[0:filas, 0:columnas]
    return(Pie_escalado)

# Unir estas dos funciones y que retornen una imagen y un float

def factor(Pie, columnas, filas):
    Factor_escalamiento = 2
    for RVAux in range(60):
        LAux = 1 + (RVAux / 200)
        RightFootST = cv2.resize(Pie, None, fx=LAux, fy=LAux, interpolation=cv2.INTER_CUBIC)
        for j in range(columnas):
            if RightFootST[filas - 1, j] != 0:
                if Factor_escalamiento > LAux:
                    Factor_escalamiento = LAux
    return Factor_escalamiento