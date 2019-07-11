def punto1(Pie, factor_escalamiento, LFU):
    y = round(17 * factor_escalamiento)
    x = LFU - round(17 * factor_escalamiento)
    P1L = 0
    P1Lcont = 0
    for i in range(-7, 7):
        for j in range(-7, 7):
            P1L = P1L + Pie[y + i, x + j]
            Pie[y + i, x + j] = 0
            P1Lcont = P1Lcont + 1
    P1L = P1L / P1Lcont
    Pie[0, 1] = P1L
    return Pie

def punto2(Pie, factor_escalamiento, size, LFR):
    y = round(62 * factor_escalamiento)
    x = int(round(LFR - size*0.25))
    P2L = 0
    P2Lcont = 0
    for i in range(-7, 7):
        for j in range(-7, 7):
            P2L = P2L + Pie[y + i, x+j]
            Pie[y + i, x + j] = 0
            P2Lcont = P2Lcont + 1
    P2L = P2L / P2Lcont
    Pie[0, 2] = P2L
    return Pie


def punto3(Pie, factor_escalamiento, LFM):
    y = round(52 * factor_escalamiento)
    x = round(LFM)
    P3L = 0
    P3Lcont = 0
    for i in range(-7, 7):
        for j in range(-7, 7):
            P3L = P3L + Pie[y + i, x + j]
            Pie[y + i, x + j] = 0
            P3Lcont = P3Lcont + 1
    P3L = P3L / P3Lcont
    Pie[0, 3] = P3L
    return Pie


def punto4(Pie, factor_escalamiento, size, LFL):
    y = round(77 * factor_escalamiento)
    x = int(round(LFL + 5 * size / 20))
    P4L = 0
    P4Lcont = 0
    for i in range(-7, 7):
        for j in range(-7, 7):
            P4L = P4L + Pie[y + i, x + j]
            Pie[y + i, x + j] = 0
            P4Lcont = P4Lcont + 1
    P4L = P4L / P4Lcont
    Pie[0, 4] = P4L
    return Pie


def punto5(Pie, factor_escalamiento, LFD):
    y = round(180 * factor_escalamiento)
    x = LFD
    P5L = 0
    P5Lcont = 0
    for i in range(-7, 7):
        for j in range(-7, 7):
            P5L = P5L + Pie[y + i, x + j]
            Pie[y + i, x + j] = 0
            P5Lcont = P5Lcont + 1
    P5L = P5L / P5Lcont
    Pie[0, 5] = P5L
    return Pie

def puntos(Pie, columnas, filas, size, factor_escalamiento):
    LFD2 = columnas
    for j in range(0, columnas):
        if Pie[filas-25, j] > 0:
            if LFD2 > j:
                LFD2 = j

    LFD3 = 0
    for j in range(0, columnas):
        if Pie[filas-25, j] > 0:
            if j > LFD3:
                LFD3 = j

    LFD = round((LFD2 + LFD3)/2)

    LFU = 0
    for j in range(0, columnas):
        if Pie[20, j] > 0:
            if j > LFU:
                LFU = j

    LFR = 0
    LFL = columnas
    for j in range(columnas):
        if Pie[round(80*factor_escalamiento), j] > 0:
            if LFL > j:
                LFL = j
        if Pie[round(60*factor_escalamiento), j] > 0:
            if j > LFR:
                LFR = j
    LFM = (LFL + LFR)/2


    Pie = punto1(Pie, factor_escalamiento, LFU)

    Pie = punto2(Pie, factor_escalamiento, size, LFR)

    Pie = punto3(Pie, factor_escalamiento, LFM)

    Pie = punto4(Pie, factor_escalamiento, size, LFL)

    Pie = punto5(Pie, factor_escalamiento, LFD)

    return Pie


