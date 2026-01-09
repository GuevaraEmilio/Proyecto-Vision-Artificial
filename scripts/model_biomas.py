import numpy as np
from PIL import Image
import random
import os
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib

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

def get_biome_label(filename):
    filename = filename.lower()
    if 'arrecife' in filename:
        return 'arrecife'
    elif 'badlands' in filename:
        return 'badlands'
    elif 'bosque' in filename:
        return 'bosque'
    elif 'cenote' in filename:
        return 'cenote'
    elif 'cerezos' in filename:
        return 'cerezos'
    elif 'cueva' in filename:
        return 'cueva'
    elif 'desierto' in filename:
        return 'desierto'
    elif 'lago' in filename:
        return 'lago'
    elif 'montana' in filename:
        return 'montana'
    elif 'pantano' in filename:
        return 'pantano'
    elif 'playa' in filename:
        return 'playa'
    elif 'pradera' in filename:
        return 'pradera'
    elif 'sabana' in filename:
        return 'sabana'
    elif 'selva' in filename:
        return 'selva'
    elif 'tundra' in filename:
        return 'tundra'
    else:
        return 'desconocido'

def extract_features(img_path, umbral):
    print(f"Procesando {img_path}")
    img = Image.open(img_path)
    img = img.resize((100, 100))  # Reducido para acelerar
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
umbral = 30  # Reducido para más grupos

# Cargar datos
data = []
labels = []
img_dir = '../imgs/img_recortadas'

for file in os.listdir(img_dir):
    if file.endswith('.png'):
        path = os.path.join(img_dir, file)
        try:
            feat = extract_features(path, umbral)
            label = get_biome_label(file)
            if label != 'desconocido':
                data.append(feat)
                labels.append(label)
        except Exception as e:
            print(f"Error procesando {file}: {e}")

print(f"Procesadas {len(data)} imágenes")

X = np.array(data)
y = labels

print(f"Dataset: {len(X)} muestras, {len(set(y))} clases")

# Guardar dataset
joblib.dump({'X': X, 'y': y}, 'dataset_biomas.pkl')
print("Dataset guardado como 'dataset_biomas.pkl'")

# Evaluar con cross-validation
clf = RandomForestClassifier(n_estimators=100, class_weight='balanced', random_state=42)
scores = cross_val_score(clf, X, y, cv=5, scoring='balanced_accuracy')
print(f"Balanced Accuracy CV: {scores.mean():.2f} (+/- {scores.std() * 2:.2f})")

# Entrenar en todo el dataset para guardar
clf.fit(X, y)

# Guardar modelo
joblib.dump(clf, 'modelo_biomas.pkl')
print("Modelo guardado como 'modelo_biomas.pkl'")

# Función para predecir en una nueva imagen
def predecir_bioma(img_path, umbral=40):
    feat = extract_features(img_path, umbral)
    pred = clf.predict([feat])
    return pred[0]

# Ejemplo de uso
print(predecir_bioma('img_recortadas/playa01.png'))