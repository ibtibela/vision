import cv2
import os
import time  # Punto 1.7: Librería para medir tiempo

# Creamos la carpeta 'images' si no existe para evitar errores al guardar
if not os.path.exists('images'):
    os.makedirs('images')

# Iniciamos la conexión con la cámara (0 es la webcam por defecto)
cap = cv2.VideoCapture(0)

# Leemos un solo fotograma (frame)
ret, frame = cap.read() 

if ret:
    # --- Punto 1.1: Guardamos el array de la imagen en un archivo físico .jpg ---
    cv2.imwrite('images/captura_paso1.jpg', frame)
    
    # --- Punto 1.2: El 'shape' nos da (alto, ancho, canales de color) ---
    # Accedemos a los índices para imprimir la resolución
    print(f"Resolución: Ancho {frame.shape[1]} x Alto {frame.shape[0]}")

# --- Puntos 1.3 y 1.4 (Vídeo en directo) ---

print("Iniciando modo LIVE. Presiona 'q' para salir.")

# --- Punto 1.7: Variable para el cálculo de FPS ---
prev_time = 0

while True:
    # Capturamos frame a frame para el vídeo
    ret, frame_live = cap.read()
    
    if not ret:
        break

    # --- Punto 1.7: Cálculo de tiempo de refresco y FPS ---
    curr_time = time.time()
    tiempo_refresco = (curr_time - prev_time) if prev_time != 0 else 0
    fps = 1 / tiempo_refresco if tiempo_refresco > 0 else 0
    prev_time = curr_time

    # --- Punto 1.5 (Dibujar círculo en el centro) ---
    alto, ancho, _ = frame_live.shape
    cv2.circle(frame_live, (ancho // 2, alto // 2), 50, (0, 255, 0), 3)

    # --- PUNTO 1.8: Mostrar FPS y tiempo de refresco (en segundos) en el frame ---
    # Ponemos los FPS arriba
    cv2.putText(frame_live, f"FPS: {int(fps)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    # Ponemos el tiempo de refresco debajo (en milisegundos para que se entienda mejor)
    cv2.putText(frame_live, f"Refresco: {tiempo_refresco*1000:.1f} ms", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
    # --- Punto 1.6 (Crear imagen pequeña) ---
    frame_mini = cv2.resize(frame_live, (100, 100))

    # Punto 1.4: Mostrar la cámara en una ventana en LIVE
    cv2.imshow("Webcam LIVE", frame_live)

    # --- Mostrar la ventana pequeña ---
    cv2.imshow("Miniatura 100x100", frame_mini)

    # Punto 1.3: El programa se detiene si pulsas la 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Al final del todo, liberamos y cerramos
cap.release()
cv2.destroyAllWindows()
