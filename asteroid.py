from typing import Any
import pygame
import sys
from random import randint
import random
import math
from pygame.locals import *

#Initialisation de Pygame
pygame.init()

#Paramètres du jeu
WIDTH, HEIGHT = 800, 600
FPS = 60

#Couleurs
WHITE = (255, 255, 255)
RED = (255, 0, 0)

#Initialisation de la fenêtre
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Asteroids Game")
clock = pygame.time.Clock()

#Classes
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.speed = 5
        self.shoot_delay = 250  #Delay entre les tirs en millisecondes
        self.last_shot = pygame.time.get_ticks()
    

    def shoot(self):
            now = pygame.time.get_ticks()
            if now - self.last_shot <= self.shoot_delay:
                return
            
            position_souris = pygame.mouse.get_pos()
            self.last_shot = now
            
            #vitesse bullets
            speed_max = 10
            vitesse_x = position_souris[0] - self.rect.centerx
            vitesse_y = position_souris[1] - self.rect.centery
            magnitude = math.sqrt(vitesse_x**2 + vitesse_y**2)

            if magnitude > speed_max:
                new_vector = ((vitesse_x/magnitude)*speed_max, (vitesse_y/magnitude)*speed_max)

            bullets.add(Bullet(self.rect.centerx, self.rect.centery, new_vector[0], new_vector[1]))

    def update(self):
        keys = pygame.key.get_pressed()
        mouse_btns = pygame.mouse.get_pressed()

        #Initialiser les changements de position pour les déplacements en diagonale
        dx = 0
        dy = 0

        if keys[K_LEFT]:
            dx -= 1
        if keys[K_RIGHT]:
            dx += 1
        if keys[K_UP]:
            dy -= 1
        if keys[K_DOWN]:
            dy += 1

        #Normaliser le vecteur de déplacement pour maintenir une vitesse constante en diagonale
        if dx != 0 and dy != 0:
            dx /= math.sqrt(2)
            dy /= math.sqrt(2)

        #Appliquer les changements de position au joueur
        self.rect.x += int(dx * self.speed)
        self.rect.y += int(dy * self.speed)

        if mouse_btns[0]:
            self.shoot()
        
        #Assurez-vous que le joueur reste dans l'écran
        self.rect.x = max(0, min(self.rect.x, WIDTH - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, HEIGHT - self.rect.height))


class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        taille=randint(15,40)
        self.image = pygame.Surface((taille, taille))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.vitesse_max = 5
        self.vitesse_min = 2
        self.vitesse_var_max = 2
        self.vitesse_var_min = -2


        #Choix aléatoire du côté d'où l'astéroïde va apparaître
        side = random.choice(["left", "right", "top", "bottom"])
        if side == "left":
            self.rect.x = 0
            self.rect.y = random.randrange(HEIGHT - self.rect.height)
            self.speed_x = random.randint(self.vitesse_min, self.vitesse_max)
            self.speed_y = random.randint(self.vitesse_var_min,  self.vitesse_var_max)
        elif side == "right":
            self.rect.x = WIDTH - self.rect.width
            self.rect.y = random.randrange(HEIGHT - self.rect.height)
            self.speed_x = -random.randint(self.vitesse_min, self.vitesse_max)
            self.speed_y = random.randint(self.vitesse_var_min,  self.vitesse_var_max)
        elif side == "top":
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = 0
            self.speed_x = random.randint(self.vitesse_var_min,  self.vitesse_var_max)
            self.speed_y = random.randint(self.vitesse_min, self.vitesse_max)                            
        elif side == "bottom":
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = HEIGHT - self.rect.height
            self.speed_x = random.randint(self.vitesse_var_min,  self.vitesse_var_max)
            self.speed_y = -random.randint(self.vitesse_min, self.vitesse_max)

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.y > HEIGHT or self.rect.x < 0 or self.rect.x > WIDTH:
            self.kill()

    def destroy(self):
        self.image.fill(RED)


class Bullet(pygame.sprite.Sprite): 
    def __init__(self, x, y, dx, dy):
        super().__init__()
        self.image = pygame.Surface((5, 5))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.dx = dx
        self.dy = dy

    def update(self, asteroids_list):
        self.rect.x += self.dx
        self.rect.y += self.dy
        pygame.draw.circle(screen, RED, (self.rect.x, self.rect.y), 5)
        
        if self.rect.x <= 0 or self.rect.x >= WIDTH or self.rect.y <= 0 or self.rect.y >= HEIGHT:
            self.kill()
        
        hits = pygame.sprite.spritecollide(self, asteroids_list, True)
        for asteroid_hit in hits:
            asteroid_hit.destroy()

    def destroy(self):
        self.kill()

         

#Groupes de sprites
all_sprites = pygame.sprite.Group()
asteroids = pygame.sprite.Group()

bullets = pygame.sprite.Group()

#Création du joueur
player = Player()
all_sprites.add(player)

#Création des astéroïdes
asteroid_spawn_time = 100  #Temps initial entre les apparitions d'astéroïdes en millisecondes
asteroid_last_spawn = pygame.time.get_ticks()

#Boucle principale
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    #Mise à jour des sprites
    all_sprites.update()


    #Gestion des collisions entre le joueur et les astéroïdes
    hits = pygame.sprite.spritecollide(player, asteroids, False)
    if hits:
        print("Game Over!")
        running = False

    #Génération d'astéroïdes de plus en plus fréquemment
    now = pygame.time.get_ticks()
    if now - asteroid_last_spawn > asteroid_spawn_time:
        asteroid = Asteroid()
        all_sprites.add(asteroid)
        asteroids.add(asteroid)
        asteroid_last_spawn = now
        #Réduire le temps entre les apparitions d'astéroïdes pour les prochaines générations
        asteroid_spawn_time = max(300, asteroid_spawn_time - 5)

    #Dessin sur l'écran
    screen.fill((0, 0, 0))

    
    for bullet in bullets:
        bullet.update(asteroids)
        hits = pygame.sprite.spritecollide(bullet, asteroids, True)
        if len(hits) > 0:
            print(hits)

    all_sprites.draw(screen)
    

    #Rafraîchissement de l'écran
    pygame.display.flip()

    #Contrôle de la fréquence d'images
    clock.tick(FPS)

#Quitter Pygame
pygame.quit()
sys.exit()
