import pygame
import math
from utils import scale_image, blit_rotate_center
import os

TRACK = pygame.image.load(os.path.join("imgs","track3.png"))
WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("NEAT")

#Track1 pos = 490, 820
#Track 2 pos = 450, 580
#Track 3 pos =  450, 670
class NEATCar(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.IMG = scale_image(pygame.image.load(os.path.join("imgs","purple-car.png")),5)
        self.image = self.IMG
        self.rect = self.image.get_rect(center=(450, 670))
        self.vel = pygame.math.Vector2(0.7, 0)
        self.angle = 0
        self.rotation_vel = 5
        self.direction = 0
        self.alive = True
        self.radars = []


    def update(self):
        self.radars.clear()
        self.step()
        self.rotate()
        
        for radar_angle in (-60, -30, 0, 30, 60):
           self.radar(radar_angle)
        self.collision()
        self.data()

    def step(self):
        self.rect.center += self.vel * 5
    
    def collision(self):
        length = 30
        rightCollision = [int(self.rect.center[0] + math.cos(math.radians(self.angle + 18)) * length),
                                 int(self.rect.center[1] - math.sin(math.radians(self.angle + 18)) * length)]
        leftCollision = [int(self.rect.center[0] + math.cos(math.radians(self.angle - 18)) * length),
                                int(self.rect.center[1] - math.sin(math.radians(self.angle - 18)) * length)]

        # Die on Collision
        if WINDOW.get_at(rightCollision) == pygame.Color(2, 105, 31, 255) \
                or WINDOW.get_at(leftCollision) == pygame.Color(2, 105, 31, 255):
            self.alive = False

        # Draw Collision Points
        pygame.draw.circle(WINDOW, (0, 255, 255, 0), rightCollision, 4)
        pygame.draw.circle(WINDOW, (0, 255, 255, 0), leftCollision, 4)


    def rotate(self):
        if self.direction == 1:
            self.angle -= self.rotation_vel
            self.vel.rotate_ip(self.rotation_vel)
        if self.direction == -1:
            self.angle += self.rotation_vel
            self.vel.rotate_ip(-self.rotation_vel)

        self.image = pygame.transform.rotozoom(self.IMG, self.angle, 0.1)
        self.rect = self.image.get_rect(center=self.rect.center)

    def radar(self,radar_angle):
        length = 0
        x = int(self.rect.center[0])
        y = int(self.rect.center[1])

        while not WINDOW.get_at((x, y)) == pygame.Color(2, 105, 31, 255) and length < 100:
            length += 1
            x = int(self.rect.center[0] + math.cos(math.radians(self.angle + radar_angle)) * length)
            y = int(self.rect.center[1] - math.sin(math.radians(self.angle + radar_angle)) * length)

        # Draw Radar
        pygame.draw.line(WINDOW, (255, 255, 255, 255), self.rect.center, (x, y), 1)
        pygame.draw.circle(WINDOW, (0, 255, 0, 0), (x, y), 3)

        dist = int(math.sqrt(math.pow(self.rect.center[0] - x, 2)
                             + math.pow(self.rect.center[1] - y, 2)))

        self.radars.append([radar_angle, dist])

    def data(self):
        input = [0,0,0,0,0] 
        for x , radar in enumerate(self.radars):
            input[x] = int(radar[1])
        return input

  



    