import pygame
from pygame.locals import *

LARGEUR = 600
HAUTEUR = 600

pygame.init()

liste_des_elements = []

pesanteur_haut: int = 2
pesanteur_bas: int = 7

class Joueur(pygame.sprite.Sprite):
    def __init__(self):
       super().__init__() #Appel obligatoire
       self.image = pygame.image.load("assets/knight.png").convert_alpha()
       self.image = pygame.transform.scale_by(self.image, 2)
       self.rect = self.image.get_rect()
       self.rect.x = LARGEUR/2
       self.rect.y = 100 #HAUTEUR/2
       self.vitesse = 7
       self.saut = False
       self.est_dans_lair = False
       self.hauteur_saut = 10
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
    def __init__(self, x, y):
        image = "assets/blocs/herbe.png"
        super().__init__(image)
        self.rect.x = x
        self.rect.y = y

class Terre(Plateforme):
    def __init__(self, x, y):
        image = "assets/blocs/terre.png"
        super().__init__(image)
        self.rect.x = x
        self.rect.y = y

class Interrogation(Plateforme):
    def __init__(self, x, y):
        image = "assets/blocs/interrogation.png"
        super().__init__(image)
        self.rect.x = x
        self.rect.y = y


class Grille():
        def creer(self, listeDeGrille):
            pos_y = 10*32
            for ligne in listeDeGrille:
                pos_x = 0
                for element in ligne:
                    if element == 1:
                        liste_des_sprites.add(Herbe(pos_x, pos_y))
                    if element == 2:
                        liste_des_sprites.add(Terre(pos_x, pos_y))
                    if element == 3:
                        liste_des_sprites.add(Interrogation(pos_x, pos_y))
                    pos_x += 32
                pos_y += 32

grille1 = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
           [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
           [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
           [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]

fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
clock = pygame.time.Clock()
joueur = Joueur()
liste_des_sprites = pygame.sprite.LayeredUpdates()
liste_des_sprites.add(joueur)

running = True

droite_appuyé = False
gauche_appuyé = False

GrilleDeJeu = Grille()
GrilleDeJeu.creer(grille1)

while running:
   for event in pygame.event.get():
        if event.type == pygame.QUIT:
           running = False
        if event.type == KEYUP:
            if event.key == K_a:
                gauche_appuyé = False
            if event.key == K_d:
                droite_appuyé = False
        if event.type == KEYDOWN:
            if event.key == K_a:
                gauche_appuyé = True
            if event.key == K_d:
                droite_appuyé = True
            if event.key == K_SPACE and not joueur.saut and not joueur.est_dans_lair:
                joueur.saut = True
                joueur.est_dans_lair = True
                joueur.vitesse_de_saut = joueur.hauteur_saut * 2

   if gauche_appuyé:
       if joueur.rect.x > -10:
           joueur.rect.x -= joueur.vitesse
   if droite_appuyé:
       if joueur.rect.x < 570:
           joueur.rect.x += joueur.vitesse


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