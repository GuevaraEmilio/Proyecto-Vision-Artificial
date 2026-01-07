import numpy as np
from PIL import Image
import random
import os
import joblib
import sys
import tkinter as tk
from tkinter import filedialog

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

def extract_features(img_path, umbral):
    print(f"Procesando {img_path}")
    img = Image.open(img_path)
    img = img.resize((100, 100))
    img = img.convert('RGB')
    img_array = np.array(img)
    height, width, channels = img_array.shape
    muestras = img_array.reshape((height * width, channels)).astype(float)
    grupos, medias, asignaciones = algoritmo_cadena(muestras, umbral)
    num_groups = len(grupos)
    group_sizes = [len(g) for g in grupos]
    avg_group_size = np.mean(group_sizes) if group_sizes else 0
    std_group_size = np.std(group_sizes) if group_sizes else 0
    min_group_size = min(group_sizes) if group_sizes else 0
    max_group_size = max(group_sizes) if group_sizes else 0
    num_large_groups = sum(1 for size in group_sizes if size > avg_group_size) if group_sizes else 0
    mean_color = np.mean(medias, axis=0) if medias else np.zeros(3)
    var_color = np.var(medias, axis=0) if medias else np.zeros(3)
    features = [num_groups, avg_group_size, std_group_size, min_group_size, max_group_size, num_large_groups] + mean_color.tolist() + var_color.tolist()
    print(f"  Grupos: {num_groups}, Tamaño prom: {avg_group_size:.2f}, Std: {std_group_size:.2f}, Min: {min_group_size}, Max: {max_group_size}, Grandes: {num_large_groups}")
    return features

# Parámetros
umbral = 50  # Mismo que en el entrenamiento

# Cargar modelo
clf = joblib.load('modelo_biomas.pkl')
print("Modelo cargado.")

# Cargar dataset (opcional, para referencia)
# data = joblib.load('dataset_biomas.pkl')
# print(f"Dataset cargado: {len(data['X'])} muestras")

# Seleccionar imagen desde una ventana
root = tk.Tk()
root.withdraw()  # Ocultar la ventana principal
img_path = filedialog.askopenfilename(
    title="Selecciona una imagen",
    filetypes=[("Imágenes", "*.png *.jpg *.jpeg *.bmp *.tiff")]
)
if not img_path:
    print("No se seleccionó ninguna imagen.")
    sys.exit(1)

if not os.path.exists(img_path):
    print(f"Imagen no encontrada: {img_path}")
    sys.exit(1)

# Extraer features y predecir
features = extract_features(img_path, umbral)
pred = clf.predict([features])
print(f"El bioma predicho para {img_path} es: {pred[0]}")