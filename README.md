# Robot Reconocedor de gestos manuales
Aplicación que hace el reconocimiento de cinco gestos
manuales tales como: Mano abierta, dedo índice levantado, dedo índice y medio levantados, dedos
pulgar y meñique levantados y un puño. El proceso fue aplicado en imágenes captadas al instante
con una cámara de vídeo. Así mismo, los gestos reconocidos son usados para controlar la dinámica,
sonido y luces de un robot móvil.

La programación de la aplicación se realizó en el lenguaje de programación Python y se traba-
jó sobre el sistema operativo Raspberry Pi Os. A partir de ello, se realizó el entrenamiento de un
modelo de YOLOv8 nano con un conjunto de datos propio generado con 6296 imágenes de gestos
manuales. La programación fue integrada en una computadora Raspberry Pi 3B+, mediante la cual
se controlan los distintos actuadores del robot móvil, permitiendo así, realizar tareas como desplazar-
se, activar luces y activar sonido, únicamente respondiendo ante los estímulos de la mano del usuario.

## Tecnologías
- Python
- Raspberry Pi
- OpenCV
- GPIO
- YOLOv8n

## Palabras clave
- Detección de destos manuales
- Vision artificial
- Procesamiento digital de imagenes
- Robot movil

## Hardware
- Raspberry Pi 3B+
- Picamera 5mp
- motores 5vcd
- Bocina 3W
- Leds de colores

## Entrenamiento

5 Gestos manuales:
- Palma		
- Índice y medio levantados
- Puño		
- Índice levantado
- Pulgar y meñique levantados

Division de los datos
- 6300 Imágenes en total
- 1260 Imágenes para cada gesto

80% Entrenamiento      20% Validación

![image](https://github.com/OmarFloresSanchez/Robot-TT/blob/main/Gestos.png)

## Detecciones

![image](https://github.com/OmarFloresSanchez/Robot-TT/blob/main/Evidencias1.png)
![image](https://github.com/OmarFloresSanchez/Robot-TT/blob/main/Evidencias2.png)

## Desempeño

Se realizaron 50 pruebas para evaluar el desempeño del sistema. Los resultados se muestran en la siguiente matriz
de confusión.

![image](https://github.com/OmarFloresSanchez/Robot-TT/blob/main/Matriz.png)

## Fotos del robot
![image](https://github.com/OmarFloresSanchez/Robot-TT/blob/main/Foto1.png)
![image](https://github.com/OmarFloresSanchez/Robot-TT/blob/main/Foto2.png)
## Link
[(Pruevas con el robot)](https://www.youtube.com/watch?v=SQMnvYvLVB0)
