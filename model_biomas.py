import numpy as np
from PIL import Image
import random
import os
from sklearn.model_selection import train_test_split
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
    img = Image.open(img_path)
    img = img.resize((200, 200))
    img = img.convert('RGB')
    img_array = np.array(img)
    height, width, channels = img_array.shape
    muestras = img_array.reshape((height * width, channels)).astype(float)
    grupos, medias, asignaciones = algoritmo_cadena(muestras, umbral)
    num_groups = len(grupos)
    avg_group_size = np.mean([len(g) for g in grupos]) if grupos else 0
    mean_color = np.mean(medias, axis=0) if medias else np.zeros(3)
    features = [num_groups, avg_group_size] + mean_color.tolist()
    return features

# Parámetros
umbral = 50  # Puedes ajustar este umbral

# Cargar datos
data = []
labels = []
img_dir = 'img_recortadas'

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

X = np.array(data)
y = labels

print(f"Dataset: {len(X)} muestras, {len(set(y))} clases")

# Dividir en train/test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Entrenar modelo
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# Evaluar
y_pred = clf.predict(X_test)
print("Classification Report:")
print(classification_report(y_test, y_pred))

# Guardar modelo
joblib.dump(clf, 'modelo_biomas.pkl')
print("Modelo guardado como 'modelo_biomas.pkl'")

# Función para predecir en una nueva imagen
def predecir_bioma(img_path, umbral=50):
    feat = extract_features(img_path, umbral)
    pred = clf.predict([feat])
    return pred[0]

# Ejemplo de uso
print(predecir_bioma('img_recortadas/playa01.png'))