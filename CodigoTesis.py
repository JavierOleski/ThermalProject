import cv2
import numpy as np
import time
from matplotlib import pyplot as plt
Cont = 0
Value = 0
st = time.time()

img = cv2.imread('230.jpg')
BarMask = cv2.imread('BarMask.jpg')
RightFootMask = cv2.imread('RightFootMask.jpg')
LeftFootMask = cv2.imread('LeftFootMask.jpg')
FeetMask = cv2.imread('FeetMasK.jpg')
kernel55 = np.ones((5, 5), np.uint8)
Originalgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
Originalgray2 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
Aux = 55; DR = 0; DRaux = 0; DRcont1 = 0; DRcont2 = 0; DRcont3 = 0; RFDR = 0; LFDR = 0; RFTR = 0; LFTR = 0;
rows, cols = Originalgray.shape

#VT1 = float(input("Temperatura 1: "))
#VT2 = float(input("Temperatura 2: "))
#if VT2 < VT1:
#    LV = VT2
#    VT2 = VT1
#    VT1 = LV


I2 = 0
for j in range(302, 316):
    if I2 < Originalgray[30, j]:
        I2 = Originalgray[30, j]
#print(I2)

I1 = 255
for j in range(302, 316):
    if I1 > Originalgray[210, j]:
        I1 = Originalgray[210, j]
#print(I1)


gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

opening = cv2.morphologyEx(gray, cv2.MORPH_OPEN, kernel55)
ret2, thresh2 = cv2.threshold(opening, Aux, 255, cv2.THRESH_TOZERO)

Mask = cv2.cvtColor(FeetMask, cv2.COLOR_BGR2GRAY)
ret3, thresh3 = cv2.threshold(Mask, 20, 255, cv2.THRESH_BINARY)

#thresh4 = cv2.bitwise_and(thresh2, thresh2, mask=thresh3)

RightFoot = cv2.bitwise_and(thresh2, thresh2, mask=thresh3)
LeftFoot = cv2.bitwise_and(thresh2, thresh2, mask=thresh3)

ret4, RightFootW = cv2.threshold(RightFoot, Aux, 255, cv2.THRESH_BINARY)
ret5, LeftFootW = cv2.threshold(LeftFoot, Aux, 255, cv2.THRESH_BINARY)

RightFoot = cv2.bitwise_and(Originalgray, Originalgray, mask=RightFootW)
LeftFoot = cv2.bitwise_and(Originalgray2, Originalgray2, mask=LeftFootW)



for i in range (0, rows):
    for j in range(0, 160):
        RightFootW[i, j] = 0
        RightFoot[i, j] = 0

for i in range(0, rows):
    for j in range(160, cols):
        LeftFootW[i, j] = 0
        LeftFoot[i, j] = 0



image, contoursRF, hierarchy = cv2.findContours(RightFootW, 1, 2)
cnt1 = contoursRF[0]
#Contours = cv2.drawContours(Originalgray, contoursRF, -1, (0,255,0), 3)

image, contoursLF, hierarchy = cv2.findContours(LeftFootW, 1, 2)
cnt2 = contoursLF[0]
#Contours = cv2.drawContours(Originalgray2, contoursLF, -1, (0,255,0), 3)



M1 = cv2.moments(cnt1) #Momentos del contorno RF
Rx = int(M1['m10']/M1['m00']) # Eje x, centro de masa Right Foot
Ry = int(M1['m01']/M1['m00']) # Eje y, centro de masa RF

M2 = cv2.moments(cnt2) #Momentos del contorno LF
Lx = int(M2['m10']/M2['m00']) # Eje x, centro de masa Left Foot
Ly = int(M2['m01']/M2['m00']) # Eje y, centro de masa LF



T1 = np.float32([[1, 0, -(Rx - cols/2)], [0, 1, 0]])
RightFootT = cv2.warpAffine(RightFoot, T1, (cols, rows)) #Translation Right Foot

T2 = np.float32([[1, 0, (cols/2-Lx)], [0, 1, 0]])
LeftFootT = cv2.warpAffine(LeftFoot, T2, (cols, rows)) #Translation Left Foot


#ROTACIÓN RIGHT FOOT
for DRaux in range(0, 20):
    RM = cv2.getRotationMatrix2D((cols/2, rows/2), DRaux, 1)
    RFT = cv2.warpAffine(RightFootT, RM, (cols, rows))
    for i in range(0, rows):
        for j in range(110, cols-50):
            if RFT[i, j] > Aux:
                DRcont1 = DRcont1 + 1
        if DRcont1 > DRcont2:
            DRcont2 = DRcont1
        DRcont1 = 0
    if DRcont3 < 1:
        DRcont3 = DRcont2
        RFDR = DRaux
    if DRcont2 < DRcont3:
        DRcont3 = DRcont2
        RFDR = DRaux
    DRcont2 = 0
RightFootSize = DRcont3
#print(RFDR)

#ROTACIÓN LEFT FOOT
DRcont1 = 0; DRcont2 = 0; DRcont3 = 0
for DRaux in range(340, 361):
    RM = cv2.getRotationMatrix2D((cols/2, rows/2), DRaux, 1)
    LFT = cv2.warpAffine(LeftFootT, RM, (cols, rows))
    for i in range(0, rows):
        for j in range(40, cols-40):
            if LFT[i, j] > Aux:
                DRcont1 = DRcont1 + 1
        if DRcont1 > DRcont2:
            DRcont2 = DRcont1
        DRcont1 = 0
    if DRcont3 < 1:
        DRcont3 = DRcont2
        LFDR = DRaux
    if DRcont2 < DRcont3:
        DRcont3 = DRcont2
        LFDR = DRaux
    DRcont2 = 0
LeftFootSize = DRcont3
#print(LFDR)

RMRF = cv2.getRotationMatrix2D((cols/2, rows/2), RFDR, 1) #Rotation Matrix Right Foot
RightFootR = cv2.warpAffine(RightFootT, RMRF, (cols, rows)) #Right Foot Rotation

RMLF = cv2.getRotationMatrix2D((cols/2, rows/2), LFDR, 1) #Rotation Matrix Left Foot
LeftFootR = cv2.warpAffine(LeftFootT, RMLF, (cols, rows)) #Left Foot Rotation



TAux = 50; RFTR = 50
for TRAux in range(0, TAux):
    RFTT = np.float32([[1, 0, 0], [0, 1, -TRAux]]) #Right Foot Translation Test
    RightFootTT = cv2.warpAffine(RightFootR, RFTT, (cols, rows)) #Right Foot Translation Test
    for j in range(0, cols):
        if RightFootTT[0, j] > 0:
            if TRAux < RFTR:
                RFTR = TRAux
                TAux = TRAux
#print(-RFTR)

TAux = 50; LFTR = 50
for TRAux in range(0, TAux):
    LFTT = np.float32([[1, 0, 0], [0, 1, -TRAux]]) #Right Foot Translation Test
    LeftFootTT = cv2.warpAffine(LeftFootR, LFTT, (cols, rows)) #Right Foot Translation Test
    for j in range(0, cols):
        if LeftFootTT[0, j] > 0:
            if TRAux < LFTR:
                LFTR = TRAux
                TAux = TRAux
#print(-LFTR)

T1 = np.float32([[1, 0, 0], [0, 1, -RFTR]])
RightFootT2 = cv2.warpAffine(RightFootR, T1, (cols, rows)) #Translation Right Foot

T2 = np.float32([[1, 0, 0], [0, 1, -LFTR]])
LeftFootT2 = cv2.warpAffine(LeftFootR, T2, (cols, rows)) #Translation Left Foot


#Escalamiento
RVRF = 2
RAux = 60
for RVAux in range (0,RAux):
    LAux = 1 + (RVAux/200)
    RightFootST = cv2.resize(RightFootT2,None,fx=LAux, fy=LAux, interpolation = cv2.INTER_CUBIC)
    for j in range (0,cols):
        if RightFootST[rows-1,j] > 0:
            if RVRF > LAux:
                RVRF = LAux
#print(RVRF)

RVLF = 2
for RVAux in range (0,RAux):
    LAux = 1 + (RVAux/200)
    LeftFootST = cv2.resize(LeftFootT2,None,fx=LAux, fy=LAux, interpolation = cv2.INTER_CUBIC)
    for j in range (0,cols):
        if LeftFootST[rows-1,j] > 0:
            if RVLF > LAux:
                RVLF = LAux
#print(RVLF)



RightFootS = cv2.resize(RightFootT2, None, fx=RVRF, fy=RVRF, interpolation=cv2.INTER_CUBIC)
RightFootS = RightFootS[0:rows, 0:cols]

LeftFootS = cv2.resize(LeftFootT2, None, fx=RVLF, fy=RVLF, interpolation=cv2.INTER_CUBIC)
LeftFootS = LeftFootS[0:rows, 0:cols]


RFD2 = cols
for j in range(0, cols):
    if RightFootS[rows-25, j] > 0:
        if RFD2 > j:
            RFD2 = j
#print(RFD2)
RFD3 = 0
for j in range(0, cols):
    if RightFootS[rows-25, j] > 0:
        if j > RFD3:
            RFD3 = j
#print(RFD3)
RFD = round((RFD2 + RFD3)/2)


LFD2 = cols
for j in range(0, cols):
    if LeftFootS[rows-25, j] > 0:
        if LFD2 > j:
            LFD2 = j
#print(LFD2)
LFD3 = 0
for j in range(0, cols):
    if LeftFootS[rows-25, j] > 0:
        if j > LFD3:
            LFD3 = j
#print(LFD3)
LFD = round((LFD2 + LFD3)/2)


RightFootAuxi = RightFootS
LeftFootAuxi = LeftFootS

RightFootPoints = RightFootS
LeftFootPoints = LeftFootS

RFU = cols
for j in range(0, cols):
    if RightFootPoints[20, j] > 0:
        if RFU > j:
            RFU = j

LFU = 0
for j in range(0, cols):
    if LeftFootPoints[20, j] > 0:
        if j > LFU:
            LFU = j

RFR = 0
RFL = cols
for j in range(0, cols):
    if RightFootPoints[round(60*RVRF), j] > 0:
        if RFL > j:
            RFL = j
    if RightFootPoints[round(80*RVRF), j] > 0:
        if j > RFR:
            RFR = j
RFM = (RFL + RFR)/2
#print(RFM)


LFR = 0
LFL = cols
for j in range (0, cols):
    if LeftFootPoints[round(80*RVLF), j] > 0:
        if LFL > j:
            LFL = j
    if LeftFootPoints[round(60*RVLF), j] > 0:
        if j > LFR:
            LFR = j
LFM = (LFL + LFR)/2
#print(LFM)


y = round(17*RVRF)
x = RFU + round(17*RVRF)
P1R = 0
P1Rcont = 0
for i in range(-7, 7):
    for j in range(-7, 7):
        P1R = P1R + RightFootPoints[y+i, x+j]
        RightFootPoints[y+i, x+j] = 0
        P1Rcont = P1Rcont + 1
P1R = P1R/P1Rcont
#print(P1R)

y = round(17*RVLF)
x = LFU - round(17*RVLF)
P1L = 0
P1Lcont = 0
for i in range(-7, 7):
    for j in range(-7, 7):
        P1L = P1L + LeftFootPoints[y+i, x+j]
        LeftFootPoints[y+i, x+j] = 0
        P1Lcont = P1Lcont + 1
P1L = P1L/P1Lcont
#print(P1L)

y = round(62*RVRF)
x = round(RFL + 5*RightFootSize/20)
P2R = 0
P2Rcont = 0
for i in range(-7, 7):
    for j in range(-7, 7):
        P2R = P2R + RightFootPoints[y+i, x+j]
        RightFootPoints[y+i, x+j] = 0
        P2Rcont = P2Rcont + 1
P2R = P2R/P2Rcont
#print(P2R)

y = round(62*RVLF)
x = round(LFR - 5*LeftFootSize/20)
P2L = 0
P2Lcont = 0
for i in range(-7, 7):
    for j in range(-7, 7):
        P2L = P2L + LeftFootPoints[y+i, x+j]
        LeftFootPoints[y+i, x+j] = 0
        P2Lcont = P2Lcont + 1
P2L = P2L/P2Lcont
#print(P2L)

y = round(52*RVRF)
x = round(RFM)
P3R = 0
P3Rcont = 0
for i in range(-7, 7):
    for j in range(-7, 7):
        P3R = P3R + RightFootPoints[y+i, x+j]
        RightFootPoints[y+i, x+j] = 0
        P3Rcont = P3Rcont + 1
P3R = P3R/P3Rcont
#print(P3R)

y = round(52*RVLF)
x = round(LFM)
P3L = 0
P3Lcont = 0
for i in range(-7, 7):
    for j in range(-7, 7):
        P3L = P3L + LeftFootPoints[y+i, x+j]
        LeftFootPoints[y+i, x+j] = 0
        P3Lcont = P3Lcont + 1
P3L = P3L/P3Lcont
#print(P3L)

y = round(77*RVRF)
x = round(RFR - 5*RightFootSize/20)
P4R = 0
P4Rcont = 0
for i in range(-7, 7):
    for j in range(-7, 7):
        P4R = P4R + RightFootPoints[y+i, x+j]
        RightFootPoints[y+i, x+j] = 0
        P4Rcont = P4Rcont + 1
P4R = P4R/P4Rcont
#print(P4R)

y = round(77*RVLF)
x = round(LFL + 5*LeftFootSize/20)
P4L = 0
P4Lcont = 0
for i in range (-7, 7):
    for j in range (-7, 7):
        P4L = P4L + LeftFootPoints[y+i, x+j]
        LeftFootPoints[y+i, x+j] = 0
        P4Lcont = P4Lcont + 1
P4L = P4L/P3Lcont
#print(P4L)

y = round(180*RVRF)
x = RFD
P5R = 0
P5Rcont = 0
for i in range (-7, 7):
    for j in range (-7, 7):
        P5R = P5R + RightFootPoints[y+i, x+j]
        RightFootPoints[y+i, x+j] = 0
        P5Rcont = P5Rcont + 1
P5R = P5R/P5Rcont
#print(P5R)

y = round(180*RVLF)
x = LFD
P5L = 0
P5Lcont = 0
for i in range (-7, 7):
    for j in range (-7, 7):
        P5L = P5L + LeftFootPoints[y+i, x+j]
        LeftFootPoints[y+i, x+j] = 0
        P5Lcont = P5Lcont + 1
P5L = P5L/P5Lcont
#print(P5L)

P1 = P1R - P1L; print(round(P1L, 2)); print(round(P1R, 2))
print()
P2 = P2R - P2L; print(round(P2L, 2)); print(round(P2R, 2))
print()
P3 = P3R - P3L; print(round(P3L, 2)); print(round(P3R, 2))
print()
P4 = P4R - P4L; print(round(P4L, 2)); print(round(P4R, 2))
print()
P5 = P5R - P5L; print(round(P5L, 2)); print(round(P5R, 2))
print()


#P1R = round((((P1R - I1)/(I2 - I1)*(VT2 - VT1)) + VT1), 2); print(P1R)
#P1L = round((((P1L - I1)/(I2 - I1)*(VT2 - VT1)) + VT1), 2); print(P1L)
#P1 = abs(round((P1R - P1L), 2)); print(P1)
#print()
#P2R = round((((P2R - I1)/(I2 - I1)*(VT2 - VT1)) + VT1), 2); print(P1R)
#P2L = round((((P2L - I1)/(I2 - I1)*(VT2 - VT1)) + VT1), 2); print(P2L)
#P2 = abs(round((P2R - P2L), 2)); print(P2)
#print()
#P3R = round((((P3R - I1)/(I2 - I1)*(VT2 - VT1)) + VT1), 2); print(P3R)
#P3L = round((((P3L - I1)/(I2 - I1)*(VT2 - VT1)) + VT1), 2); print(P3L)
#P3 = abs(round((P3R - P3L), 2)); print(P3)
#print()
#P4R = round((((P4R - I1)/(I2 - I1)*(VT2 - VT1)) + VT1), 2); print(P4R)
#P4L = round((((P4L - I1)/(I2 - I1)*(VT2 - VT1)) + VT1), 2); print(P4L)
#P4 = abs(round((P4R - P4L), 2)); print(P4)
#print()
#P5R = round((((P5R - I1)/(I2 - I1)*(VT2 - VT1)) + VT1), 2); print(P5R)
#P5L = round((((P5L - I1)/(I2 - I1)*(VT2 - VT1)) + VT1), 2); print(P5L)
#P5 = abs(round((P5R - P5L), 2)); print(P5)
#print()

print("----%.2f----"%(time.time()-st))

while True:
    #cv2.imshow('Escala de grises', Originalgray)
    #Subploteo de imágenes:
    plt.subplot(1, 1, 1), plt.imshow(LeftFootPoints, cmap='gray'); plt.title('Escala de grises'), plt.xticks([]), plt.yticks([])
    #plt.subplot(1, 2, 2), plt.imshow(LeftFootAuxi, cmap='gray'); plt.title('Puntos de interés pie izquierdo'), plt.xticks([]), plt.yticks([])
    plt.show()
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()