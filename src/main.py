import cv2
import os

# Creamos la carpeta 'images' si no existe para evitar errores al guardar
if not os.path.exists('images'):
    os.makedirs('images')

# Iniciamos la conexión con la cámara (0 es la webcam por defecto)
cap = cv2.VideoCapture(0)

# Leemos un solo fotograma (frame)
ret, frame = cap.read() 

if ret:
    # Punto 1.1: Guardamos el array de la imagen en un archivo físico .jpg
    cv2.imwrite('images/captura_paso1.jpg', frame)
    
    # Punto 1.2: El 'shape' nos da (alto, ancho, canales de color)
    # Accedemos a los índices para imprimir la resolución
    print(f"Resolución: Ancho {frame.shape[1]} x Alto {frame.shape[0]}")