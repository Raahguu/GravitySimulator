import pygame
from pVectors import Vector2
import math
import time

GRAVITY = 6.6743*10**-11

class body:
    bodies : list["body"] = []
    def __init__(self, mass : int, location : list[int, int], color : str):
        self.mass = mass
        self.location = Vector2(location)
        self.color = color
        self.velocity = Vector2.ZERO
        self.gravity_force = Vector2.ZERO
        body.bodies.append(self)
    
    def update_location(self, deltaTimeSeconds : float):
        self.location 
        self.velocity += self.gravity_force * self.mass * deltaTimeSeconds
        self.location += self.velocity * deltaTimeSeconds

pygame.init()
screen = pygame.display.set_mode((500, 500), pygame.RESIZABLE)

body1 = body(100, [0, 0], "yellow")
body2 = body(10, [10, 10], "red")

FPS = 60

while True:
    for i in body.bodies:
        i.gravity_force = 0
        for j in body.bodies:
            if j == i: continue
            i.gravity_force += GRAVITY * j.mass / Vector2.distance_between_squared(i.location, j.location) * Vector2.unit_vector_towards(i.location, j.location)
        i.update_location(1/FPS)
        pygame.draw.circle(screen, i.color, i.location, math.sqrt(i.mass/math.pi))
    
    pygame.display.flip()
    time.sleep(1/FPS)