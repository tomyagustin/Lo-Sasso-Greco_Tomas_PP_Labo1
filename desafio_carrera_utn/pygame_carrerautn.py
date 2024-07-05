from datos import lista
from colores import *

import pygame
import sys
import json

pygame.init()

ANCHO_VENTANA = 1024
ALTO_VENTANA = 768

pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))

pygame.display.set_caption("Desafio Carrera de Mente")

fuente = pygame.font.SysFont("Arial", 30)
texto = fuente.render("Renag", True, GREEN)
fuente = pygame.font.SysFont("Arial", 30)
fuente_rect = pygame.font.SysFont("Arial", 15)

pygame.mixer.music.load("desafio_carrera_mente/musica.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.1)

imagen_carrera_utn = pygame.image.load("desafio_carrera_utn/carrera_utn.jpg")
imagen_utn = pygame.image.load("desafio_carrera_utn/UTN.jpg")

imagen_salida = pygame.image.load("desafio_carrera_utn/Salida.png")
imagen_llegada = pygame.image.load("desafio_carrera_utn/Llegada.jpg")


colores_rectangulos = [
    ORANGE, GREEN2, YELLOW1, SKYBLUE, RED1, VIOLET, YELLOW2, GREEN1,
    ORANGE, GREEN2, YELLOW1, SKYBLUE, RED1, VIOLET, YELLOW2, GREEN
]

coordenadas_rectangulos = [
    (200, 300), (300, 300), (400, 300), (500, 300), (600, 300), (700, 300), (800, 300), (900, 300),  # Fila 1
    (200, 400), (300, 400), (400, 400), (500, 400), (600, 400), (700, 400), (800, 400), (900, 400)   # Fila 2
]

texto_avanza = fuente_rect.render("Avanza 1", True, BLACK)
texto_retrocede = fuente_rect.render("Retrocede 1", True, BLACK)

preguntas = []
for e_lista in lista:
    pregunta_actual = []
    pregunta_actual.append(e_lista['pregunta'])
    pregunta_actual.append(e_lista['a'])
    pregunta_actual.append(e_lista['b'])
    pregunta_actual.append(e_lista['c'])
    pregunta_actual.append(e_lista['correcta'])
    pregunta_actual.append(e_lista['tema'])
    preguntas.append(pregunta_actual)

score = 0
pregunta_actual = 0
tiempo_restante = 5

pregunta = preguntas[pregunta_actual][0]
tema = preguntas[pregunta_actual][5]
etiqueta_pregunta = fuente.render(str(pregunta), True, BLACK)
etiqueta_tema = fuente.render("Tema: " + str(tema), True, BLACK)
opcion_a = fuente.render("A. " + preguntas[pregunta_actual][1], True, BLACK)
opcion_b = fuente.render("B. " + preguntas[pregunta_actual][2], True, BLACK)
opcion_c = fuente.render("C. " + preguntas[pregunta_actual][3], True, BLACK)
puntaje = fuente.render("Puntaje: " + str(score), True, BLACK)
etiqueta_tiempo = fuente.render("Tiempo: " + str(tiempo_restante), True, BLACK)

# Avanzar 1
rect_avanza = coordenadas_rectangulos[6]
x_avanza = rect_avanza[0] + (50 - texto_avanza.get_width()) // 2
y_avanza = rect_avanza[1] + (50 - texto_avanza.get_height()) // 2
pantalla.blit(texto_avanza, (x_avanza, y_avanza))

# Retroceder 1
rect_retrocede = coordenadas_rectangulos[11]
x_retrocede = rect_retrocede[0] + (50 - texto_retrocede.get_width()) // 2
y_retrocede = rect_retrocede[1] + (50 - texto_retrocede.get_height()) // 2
pantalla.blit(texto_retrocede, (x_retrocede, y_retrocede))

nombre_usuario = ""
posicion_personaje = 0

coordenadas_casillas_fila1 = coordenadas_rectangulos[:8]
coordenadas_casillas_fila2 = coordenadas_rectangulos[8:]

imagen_personaje = pygame.image.load("desafio_carrera_utn/personaje.jpg")
imagen_personaje = pygame.transform.scale(imagen_personaje, (50, 50))

def verificar_respuesta(respuesta, pregunta_actual, score, posicion_personaje):
    """ Funcion para verificar la respuesta del jugador

    Args:
        respuesta: respuesta correcta o incorrecta ingresada por el jugador
        pregunta_actual : indice de la pregunta actual
        score: puntaje actual
        posicion_personaje: posición actual del personaje
    """
    if posicion_personaje < len(coordenadas_casillas_fila1):
        if respuesta == preguntas[pregunta_actual][4]:
            score += 10
            posicion_personaje += 2
            if posicion_personaje >= len(coordenadas_casillas_fila1):
                posicion_personaje = len(coordenadas_casillas_fila1) + len(coordenadas_casillas_fila2) - 1
        else:
            posicion_personaje -= 1
            if posicion_personaje < 0:
                posicion_personaje = 0
    else:
        if respuesta == preguntas[pregunta_actual][4]:
            score += 10
            posicion_personaje -= 2
            if posicion_personaje < len(coordenadas_casillas_fila1):
                posicion_personaje = len(coordenadas_casillas_fila1)
        else:
            posicion_personaje += 1
            if posicion_personaje >= len(coordenadas_casillas_fila1) + len(coordenadas_casillas_fila2):
                posicion_personaje = len(coordenadas_casillas_fila1) + len(coordenadas_casillas_fila2) - 1

    return score, posicion_personaje

def reiniciar_pregunta(pregunta_actual, score, tiempo_restante, pregunta, tema, etiqueta_pregunta, etiqueta_tema, opcion_a, opcion_b, opcion_c, puntaje, etiqueta_tiempo):
    """
    Función para reiniciar la pregunta y actualizar las variables correspondientes

    Args:
        pregunta_actual: indice de la pregunta actual
        score: puntaje actual
        tiempo_restante: tiempo restante para la pregunta
        pregunta: texto de la pregunta actual
        tema: tema de la pregunta actual
        etiqueta_pregunta: etiqueta con el texto de la pregunta
        etiqueta_tema: etiqueta con el tema
        opcion_a: opcion A de la pregunta
        opcion_b: opcion B de la pregunta
        opcion_c: opcion C de la pregunta
        puntaje: etiqueta del puntaje
        etiqueta_tiempo: etiqueta del tiempo restante
    """
    tiempo_restante = 5
    if pregunta_actual >= len(preguntas):
        guardar_puntaje(nombre_usuario)
        mostrar_mejores_puntajes()
        pygame.quit()
        sys.exit()
    pregunta = preguntas[pregunta_actual][0]
    tema = preguntas[pregunta_actual][5]
    etiqueta_pregunta = fuente.render(str(pregunta), True, BLACK)
    etiqueta_tema = fuente.render("Tema: " + str(tema), True, BLACK)
    opcion_a = fuente.render("A. " + preguntas[pregunta_actual][1], True, BLACK)
    opcion_b = fuente.render("B. " + preguntas[pregunta_actual][2], True, BLACK)
    opcion_c = fuente.render("C. " + preguntas[pregunta_actual][3], True, BLACK)
    puntaje = fuente.render("Puntaje: " + str(score), True, BLACK)
    etiqueta_tiempo = fuente.render("Tiempo: " + str(tiempo_restante), True, BLACK)

    return tiempo_restante, pregunta, tema, etiqueta_pregunta, etiqueta_tema, opcion_a, opcion_b, opcion_c, puntaje, etiqueta_tiempo

def guardar_puntaje(nombre):
    """Funcion para guardar el puntaje en un archivo JSON, si ya existe el archivo lo lee, y si no lo crea. Guarda el top 10 de forma descendente 
    """
    nuevo_puntaje = {"nombre": nombre, "score": score}
    
    try:
        with open('desafio_carrera_utn/puntajes.json', 'r') as archivo:
            puntajes = json.load(archivo)
    except FileNotFoundError:
        puntajes = []

    puntajes.append(nuevo_puntaje)
    
    for i in range(len(puntajes) - 1):
        for j in range(i + 1, len(puntajes)):
            if 'score' in puntajes[i] and 'score' in puntajes[j]:
                if puntajes[i]['score'] < puntajes[j]['score']:
                    aux = puntajes[i]
                    puntajes[i] = puntajes[j]
                    puntajes[j] = aux

    if len(puntajes) > 10:
        puntajes = puntajes[:10]

    with open('desafio_carrera_utn/puntajes.json', 'w') as archivo:
        json.dump(puntajes, archivo)

def dibujar_mejores_puntajes(pantalla, puntajes):
    """Funcion para dibujar los mejores puntajes en pantalla

    Args:
        pantalla: ventana del juego
        puntajes: score del usuario
    """
    
    pantalla.fill(RED1)

    fuente = pygame.font.SysFont("Arial", 50)
    titulo_puntaje = fuente.render("Puntaje", True, WHITE)
    pantalla.blit(titulo_puntaje, (50, 20))

    fuente_puntajes = pygame.font.SysFont("Arial", 30)
    y = 80
    for puntaje in puntajes:
        texto_puntaje = fuente_puntajes.render(f"{puntaje['nombre']} {puntaje['score']}", True, WHITE)
        pantalla.blit(texto_puntaje, (50, y))
        y += 40

    boton_salir = pygame.draw.rect(pantalla, SKYBLUE4, (300, 500, 200, 50))
    etiqueta_boton_salir = fuente_puntajes.render("Salir", True, BLACK)
    pantalla.blit(etiqueta_boton_salir, (350, 500))
    pantalla.blit(imagen_carrera_utn, (400, 100))
    nueva_imagen_personaje = pygame.transform.scale(imagen_personaje, (70, 90))
    pantalla.blit(nueva_imagen_personaje, (250, 20))

def mostrar_mejores_puntajes():
    """
    Función para mostrar los mejores puntajes en pantalla
    """
    try:
        with open('desafio_carrera_utn/puntajes.json', 'r') as archivo:
            puntajes = json.load(archivo)
    except FileNotFoundError:
        puntajes = []

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click = pygame.mouse.get_pos()
                x = click[0]
                y = click[1]
                if 300 <= x <= 500 and 500 <= y <= 550:  # Botón Salir
                    pygame.quit()
                    sys.exit()

        dibujar_mejores_puntajes(pantalla, puntajes)
        pygame.display.flip()

screen_width = pantalla.get_width()  # Ancho
screen_height = pantalla.get_height()  # Alto
surface = pygame.Surface((screen_width, screen_height))  # Fondo
surface.fill(GREEN4)

clock = pygame.time.Clock()
flag_correr = True
ultimo_tiempo = pygame.time.get_ticks()

juego_comenzado = False

def pedir_nombre():
    nombre = ""
    input_activo = True

    while input_activo:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    input_activo = False
                elif event.key == pygame.K_BACKSPACE:
                    nombre = nombre[:-1]
                else:
                    nombre += event.unicode

        pantalla.fill(GREEN4)
        mensaje = fuente.render("Ingresa tu nombre y presiona ENTER:", True, BLACK)
        pantalla.blit(mensaje, (200, 300))
        input_surface = fuente.render(nombre, True, BLACK)
        pantalla.blit(input_surface, (300, 350))

        pygame.display.flip()

    return nombre

while flag_correr:
    tiempo_actual = pygame.time.get_ticks()
    if juego_comenzado and tiempo_actual - ultimo_tiempo >= 1000:
        ultimo_tiempo = tiempo_actual
        tiempo_restante -= 1
        etiqueta_tiempo = fuente.render("Tiempo: " + str(tiempo_restante), True, BLACK)
        if tiempo_restante <= 0:
            pregunta_actual += 1
            if pregunta_actual >= len(preguntas):
                flag_correr = False
                guardar_puntaje(nombre_usuario)
                mostrar_mejores_puntajes()
            else:
                tiempo_restante, pregunta, tema, etiqueta_pregunta, etiqueta_tema, opcion_a, opcion_b, opcion_c, puntaje, etiqueta_tiempo = reiniciar_pregunta(pregunta_actual, score, tiempo_restante, pregunta, tema, etiqueta_pregunta, etiqueta_tema, opcion_a, opcion_b, opcion_c, puntaje, etiqueta_tiempo)

    lista_eventos = pygame.event.get()
    for event in lista_eventos:
        if event.type == pygame.QUIT:
            flag_correr = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            click = pygame.mouse.get_pos()
            x = click[0]
            y = click[1]

            if not juego_comenzado:
                if 100 <= x <= 300 and 400 <= y <= 450:  # Comenzar
                    nombre_usuario = pedir_nombre()
                    juego_comenzado = True
                elif 400 <= x <= 600 and 400 <= y <= 450:  # Terminar
                    flag_correr = False
            else:
                if 50 <= x <= 200 and 200 <= y <= 230:
                    score, posicion_personaje = verificar_respuesta('a', pregunta_actual, score, posicion_personaje)
                    pregunta_actual += 1
                    if pregunta_actual >= len(preguntas):
                        flag_correr = False
                        guardar_puntaje(nombre_usuario)
                        mostrar_mejores_puntajes()
                    else:
                        tiempo_restante, pregunta, tema, etiqueta_pregunta, etiqueta_tema, opcion_a, opcion_b, opcion_c, puntaje, etiqueta_tiempo = reiniciar_pregunta(pregunta_actual, score, tiempo_restante, pregunta, tema, etiqueta_pregunta, etiqueta_tema, opcion_a, opcion_b, opcion_c, puntaje, etiqueta_tiempo)
                elif 50 <= x <= 200 and 260 <= y <= 280:
                    score, posicion_personaje = verificar_respuesta('b', pregunta_actual, score, posicion_personaje)
                    pregunta_actual += 1
                    if pregunta_actual >= len(preguntas):
                        flag_correr = False
                        guardar_puntaje(nombre_usuario)
                        mostrar_mejores_puntajes()
                    else:
                        tiempo_restante, pregunta, tema, etiqueta_pregunta, etiqueta_tema, opcion_a, opcion_b, opcion_c, puntaje, etiqueta_tiempo = reiniciar_pregunta(pregunta_actual, score, tiempo_restante, pregunta, tema, etiqueta_pregunta, etiqueta_tema, opcion_a, opcion_b, opcion_c, puntaje, etiqueta_tiempo)
                elif 50 <= x <= 200 and 310 <= y <= 335:
                    score, posicion_personaje = verificar_respuesta('c', pregunta_actual, score, posicion_personaje)
                    pregunta_actual += 1
                    if pregunta_actual >= len(preguntas):
                        flag_correr = False
                        guardar_puntaje(nombre_usuario)
                        mostrar_mejores_puntajes()
                    else:
                        tiempo_restante, pregunta, tema, etiqueta_pregunta, etiqueta_tema, opcion_a, opcion_b, opcion_c, puntaje, etiqueta_tiempo = reiniciar_pregunta(pregunta_actual, score, tiempo_restante, pregunta, tema, etiqueta_pregunta, etiqueta_tema, opcion_a, opcion_b, opcion_c, puntaje, etiqueta_tiempo)

    if posicion_personaje < len(coordenadas_casillas_fila1):
        pos_personaje = coordenadas_casillas_fila1[posicion_personaje]
    else:
        pos_personaje = coordenadas_casillas_fila2[posicion_personaje - len(coordenadas_casillas_fila1)]              

    rect_casilla6 = pygame.Rect(coordenadas_rectangulos[5][0], coordenadas_rectangulos[5][1], 50, 50)
    rect_casilla12 = pygame.Rect(coordenadas_rectangulos[11][0], coordenadas_rectangulos[11][1], 50, 50)

    if rect_casilla6.colliderect(pygame.Rect(pos_personaje[0], pos_personaje[1], 50, 50)):
        posicion_personaje += 1
        if posicion_personaje >= len(coordenadas_casillas_fila1) + len(coordenadas_casillas_fila2):
            posicion_personaje = len(coordenadas_casillas_fila1) + len(coordenadas_casillas_fila2) - 1
    elif rect_casilla12.colliderect(pygame.Rect(pos_personaje[0], pos_personaje[1], 50, 50)):
        posicion_personaje += 1
        if posicion_personaje < 0:
            posicion_personaje = 0 

    pantalla.blit(surface, (0, 0))

    if not juego_comenzado:
        boton_comenzar = pygame.draw.rect(pantalla, RED1, (100, 400, 180, 50))
        boton_terminar = pygame.draw.rect(pantalla, RED1, (400, 400, 180, 50))
        etiqueta_boton_comenzar = fuente.render("Comenzar", True, WHITE)
        etiqueta_boton_terminar = fuente.render("Terminar", True, WHITE)
        pantalla.blit(etiqueta_boton_comenzar, (110, 400))
        pantalla.blit(etiqueta_boton_terminar, (430, 400))
        imagen_utn_reescalada = pygame.transform.scale(imagen_utn, (500, 300))
        pantalla.blit(imagen_utn_reescalada, (100, 10))
    else:
        pantalla.blit(etiqueta_pregunta, (50, 100))
        pantalla.blit(etiqueta_tema, (50, 150))
        pantalla.blit(opcion_a, (50, 200))
        pantalla.blit(opcion_b, (50, 250))
        pantalla.blit(opcion_c, (50, 300))
        pantalla.blit(puntaje, (10, 10))
        pantalla.blit(etiqueta_tiempo, (10, 50))
        pantalla.blit(imagen_carrera_utn, (300, 500))
        pantalla.blit(texto_avanza, (x_avanza, y_avanza))
        pantalla.blit(texto_retrocede, (x_retrocede, y_retrocede))
        imagen_salida_reescalada = pygame.transform.scale(imagen_salida, (50, 50))
        pantalla.blit(imagen_salida_reescalada, (150, 300))
        pantalla.blit(imagen_llegada, (50, 410))

        for i in range(len(coordenadas_rectangulos)):
            pygame.draw.rect(pantalla, colores_rectangulos[i], (coordenadas_rectangulos[i][0], coordenadas_rectangulos[i][1], 50, 50))

        rect_avanza = coordenadas_rectangulos[5]
        x_avanza = rect_avanza[0] + (50 - texto_avanza.get_width()) // 2
        y_avanza = rect_avanza[1] + (50 - texto_avanza.get_height()) // 2
        pantalla.blit(texto_avanza, (x_avanza, y_avanza))

        rect_retrocede = coordenadas_rectangulos[11]
        x_retrocede = rect_retrocede[0] + (50 - texto_retrocede.get_width()) // 2
        y_retrocede = rect_retrocede[1] + (50 - texto_retrocede.get_height()) // 2
        pantalla.blit(texto_retrocede, (x_retrocede, y_retrocede))

        if posicion_personaje < len(coordenadas_casillas_fila1):
            pantalla.blit(imagen_personaje, coordenadas_casillas_fila1[posicion_personaje])
        else:
            pantalla.blit(imagen_personaje, coordenadas_casillas_fila2[posicion_personaje - len(coordenadas_casillas_fila1)])

    clock.tick(30)
    pygame.display.flip()

pygame.quit()