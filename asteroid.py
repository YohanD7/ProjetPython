import pygame, sys
import time
from pygame.locals import *
from random import randint
from pygame.math import Vector2
from utils import load_sprite
from models import GameObject


LARGEUR = 640
HAUTEUR = 480
RAYON = 20
NB_BALLES = 10

pygame.display.init()
fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
fenetre.fill([0, 0, 0])


class Spaceship(GameObject):
    def __init__(self, position):
        super().__init__(position, load_sprite("spaceship"), Vector2(0))

class Balle:
    def __init__(self):
        self.x = randint(0, LARGEUR)
        self.y = randint(0, HAUTEUR)
        self.dx = randint(2, 5)
        self.dy = randint(2, 5)
        self.couleur = (randint(0, 255), randint(0, 255), randint(0, 255))
        self.taille = RAYON
    #création de la balle
    def dessine(self):
        pygame.draw.circle(fenetre, self.couleur, (self.x, self.y), self.taille)

    def bouge(self):
        #déplacement au spawn :
        self.x += self.dx
        self.y += self.dy
        #rebondissemeents mur :
        if self.y < self.taille or self.y > HAUTEUR - self.taille:
            self.dy = -self.dy
        if self.x < self.taille or self.x > LARGEUR - self.taille:
            self.dx = -self.dx
        #rebondissemeents balles : 
        for balle in mon_sac_a_balles:
            if (
                (self.x - balle.x) ** 2 + (self.y - balle.y) ** 2
            ) ** 0.5 < self.taille + balle.taille:
                self.dx, balle.dx = balle.dx, self.dx
                self.dy, balle.dy = balle.dy, self.dy

#Balles, propriétés
mon_sac_a_balles = []
for _ in range(NB_BALLES):
    new_ball = Balle()
    mon_sac_a_balles.append(new_ball)



#NE PAS TOUCHER
while True:
    fenetre.fill([0, 0, 0])

    for balle in mon_sac_a_balles:
        balle.dessine()
        balle.bouge()

    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            sys.exit()

    time.sleep(0.05)


