import subprocess
from picamera2 import Picamera2 
import cv2
import joblib
import numpy as np
import RPi.GPIO as GPIO
from ultralytics import YOLO
from scipy.stats import skew


comando= "mpg123 /home/ezio/Music/Op.mp3"
subprocess.run(comando, shell=True, check=True)


"""[+*+*+*!+*+*!+*!!!!!!!¡¡¡¡////________COSITAS DE LOS MOTORES________\\\¡¡¡>"""
#Modo de pines
GPIO.setmode(GPIO.BOARD)
# Configuración del pin PWM
PIN2 = 16 # Cambia al pin que estás usando
PIN1 = 18
PIN3 = 13 # Cambia al pin que estás usando
PIN4 = 11
FRECUENCIA_PWM = 100
#Salidas
GPIO.setup(PIN1, GPIO.OUT)
GPIO.setup(PIN2, GPIO.OUT)
GPIO.setup(PIN3, GPIO.OUT)
GPIO.setup(PIN4, GPIO.OUT)
#PWMs
pwm1 = GPIO.PWM(PIN2, FRECUENCIA_PWM)
pwm2 = GPIO.PWM(PIN1, FRECUENCIA_PWM)
pwm3 = GPIO.PWM(PIN3, FRECUENCIA_PWM)
pwm4 = GPIO.PWM(PIN4, FRECUENCIA_PWM)
#Inician
pwm1.start(0)
pwm2.start(0)
pwm3.start(0)
pwm4.start(0)

"""[+*+*+*!+*+*!+*!!!!!!!¡¡¡¡////________PA QUE NO SE ACABE LA RAM________\\\>"""
def configurar_swap():
    comandos = [
        "sudo swapon /swapfile",
        "sudo swapon /swapfile2",
        "sudo swapon /swapfile3",
        "sudo swapon /swapfile4"
    ]
    for comando in comandos:
        resultado = subprocess.run(comando, shell=True, capture_output=True, text=True)
        if resultado.returncode != 0:
            print(f"Error ejecutando {comando}: {resultado.stderr}")
    resultado = subprocess.run("free -h", shell=True, capture_output=True, text=True)
    print(resultado.stdout)

"""[+*+*+*!+*+*!+*!!!!!!!¡¡¡¡////________MAMADAS INICIALES XD________\\\¡¡¡¡!>"""
configurar_swap()
#Inicia
model = YOLO("/home/ezio/picamera2/Ra/Unravel.pt")
clases={0:"Palma",1:"Puño",2:"Avanza",3:"Andiamo",4:"Cuernitos"}
# Función para procesar la imagen de la cámara y detectar dedos

comando= "mpg123 /home/ezio/Music/Trueno.mp3"
subprocess.run(comando, shell=True, check=True)


"""[+*+*+*!+*+*!+*!!!!!!!¡¡¡¡////________MEJORA DE IMAGE________\\\¡¡¡¡!>"""

def gamma(image, gamma):
    inv_gamma = 1.0 / gamma
    table = np.array([( (i / 255.0) ** inv_gamma ) * 255
                      for i in np.arange(256)]).astype("uint8")
    return cv2.LUT(image, table)
def brillo1(frame):
    img=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    promedio = np.mean(img)
    return promedio
def saturacion(frame,factor):
    img = frame
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    s = np.clip(s * factor, 0, 255).astype(np.uint8)
    hsv_mod = cv2.merge([h, s, v])
    img_saturada = cv2.cvtColor(hsv_mod, cv2.COLOR_HSV2BGR)
    return img_saturada
def coloracion(img,valor):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    h = (h + valor) % 180
    hsv_mod = cv2.merge([h, s, v])
    img_mod = cv2.cvtColor(hsv_mod, cv2.COLOR_HSV2BGR)
    return img_mod
def cambio_brillo(img,nivel):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    limite = 255 - nivel
    v[v > limite] = 255
    v[v <= limite] = v[v <= limite] + nivel
    hsv_mod = cv2.merge([h, s, v])
    img_brillo = cv2.cvtColor(hsv_mod, cv2.COLOR_HSV2BGR)
    return img_brillo
def contraste(img, nivel):
    alpha = nivel  # Contraste (1.0 = igual, >1.0 = más contraste, <1.0 = menos)
    beta = 0     # Brillo adicional
    img_contraste = cv2.convertScaleAbs(img, alpha=alpha, beta=beta)
    return img_contraste
def temperatura(img,factor_b, factor_g, factor_r):
    b, g, r = cv2.split(img.astype(np.float32))
    b = np.clip(b * factor_b, 0, 255)
    r = np.clip(r * factor_r, 0, 255)
    g = np.clip(g * factor_g, 0, 255)
    img_out = cv2.merge([b.astype(np.uint8), g.astype(np.uint8), r.astype(np.uint8)])
    return img_out
def desv(frame):
    img=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    desviacion=np.std(img)
    return desviacion
def binario(frame,umbral):
    img=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, binaria = cv2.threshold(img, umbral, 255, cv2.THRESH_BINARY_INV)
    b,g,r=cv2.split(frame.astype(np.float32))
    b=binaria
    g=binaria
    r=binaria
    chida=cv2.merge([b.astype(np.uint8),g.astype(np.uint8),r.astype(np.uint8)])
    return chida
def promedio(frame):
    b,g,r=cv2.split(frame.astype(np.float32))
    mediab=np.mean(b)
    mediag=np.mean(g)
    mediar=np.mean(r)
    return mediab,mediag,mediar
def momentos(frame):
    lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
    L = lab[:, :, 0]
    mean_L = np.mean(L)            # Media
    var_L = np.var(L)              # Varianza
    skew_L = skew(L.flatten()) 
    return mean_L,var_L,skew_L
def caracterizador(frame):
    car1=float(brillo1(frame))
    car2=float(desv(frame))
    car3,car4,car5=promedio(frame)
    car6,car7,car8=momentos(frame)
    arr=np.array([car1,car2,car3,car4,car5,car6,car7,car8])
    return arr



"""[+*+*+*!+*+*!+*!!!!!!!¡¡¡¡////________RUNNING IN MY HEAD________\\\¡¡¡¡!>"""
def procesar_imagen(foto):
    results = model.predict(source=frame, imgsz=640, conf=0.5, stream=False)[0]
    for box in results.boxes:
        #conf=float(box.conf[0])
        #if conf > 0.85:
        cls=int(box.cls[0])
        tipo=clases.get(cls,f"Clase{cls}")
        #print(tipo)
        #CUENTADEDOS_______________________________________________________#

        if tipo=="Avanza":
            pwm1.ChangeDutyCycle(43)
            pwm2.ChangeDutyCycle(43)
            pwm3.ChangeDutyCycle(43)
            pwm4.ChangeDutyCycle(43)
            #comando=comando = "mpg123 /home/ezio/Robot12.mp3"
            #subprocess.run(comando, shell=True, check=True)
            #print("Camina")


        if tipo=="Andiamo":
            pwm1.ChangeDutyCycle(60)
            pwm2.ChangeDutyCycle(60)
            pwm3.ChangeDutyCycle(60)
            pwm4.ChangeDutyCycle(60)
            #comando=comando = "mpg123 /home/ezio/Robot3.mp3"
            #subprocess.run(comando, shell=True, check=True)
            #print("Andiamo")


        if tipo=="Palma":
            pwm1.ChangeDutyCycle(0)
            pwm2.ChangeDutyCycle(0)
            pwm3.ChangeDutyCycle(0)
            pwm4.ChangeDutyCycle(0)
            comando=comando = "mpg123 /home/ezio/Music/Trueno.mp3"
            subprocess.run(comando, shell=True, check=True)
            #print("Detende")


        if tipo=="Puño":
            comando=comando = "mpg123 /home/ezio/Robot5.mp3"
            subprocess.run(comando, shell=True, check=True)
            #print("Puch")


        if tipo=="Cuernitos":
            comando=comando = "mpg123 /home/ezio/Robot6.mp3"
            subprocess.run(comando, shell=True, check=True)
            #print("Cuernitos")
    return

"""[+*+*+*!+*+*!+*!!!!!!!¡¡¡¡////________VOID LOOP________\\\¡¡¡¡!>"""
knn = joblib.load("/home/ezio/picamera2/Ra/naomixanat.pkl")
# Inicialización de la cámara
try:
    picam2 = Picamera2()
    picam2.start()
    while True:
        frame = picam2.capture_array()
        # Convertir de BGRA a RGB (si es necesario)
        if frame.shape[2] == 4:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2RGB)
        else:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        #KNN
        nueva_instancia = caracterizador(frame)
        prediccion = knn.predict([nueva_instancia])
        #CAMBIO DE LUZ
        if prediccion==1:
            frame=gamma(frame,2.45)
            frame=cambio_brillo(frame,51.5)
            frame=contraste(frame,1.045)
            frame=saturacion(frame,1.15)
            frame=temperatura(frame,factor_b=0.885,factor_g=0.975,factor_r=1.135)

        if prediccion==2:
            frame=binario(frame,100)
        prediccion = knn.predict([nueva_instancia])
        procesar_imagen(frame)
except KeyboardInterrupt:
    print("Interrupción por teclado.")
finally:
    picam2.stop()
