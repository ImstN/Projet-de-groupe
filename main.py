import pygame
from pygame.locals import *

pygame.init()

class Joueur(pygame.sprite.Sprite):
    def __init__(self):
       super().__init__() #Appel obligatoire
       self.image = pygame.image.load("assets/knight.png").convert_alpha()
       self.image = pygame.transform.scale_by(self.image, 2)
       self.rect = self.image.get_rect()
       self.rect.x = LARGEUR/2
       self.rect.y = HAUTEUR/2
       self.vitesse = 13

class Plateforme(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale_by(self.image, 2)
        self.rect = self.image.get_rect()
        self.rect.x = LARGEUR/2
        self.rect.y = HAUTEUR/2

class Herbe(Plateforme):
    def __init__(self):
        image = "assets/herbe.png"
        super().__init__(image)




LARGEUR = 600
HAUTEUR = 600
fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
clock = pygame.time.Clock()
joueur = Joueur()
liste_des_sprites = pygame.sprite.LayeredUpdates()
liste_des_sprites.add(joueur)
herbe = Herbe()
liste_des_sprites.add(herbe)
running = True
pygame.key.set_repeat(40, 30)


while running:
   for event in pygame.event.get():
        if event.type == pygame.QUIT:
           running = False
        if event.type == KEYDOWN:

            if event.key == K_a:
                if joueur.rect.x > -10:
                    joueur.rect.x -= joueur.vitesse
            if event.key == K_d:
                if joueur.rect.x < 570:
                    joueur.rect.x += joueur.vitesse
            if event.key == K_w:
                if joueur.rect.y > -10:
                    joueur.rect.y -= joueur.vitesse
            if event.key == K_s:
                if joueur.rect.y < 570:
                    joueur.rect.y += joueur.vitesse

   fenetre.fill((255, 255, 255))
   liste_des_sprites.draw(fenetre)
   pygame.display.flip()
   clock.tick(60)  # Limite la boucle à 60 images par seconde
pygame.quit()