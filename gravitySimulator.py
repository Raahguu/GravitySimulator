import pygame
from pVectors import Vector2
import math
import time

GRAVITY = 1
ZOOM_OUT = 3

class body:
    bodies : list["body"] = []
    def __init__(self, mass : int, location : list[int, int], color : str):
        self.mass = mass
        self.location = Vector2(location)
        self.color = color
        self.velocity = Vector2.ZERO
        self.acceleration = Vector2.ZERO
        body.bodies.append(self)
    
    def update_location(self, FPS):
        self.velocity += self.acceleration * 1/FPS
        self.location += self.velocity * 1/FPS
    
    @property
    def radius(self):
        global ZOOM_OUT
        return math.sqrt(self.mass/math.pi) / ZOOM_OUT * 2

pygame.init()
screen = pygame.display.set_mode((500, 500), pygame.RESIZABLE)
screen_center = (screen.get_width() // 2, screen.get_height() // 2)

def spot_around_circle(radius : int, amount : int, index : int, center = [0, 0]):
    angle = index * 360 / amount
    location = [math.cos(angle) * radius + center[0], math.sin(angle) * radius + center[1]]
    return location

#Create a bunch of bodies
bodies_colors = ["blue", "red", "yellow", "green", "purple", "brown", "grey"]
for i, color in enumerate(bodies_colors):
    ball = body(50, spot_around_circle(100, len(bodies_colors), i, center=[0, 0]), color)

def wait_for_space():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return

def main(FPS : float, screen : pygame.Surface):
    global screen_center, ZOOM_OUT
    #initial drawing of bodies to the screen
    for b in body.bodies:
        pygame.draw.circle(screen, b.color, list((b.location / ZOOM_OUT + Vector2(screen_center))), b.radius)
    pygame.display.flip()
    wait_for_space()
    #gravity simulation
    while True:
        screen_center = (screen.get_width() // 2, screen.get_height() // 2)
        for i in body.bodies:
            i.acceleration = 0
            for j in body.bodies:
                if j == i: continue
                dist = Vector2.distance_between(i.location, j.location)
                if dist <= i.radius + j.radius: break
                else: i.acceleration += GRAVITY * i.mass * j.mass / dist * Vector2.unit_vector_towards(i.location, j.location)
            i.update_location(FPS)
            pygame.draw.circle(screen, i.color, list((i.location / ZOOM_OUT + Vector2(screen_center))), i.radius)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        time.sleep(1/FPS)

if "__main__" == __name__:
    main(30, screen)

