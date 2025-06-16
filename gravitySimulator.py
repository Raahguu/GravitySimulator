import pygame
from pVectors import Vector2
import math
import time

GRAVITY = 1000
ZOOM_OUT = 0.5

class body:
    bodies : list["body"] = []
    def __init__(self, mass : int, location : list[int, int], color : str):
        self.mass = mass
        self.location = Vector2(location)
        self.color = color
        self.velocity = Vector2.ZERO
        self.acceleration = Vector2.ZERO
        body.bodies.append(self)
    
    def update_location(self, deltaTimeSeconds : float):
        self.velocity += self.acceleration * deltaTimeSeconds
        self.location += self.velocity * deltaTimeSeconds

pygame.init()
screen = pygame.display.set_mode((500, 500), pygame.RESIZABLE)

earth = body(100, [0, 0], "blue")
moon = body(10, [100, 100], "grey")

FPS = 200

def main(FPS : int, screen : pygame.Surface):
    while True:
        screen.fill("black")
        for i in body.bodies:
            i.acceleration = 0
            for j in body.bodies:
                if j == i: continue
                dist_squared = Vector2.distance_between_squared(i.location, j.location)
                if dist_squared <= (math.sqrt(i.mass/math.pi) + math.sqrt(j.mass/math.pi)) / ZOOM_OUT: i.velocity = -i.velocity
                else: i.acceleration += GRAVITY * i.mass * j.mass / dist_squared * Vector2.unit_vector_towards(i.location, j.location)
            i.update_location(1/FPS)
            pygame.draw.circle(screen, i.color, list((i.location + Vector2(screen.get_width() // 2, screen.get_height() // 2))), math.sqrt(i.mass/math.pi) / ZOOM_OUT)
        
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        time.sleep(1/FPS)

if "__main__" == __name__:
    main(FPS, screen)

