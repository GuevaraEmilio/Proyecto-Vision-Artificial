import numpy as np
from PIL import Image
import random

def distancia_euclidiana(x, m): # x es la muestra, m es la media del grupo
    return np.linalg.norm(x - m)

def algoritmo_cadena(muestras, umbral):
    grupos = []      # cada grupo es una lista de muestras
    medias = []      # media de cada grupo
    asignaciones = []  # lista de índices de grupo para cada muestra

    # Paso 1
    grupos.append([muestras[0]])
    medias.append(muestras[0])
    asignaciones.append(0)

    # Pasos siguientes
    for x in muestras[1:]:
        distancias = [distancia_euclidiana(x, m) for m in medias]
        d_min = min(distancias)
        k = distancias.index(d_min)

        if d_min < umbral:
            # asignar al grupo existente
            grupos[k].append(x)
            medias[k] = np.mean(grupos[k], axis=0)
            asignaciones.append(k)
        else:
            # crear nuevo grupo
            grupos.append([x])
            medias.append(x)
            asignaciones.append(len(grupos) - 1)

    return grupos, medias, asignaciones

# Cargar imagen y convertir a matriz de muestras
img_path = 'imgs/playa06.png'
img = Image.open(img_path)

# Redimensionar la imagen para acelerar el procesamiento (ajusta el tamaño según necesites)
img = img.resize((200, 200))  # Cambia a un tamaño más pequeño si es necesario

# Convertir a RGB para asegurar 3 canales
img = img.convert('RGB')

img_array = np.array(img)

# Si la imagen es RGB, aplanar a (altura*ancho, 3)
if img_array.ndim == 3:
    height, width, channels = img_array.shape
    muestras = img_array.reshape((height * width, channels)).astype(float)
    print(f"Imagen cargada: {width}x{height}, {channels} canales, {len(muestras)} píxeles")
else:
    # Si es escala de grises, aplanar a (altura*ancho, 1)
    muestras = img_array.flatten().reshape(-1, 1).astype(float)
    print(f"Imagen cargada: {img_array.shape}, {len(muestras)} píxeles")

umbral = input("Ingrese el umbral de distancia: ")
umbral = float(umbral)

grupos, medias, asignaciones = algoritmo_cadena(muestras, umbral)

print("Número de grupos:", len(grupos))
for i, g in enumerate(grupos):
    print(f"Grupo {i+1}: {len(g)} muestras")

# Visualizar los grupos en la imagen
height, width, channels = img_array.shape
segmented_img = np.zeros_like(img_array)

# Asignar colores aleatorios a cada grupo
colors = {}
for i in range(len(grupos)):
    colors[i] = [random.randint(0, 255) for _ in range(3)]

# Reconstruir la imagen con colores por grupo
for idx, group_id in enumerate(asignaciones):
    row = idx // width
    col = idx % width
    segmented_img[row, col] = colors[group_id]

# Crear imagen segmentada
segmented_pil = Image.fromarray(segmented_img.astype('uint8'))
segmented_pil.save('segmented_image.png')
print("Imagen segmentada guardada como 'segmented_image.png'")  # Solo mostrar cantidad para no imprimir todo