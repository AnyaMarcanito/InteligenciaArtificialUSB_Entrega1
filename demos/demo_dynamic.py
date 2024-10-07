import sys
import os
import random
import pygame

# Añadir el directorio principal al sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from vector import Vector
from images import cargar_imagenes
from behaviors.seek import Seek
from behaviors.arrive import Arrive
from behaviors.flee import Flee
from behaviors.wander import Wander
from kinematic import Kinematic

# Inicialización de Pygame y configuración de la pantalla
pygame.init()
width, height = 1280, 720
pantalla = pygame.display.set_mode((width, height))

# Cargar las imágenes
imagenes = cargar_imagenes()
background = imagenes["background"]
background2 = imagenes["background2"]

# Crear el personaje del jugador
player_kinematic = Kinematic(Vector(600, 600), 0, Vector(0, 0), 0)
player_image = imagenes["sakuraFlying"]

# Crear otros personajes con jugador como objetivo
wander_kinematic_light = Kinematic(Vector(100, 100), 0, Vector(0, 0), 0)
wander_image_light = imagenes["clowCardTheLight"]

wander_kinematic_dark = Kinematic(Vector(150, 150), 0, Vector(0, 0), 0)
wander_image_dark = imagenes["clowCardTheDark"]

wander_kinematic_shadow = Kinematic(Vector(200, 200), 0, Vector(0, 0), 0)
wander_image_shadow = imagenes["clowCardTheShadow"]

wander_kinematic_sleep = Kinematic(Vector(250, 250), 0, Vector(0, 0), 0)
wander_image_sleep = imagenes["clowCardTheSleep"]

wander_kinematic_flower = Kinematic(Vector(300, 300), 0, Vector(0, 0), 0)
wander_image_flower = imagenes["clowCardTheFlower"]

seek_kinematic = Kinematic(Vector(350, 350), 0, Vector(0, 0), 0)
seek_image = imagenes["yueFlying"]

arrive_kinematic = Kinematic(Vector(400, 400), 0, Vector(0, 0), 0)
arrive_image = imagenes["eriolFlying"]

flee_kinematic = Kinematic(Vector(450, 450), 0, Vector(0, 0), 0)
flee_image = imagenes["keroFlying"]

# Asignar comportamientos
wander_behavior_light = Wander(wander_kinematic_light, wanderOffset=5, wanderRadius=10, wanderRate=1, maxAcceleration=100)
wander_behavior_dark = Wander(wander_kinematic_dark, wanderOffset=5, wanderRadius=10, wanderRate=1, maxAcceleration=100)
wander_behavior_shadow = Wander(wander_kinematic_shadow, wanderOffset=5, wanderRadius=10, wanderRate=1, maxAcceleration=100)
wander_behavior_sleep = Wander(wander_kinematic_sleep, wanderOffset=5, wanderRadius=10, wanderRate=1, maxAcceleration=100)
wander_behavior_flower = Wander(wander_kinematic_flower, wanderOffset=5, wanderRadius=10, wanderRate=1, maxAcceleration=100)
seek_behavior = Seek(seek_kinematic, player_kinematic, maxAcceleration=100)
arrive_behavior = Arrive(arrive_kinematic, player_kinematic, maxAcceleration=100, maxSpeed=50, targetRadius=10, slowRadius=50)
flee_behavior = Flee(flee_kinematic, player_kinematic, maxAcceleration=80, fleeRadius=300)  # Definir fleeRadius

personajes = [
    (wander_kinematic_light, wander_image_light, wander_behavior_light),
    (wander_kinematic_dark, wander_image_dark, wander_behavior_dark),
    (wander_kinematic_shadow, wander_image_shadow, wander_behavior_shadow),
    (wander_kinematic_sleep, wander_image_sleep, wander_behavior_sleep),
    (wander_kinematic_flower, wander_image_flower, wander_behavior_flower),
    (seek_kinematic, seek_image, seek_behavior),
    (arrive_kinematic, arrive_image, arrive_behavior),
    (flee_kinematic, flee_image, flee_behavior),
    (player_kinematic, player_image, None)  # El jugador no tiene comportamiento
]

# Función para actualizar la posición del jugador con el mouse
def actualizar_posicion_jugador(evento, jugador):
    if evento.type == pygame.MOUSEMOTION:
        jugador.position = Vector(evento.pos[0], evento.pos[1])

# Función para verificar colisiones con los bordes de la pantalla
def verificar_colisiones_con_bordes(kinematic, width, height):
    if kinematic.position.x < 0:
        kinematic.position.x = 0
        kinematic.velocity.x = -kinematic.velocity.x
    elif kinematic.position.x > width:
        kinematic.position.x = width
        kinematic.velocity.x = -kinematic.velocity.x

    if kinematic.position.y < 0:
        kinematic.position.y = 0
        kinematic.velocity.y = -kinematic.velocity.y
    elif kinematic.position.y > height:
        kinematic.position.y = height
        kinematic.velocity.y = -kinematic.velocity.y

# Iniciar el bucle del juego
def game_loop(pantalla, background, personajes, width, height, fps):
    clock = pygame.time.Clock()
    running = True
    maxSpeed = 200
    fleeRadius = 300  # Definir el radio de fuga

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            actualizar_posicion_jugador(event, player_kinematic)

        pantalla.blit(background, (0, 0))

        for kinematic, image, behavior in personajes:
            if behavior:
                steering = behavior.getSteering()
                if steering:
                    kinematic.update_with_steering(steering, maxSpeed, 1/fps)  # Cambiar update por update_with_steering
            # Verificar colisiones solo para comportamientos de wandering
            if isinstance(behavior, Wander):
                verificar_colisiones_con_bordes(kinematic, width, height)
            pantalla.blit(image, (kinematic.position.x, kinematic.position.y))

        # Dibujar el radio de fuga alrededor del cursor
        pygame.draw.circle(pantalla, (255, 0, 0), (int(player_kinematic.position.x), int(player_kinematic.position.y)), fleeRadius, 1)

        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()

# Ejecutar el bucle del juego
game_loop(pantalla, background2, personajes, width, height, 60)