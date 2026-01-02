import os
from PIL import Image

# Carpeta de entrada y salida
input_dir = "imgs"
output_dir = "imagenes_recortadas"

os.makedirs(output_dir, exist_ok=True)

# Obtener lista de imágenes
imagenes = [f for f in os.listdir(input_dir)
             if f.lower().endswith((".png", ".jpg", ".jpeg"))]

# Paso 1: obtener dimensiones mínimas
min_width = float("inf")
min_height = float("inf")

for img_name in imagenes:
    img_path = os.path.join(input_dir, img_name)
    with Image.open(img_path) as img:
        w, h = img.size
        min_width = min(min_width, w)
        min_height = min(min_height, h)

print(f"Tamaño final: {min_width} x {min_height}")

# Paso 2: recortar todas las imágenes
for img_name in imagenes:
    img_path = os.path.join(input_dir, img_name)
    with Image.open(img_path) as img:
        w, h = img.size

        left = (w - min_width) // 2
        top = (h - min_height) // 2
        right = left + min_width
        bottom = top + min_height

        img_crop = img.crop((left, top, right, bottom))

        save_path = os.path.join(output_dir, img_name)
        img_crop.save(save_path)

print("Imágenes guardadas en:", output_dir)
