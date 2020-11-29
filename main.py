#Sara Zavala
#Ultimo proyecto
#Graficas por computador

import pygame
from pygame.locals import *
from pygame.math import Vector2, Vector3

from gl import Renderer, Model
import shaders
import glm

deltaTime = 0.0

pygame.init()
clock = pygame.time.Clock()
screenSize = (960, 540)
screen = pygame.display.set_mode(screenSize, DOUBLEBUF | OPENGL)

maxZoom = 2
zoom = 0
r = Renderer(screen)
r.camPos.z = 3
r.pointLight.x = 1
r.pointLight.y = 2
r.pointLight.z = 3

offset = Vector2(r.camPos[0],r.camPos[2])
angle = 0

r.setShaders(shaders.vertex_shader, shaders.fragment_shader)

active_shader = 0
r.modelList.append(Model('./Models/model.obj', './Textures/model.bmp', 1))
r.modelList.append(Model('./Models/spiderman.obj', './Textures/spider1.bmp', 1))
r.modelList.append(Model('./Models/doctor.obj', './Textures/doctor.bmp', 1))
r.modelList.append(Model('./Models/hulk.obj', './Textures/hulk.bmp', 0.5))

isPlaying = True
pygame.mixer_music.load('./Music/sponge.mp3')
pygame.mixer.music.play(-1)

while isPlaying:

    keys = pygame.key.get_pressed()
    # Movimiento de camara horizontalmente
    if keys[pygame.K_a]:
        r.camRot.y -= 24* deltaTime
        angle += 25 * deltaTime
        newPos = offset.rotate(angle)
        r.camPos.x = newPos[0]
        r.camPos.z = newPos[1]
    if keys[pygame.K_d]:
        r.camRot.y += 25 * deltaTime
        angle -= 25 * deltaTime
        newPos = offset.rotate(angle)
        r.camPos.x = newPos[0]
        r.camPos.z = newPos[1]

    # Zoom in and Zoom out de camara
    if keys[pygame.K_w]:
        if zoom > -maxZoom:
            offset[1] -= 1 * deltaTime
            r.camPos.z -= 1 * deltaTime
            zoom -= 1 * deltaTime
    if keys[pygame.K_s]:
        if zoom < maxZoom:
            offset[1] += 1 * deltaTime
            r.camPos.z += 1 * deltaTime
            zoom += 1 * deltaTime

    #Movimiento de camara vertical
    if keys[pygame.K_UP]:
        r.camPos.y += 1 * deltaTime
    if keys[pygame.K_DOWN]:
        r.camPos.y -= 1 * deltaTime
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            isPlaying = False
        elif ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_1:
                r.filledMode()
            elif ev.key == pygame.K_2:
                r.wireframeMode
            elif ev.key == pygame.K_ESCAPE:
                isPlaying = False

        elif ev.type == pygame.KEYUP:
            if ev.key == pygame.K_RIGHT:
                if r.active_model != 3:
                    r.active_model += 1
                else:
                    r.active_model = 0
            elif ev.key == pygame.K_LEFT:
                if r.active_model != 0:
                    r.active_model -= 1
                else:
                    r.active_model = 3
            elif ev.key == pygame.K_PERIOD:
                if active_shader != 5:
                    active_shader += 1
                else:
                    active_shader = 0
                if active_shader == 0:
                    r.setShaders(shaders.vertex_shader, shaders.fragment_shader)
                elif active_shader == 1:
                    r.setShaders(shaders.vertex_shader, shaders.fragment_neg_shader)
                elif active_shader == 2:
                    r.setShaders(shaders.reverse_vertex_shader, shaders.fragment_shader)
                elif active_shader == 3:
                    r.setShaders(shaders.reverse_vertex_shader, shaders.fragment_neg_shader)
                elif active_shader == 4:
                    r.setShaders(shaders.toon_vertex_shader, shaders.fragment_shader)
                elif active_shader == 5:
                    r.setShaders(shaders.vertex_shader, shaders.fragment_static_shader)

    # Main Renderer Loop
    r.render()
    pygame.display.flip()
    clock.tick(60)
    deltaTime = clock.get_time() / 1000
pygame.quit()
