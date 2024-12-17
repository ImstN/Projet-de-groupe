import pygame
from pygame.locals import *

LARGEUR = 600
HAUTEUR = 600

pygame.init()

liste_des_elements = []

pesanteur_haut: int = 2
pesanteur_bas: int = 6

class Joueur(pygame.sprite.Sprite):
    def __init__(self):
       super().__init__() #Appel obligatoire
       self.image = pygame.image.load("assets/knight.png").convert_alpha()
       self.image = pygame.transform.scale_by(self.image, 2)
       self.rect = self.image.get_rect()
       self.rect.x = LARGEUR/2
       self.rect.y = HAUTEUR/2-200
       self.vitesse = 13
       self.saut = False
       self.est_dans_lair = False
       self.hauteur_saut = 8
       self.vitesse_de_saut = 0

    def actualiser(self):
        if self.saut:
            self.rect.y -= self.vitesse_de_saut
            self.vitesse_de_saut -= pesanteur_haut
            if self.vitesse_de_saut < 0:
                self.saut = False
        else:
            self.rect.y += pesanteur_bas

class Plateforme(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale_by(self.image, 2)
        self.rect = self.image.get_rect()
        self.rect.x = LARGEUR/2
        self.rect.y = HAUTEUR/2
        self.taille = self.image.get_height()
        liste_des_elements.append(self)

class Herbe(Plateforme):
    def __init__(self):
        image = "assets/herbe.png"
        super().__init__(image)

class Background(pygame.sprite.Sprite):
    def __init__(self, location):
        image = "assets/ap.png"
        super().__init__()
        self.image = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale_by(self.image, 0.043)
        self.rect = self.image.get_rect()
        (self.rect.x, self.rect.y) = location


fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
clock = pygame.time.Clock()

liste_des_sprites = pygame.sprite.LayeredUpdates()
for i in range(7):
    background = Background([86*i, 0])
    liste_des_sprites.add(background)
joueur = Joueur()
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
            if event.key == K_SPACE and not joueur.saut and not joueur.est_dans_lair:
                joueur.saut = True
                joueur.est_dans_lair = True
                joueur.vitesse_de_saut = joueur.hauteur_saut * 2

   joueur.actualiser()

   for bloc in liste_des_elements:
       if joueur.rect.colliderect(bloc.rect):
           if joueur.vitesse_de_saut <= 0 and joueur.rect.bottom <= bloc.rect.top + 10:
               joueur.rect.bottom = bloc.rect.top
               joueur.saut = False
               joueur.est_dans_lair = False
               joueur.vitesse_de_saut = 0


   fenetre.fill((255, 255, 255))
   liste_des_sprites.draw(fenetre)
   pygame.display.flip()
   clock.tick(60)  # Limite la boucle à 60 images par seconde
pygame.quit()