import cv2
import os
import time
from ultralytics import YOLO

# 1. Cargar el modelo (probar con 'yolov8s.pt', 'yolov8m.pt', 'yolov8l.pt' )
model = YOLO('yolov8l.pt')

# 2. Abrir la cámara
cap = cv2.VideoCapture(0)
prev_time = 0
if not cap.isOpened():
    print("Error: No se pudo acceder a la cámara.")
    exit()

# --- CONFIGURACIÓN DE HARDWARE ---
# Opción A: "cpu" para forzar el procesador
# Opción B: 0 (o "cuda") para usar la tarjeta NVIDIA
used_device="cuda"

while True:
        t_inicio = time.time()  # Empieza el cronómetro del ciclo total
        # 1. Medir toma de imagen
        t_captura_start = time.time()
        ret, frame = cap.read()
        t_captura = (time.time() - t_captura_start) * 1000
        if not ret:
            print("Error al leer el frame")
            break
        # 2. Medir Procesado (Inferencia)
        t_inferencia_start = time.time()
        results = model(frame, stream=True, device=used_device, verbose=False)
        
        for r in results:
            frame_con_detecciones = r.plot()
            
        t_inferencia = (time.time() - t_inferencia_start) * 1000

        # 3. Cálculo de FPS y Ciclo Total
        t_ciclo_total = (time.time() - t_inicio) * 1000 
        fps = 1000 / t_ciclo_total if t_ciclo_total > 0 else 0

        # 4. Mostrar FPS y tiempos en el frame
        cv2.putText(frame_con_detecciones, f"FPS: {int(fps)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(frame_con_detecciones, f"Ciclo Total: {t_ciclo_total:.1f} ms", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(frame_con_detecciones, f"Inferencia: {t_inferencia:.1f} ms", (10, 105), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
        cv2.putText(frame_con_detecciones, f"Captura: {t_captura:.1f} ms", (10, 140), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)        # 6. Mostrar el vídeo
        cv2.imshow("YOLOv8 Real-Time", frame_con_detecciones)

        # 7. Salida
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Al salir del bucle, limpiamos todo
cap.release()
cv2.destroyAllWindows()