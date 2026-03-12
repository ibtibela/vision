import cv2
import os
import time
from ultralytics import YOLO

# 1. Cargar el modelo
model = YOLO('yolov8s.pt')

# 2. Abrir la cámara
cap = cv2.VideoCapture(0)
prev_time = 0
if not cap.isOpened():
    print("Error: No se pudo acceder a la cámara.")
    exit()

# --- CONFIGURACIÓN DE HARDWARE ---
# Opción A: "cpu" para forzar el procesador
# Opción B: 0 (o "cuda") para usar la tarjeta NVIDIA
used_device="cpu"

while True:
        ret, frame = cap.read()
        if not ret:
            print("Error al leer el frame")
            break
        # 3. Hacer la inferencia (Detección de objetos)
        # Usamos stream=True para que sea más fluido
        results = model(frame, stream=True, device=used_device, verbose=False)

        # 4. Dibujar las detecciones en la imagen
        for r in results:
            frame_con_detecciones = r.plot()

        # 5. Cálculo de FPS
        curr_time = time.time()
        tiempo_refresco = (curr_time - prev_time) if prev_time != 0 else 0
        fps = 1 / tiempo_refresco if tiempo_refresco > 0 else 0
        prev_time = curr_time

        # Mostrar FPS y tiempo de refresco (en segundos) en el frame
        cv2.putText(frame_con_detecciones, f"FPS: {int(fps)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.putText(frame_con_detecciones, f"Refresco: {tiempo_refresco*1000:.1f} ms", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

        # 6. Mostrar el vídeo
        cv2.imshow("YOLOv8 Real-Time", frame_con_detecciones)

        # 7. Salida
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Al salir del bucle, limpiamos todo
cap.release()
cv2.destroyAllWindows()