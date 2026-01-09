import os
from PIL import Image

# Carpeta de entrada y salida
input_dir = "../imgs/newImagenes"
output_dir = "imgs/imag_recortadas"

# ===== CONFIGURACIÓN: Cambiar dimensiones aquí =====
TARGET_WIDTH = 200
TARGET_HEIGHT = 200
# ====================================================

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

print(f"Tamaño mínimo encontrado: {min_width} x {min_height}")

# Paso 2: recortar y re-escalar todas las imágenes
for img_name in imagenes:
    img_path = os.path.join(input_dir, img_name)
    with Image.open(img_path) as img:
        w, h = img.size

        # Recortar al tamaño mínimo (centrado)
        left = (w - min_width) // 2
        top = (h - min_height) // 2
        right = left + min_width
        bottom = top + min_height

        img_crop = img.crop((left, top, right, bottom))

        # Re-escalar manteniendo la proporción
        img_crop.thumbnail((TARGET_WIDTH, TARGET_HEIGHT), Image.Resampling.LANCZOS)
        
        # Crear imagen final con fondo blanco y centrar la imagen escalada
        final_img = Image.new("RGB", (TARGET_WIDTH, TARGET_HEIGHT), color="white")
        offset_x = (TARGET_WIDTH - img_crop.width) // 2
        offset_y = (TARGET_HEIGHT - img_crop.height) // 2
        final_img.paste(img_crop, (offset_x, offset_y))

        save_path = os.path.join(output_dir, img_name)
        final_img.save(save_path)

print(f"Imágenes guardadas en: {output_dir}")
print(f"Tamaño final de las imágenes: {TARGET_WIDTH} x {TARGET_HEIGHT}")
