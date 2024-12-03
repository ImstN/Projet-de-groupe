import pygame
from pygame.locals import *

LARGEUR = 600
HAUTEUR = 600

pygame.init()

class Joueur(pygame.sprite.Sprite):
    def __init__(self):
       super().__init__() #Appel obligatoire
       self.image = pygame.image.load("assets/mario.png").convert_alpha()
       self.rect = self.image.get_rect()
       self.rect.x = LARGEUR/2
       self.rect.y = HAUTEUR/2
       self.vitesse = 13

       self.saut = False
       self.hauteur_saut = 30
       self.vitesse_de_saut = self.hauteur_saut
       self.pesanteur = 5



fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
clock = pygame.time.Clock()
joueur = Joueur()
liste_des_sprites = pygame.sprite.LayeredUpdates()
liste_des_sprites.add(joueur)
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
            if event.key == K_SPACE:
                joueur.saut = True
   if joueur.saut:
       joueur.rect.y -= joueur.vitesse_de_saut
       joueur.vitesse_de_saut -= joueur.pesanteur

       if joueur.vitesse_de_saut < - joueur.hauteur_saut:
           joueur.saut = False
           joueur.vitesse_de_saut = joueur.hauteur_saut

   fenetre.fill((255, 255, 255))
   liste_des_sprites.draw(fenetre)
   pygame.display.flip()
   clock.tick(60)  # Limite la boucle à 60 images par seconde
pygame.quit()