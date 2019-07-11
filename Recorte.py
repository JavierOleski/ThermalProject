def recorte(img, inicio, fin, filas):
    for i in range(filas):
        for j in range(inicio, fin):
            img[i, j] = 0
            img[i, j] = 0
    return img
