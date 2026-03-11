import cv2
import os
import time
from ultralytics import YOLO

# 1. Cargar el modelo YOLOv8 Small (Punto 2.1)
model = YOLO('yolov8s.pt')

# 2. Capturar una imagen de la webcam
cap = cv2.VideoCapture(0)
# Dejamos un pequeño delay para que la cámara autoenfoque
time.sleep(1) 
ret, frame = cap.read()
cap.release()

if ret:
    # 3. Hacer la inferencia (Detección de objetos)
    results = model(frame)

    # 4. Dibujar las detecciones en la imagen (.plot() ya nos da el dibujo hecho)
    # Cogemos el primer resultado [0]
    frame_con_detecciones = results[0].plot()

    # 5. Asegurarnos de que existe la carpeta para guardar
    if not os.path.exists('outputs'):
        os.makedirs('outputs')

    # 6. Guardar en .jpg y en .png (Punto 2.1)
    path_jpg = 'outputs/deteccion.jpg'
    path_png = 'outputs/deteccion.png'
    
    cv2.imwrite(path_jpg, frame_con_detecciones)
    cv2.imwrite(path_png, frame_con_detecciones)

    # 7. --- COMPARATIVA DE OCUPACIÓN ---
    size_jpg = os.path.getsize(path_jpg) / 1024  # Pasamos a KB
    size_png = os.path.getsize(path_png) / 1024  # Pasamos a KB

    print("\n" + "="*30)
    print(" RESULTADOS DE OCUPACIÓN ")
    print("="*30)
    print(f"Foto en JPG: {size_jpg:.2f} KB")
    print(f"Foto en PNG: {size_png:.2f} KB")
    print(f"El PNG es {size_png/size_jpg:.1f} veces más grande que el JPG")
    print("="*30)

else:
    print("Error: No se pudo acceder a la cámara.")