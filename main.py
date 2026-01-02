import numpy as np

def distancia_euclidiana(x, m): # x es la muestra, m es la media del grupo
    return np.linalg.norm(x - m)

def algoritmo_cadena(muestras, umbral):
    grupos = []      # cada grupo es una lista de muestras
    medias = []      # media de cada grupo

    # Paso 1
    grupos.append([muestras[0]])
    medias.append(muestras[0])

    # Pasos siguientes
    for x in muestras[1:]:
        distancias = [distancia_euclidiana(x, m) for m in medias]
        d_min = min(distancias)
        k = distancias.index(d_min)

        if d_min < umbral:
            # asignar al grupo existente
            grupos[k].append(x)
            medias[k] = np.mean(grupos[k], axis=0)
        else:
            # crear nuevo grupo
            grupos.append([x])
            medias.append(x)

    return grupos, medias

# Muestras de características (por ejemplo, color, textura, etc.)
muestras = np.array([
    [10, 10],
    [12, 11],
    [100, 100],
    [102, 98],
    [11, 9]
])

umbral = 15

grupos, medias = algoritmo_cadena(muestras, umbral)

print("Número de grupos:", len(grupos))
for i, g in enumerate(grupos):
    print(f"Grupo {i+1}: {g}")