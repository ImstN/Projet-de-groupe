import pygame
from pygame.locals import *

LARGEUR = 600
HAUTEUR = 600

pygame.init()

liste_des_elements = []

pesanteur_haut: int = 2
pesanteur_bas: int = 8

fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
clock = pygame.time.Clock()

# initialiser le score
score = 0
checkpoint = 50

police = pygame.font.SysFont("Arial", 50)
texte = pygame.sprite.Sprite()
pygame.sprite.Sprite.__init__(texte)
texte.image = police.render(f"Score:{score}", True, (0, 0, 0))  # Texte noir
rect_texte = texte.image.get_rect(center=(LARGEUR / 2, HAUTEUR / 2))
texte.rect = texte.image.get_rect()
texte.rect.centerx = fenetre.get_rect().centerx
texte.rect.centery = 50

# la classe du joueur, son constructeur et ses mouvements
class Joueur(pygame.sprite.Sprite):
    def __init__(self):
       super().__init__() #Appel obligatoire
       self.image = pygame.image.load("assets/knight.png").convert_alpha()
       self.image = pygame.transform.scale_by(self.image, 2)
       self.rect = self.image.get_rect()
       self.rect.x = 25
       self.rect.y = 100 #HAUTEUR/2
       self.vitesse = 5
       self.saut = False
       self.est_dans_lair = False
       self.hauteur_saut = 10
       self.vitesse_de_saut = 0
       self.distance_parcourue = 0


    # fonction pour voir si le joueur saut
    def actualiser(self):
        if self.saut:
            self.rect.y -= self.vitesse_de_saut
            self.vitesse_de_saut -= pesanteur_haut
            if self.vitesse_de_saut < 0:
                self.saut = False
        else:
            self.rect.y += pesanteur_bas

    def bouger_droite(self):
        rectangle = self.rect.copy()
        rectangle.y -= 3
        rectangle.x += 3
        collision = False
        for element in GrilleDeJeu.get_blocks():
            if rectangle.colliderect(element):
                collision = True
                break

        if self.rect.x < 570 and not collision:
            self.distance_parcourue += self.vitesse
            GrilleDeJeu.bouger(-5)

    def bouger_gauche(self):
        rectangle = self.rect.copy()
        rectangle.y -= 3
        rectangle.x -= 3
        collision = False
        for element in GrilleDeJeu.get_blocks():
            if rectangle.colliderect(element):
                collision = True
                break
        if self.rect.x > -10 and not collision:
            self.distance_parcourue -= self.vitesse
            GrilleDeJeu.bouger(5)


# Classe de base pour toutes les plateformes
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

# la platforme de l'herbe
class Herbe(Plateforme):
    def __init__(self, x, y):
        image = "assets/blocs/herbe.png"
        super().__init__(image)
        self.rect.x = x
        self.rect.y = y

# la platforme de la terre
class Terre(Plateforme):
    def __init__(self, x, y):
        image = "assets/blocs/terre.png"
        super().__init__(image)
        self.rect.x = x
        self.rect.y = y

# la platforme du symbole d'interrogation
class Interrogation(Plateforme):
    def __init__(self, x, y):
        image = "assets/blocs/interrogation.png"
        super().__init__(image)
        self.rect.x = x
        self.rect.y = y

# classe du grille et son constructeur
class Grille():
    def __init__(self):
        self.blocks = []
    def bouger(self, offset):
        for block in self.blocks:
            block.rect.x += offset
    def get_blocks(self):
        return self.blocks
    def creer(self, listeDeGrille):
        pos_y = 10*32
        for ligne in listeDeGrille:
            pos_x = 0
            for element in ligne:
                if element == 0:
                    pos_x += 32
                    continue
                if element == 1:
                    block = Herbe(pos_x, pos_y)
                if element == 2:
                    block = Terre(pos_x, pos_y)
                if element == 3:
                    block = Interrogation(pos_x,pos_y)
                liste_des_sprites.add(block)
                self.blocks.append(block)
                pos_x += 32
            pos_y += 32

def afficher_ecran_game_over(fenetre):
    fenetre.fill((0, 0, 255))  # Fond bleu
    police = pygame.font.SysFont("Arial", 50)
    texte = police.render("GAME OVER", True, (255, 255, 255))  # couleur du texte: blanc
    texte2 = police.render(f"SCORE: {score}", True, (255, 255, 255))  # couleur du texte: blanc
    rect_texte = texte.get_rect(center=(LARGEUR / 2, HAUTEUR / 2 - 50))
    rect_texte2 = texte.get_rect(center=(LARGEUR / 2, HAUTEUR / 2 + 50))
    fenetre.blit(texte, rect_texte)
    fenetre.blit(texte2, rect_texte2)
    pygame.display.flip()
    pygame.time.wait(3000)  # Attendre 2 secondes

def afficher_ecran_titre(fenetre):
    fenetre.fill((0, 0, 255))  # Fond bleu
    police = pygame.font.SysFont("Arial", 30)
    texte = police.render("Cliquez pour commencer", True, (255, 255, 255))  # Texte blanc
    rect_texte = texte.get_rect(center=(LARGEUR / 2, HAUTEUR / 2))
    fenetre.blit(texte, rect_texte)
    pygame.display.flip()


# le grille
grille1 = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,0,0,0],
           [0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0],
           [0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0],
           [1,1,1,1,0,0,1,1,0,1,1,1,0,0,0,0,0,0],
           [2,2,2,2,0,0,0,2,0,2,2,2,1,0,0,0,0,0],
           [2,2,2,0,0,0,0,0,0,2,2,2,2,2,2,2,0,1],
           [0,0,0,0,0,0,0,0,0,0,0,2,2,2,2,2,0,2],
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]

# classe de l'arrière plan
class Background(pygame.sprite.Sprite):
    def __init__(self, location):
        image = "assets/ap.png"
        super().__init__()
        self.image = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale_by(self.image, 0.043)
        self.rect = self.image.get_rect()
        (self.rect.x, self.rect.y) = location




# liste des sprites et l'ajoute de toutes les plateformes
liste_des_sprites = pygame.sprite.LayeredUpdates()
for i in range(7):
    background = Background([86*i, 0])
    liste_des_sprites.add(background)

# initialisation du joueur
joueur = Joueur()
liste_des_sprites.add(joueur)
liste_des_sprites.add(texte)



running = True

droite_appuye = False
gauche_appuye = False

GrilleDeJeu = Grille()
GrilleDeJeu.creer(grille1)


while running:
    # mouvement à gauche et droite et le saut
   for event in pygame.event.get():
        if event.type == pygame.QUIT:
           running = False
        if event.type == KEYUP:
            if event.key == K_a:
                gauche_appuye = False
            if event.key == K_d:
                droite_appuye = False
        if event.type == KEYDOWN:
            if event.key == K_a:

                gauche_appuye = True
            if event.key == K_d:
                droite_appuye = True
            if event.key == K_SPACE and not joueur.saut and not joueur.est_dans_lair:
                joueur.saut = True
                joueur.est_dans_lair = True
                joueur.vitesse_de_saut = joueur.hauteur_saut * 2

   if gauche_appuye:

       joueur.bouger_gauche()
   if droite_appuye:
       joueur.bouger_droite()


   joueur.actualiser()

   # affichache de l'écran "game-over"
   if joueur.rect.y > HAUTEUR:
       afficher_ecran_game_over(fenetre)
       running = False

   # gestion des collisions
   for bloc in liste_des_elements:
       if joueur.rect.colliderect(bloc.rect):
           if joueur.vitesse_de_saut <= 0 and joueur.rect.bottom <= bloc.rect.top + 10:
               joueur.rect.bottom = bloc.rect.top
               joueur.saut = False
               joueur.est_dans_lair = False
               joueur.vitesse_de_saut = 0


   if joueur.distance_parcourue >= checkpoint:
      score += 1
      texte.image = police.render(f"Score:{score}", True, (0, 0, 0))
      joueur.distance_parcourue -= checkpoint



   fenetre.fill((255, 255, 255))
   liste_des_sprites.draw(fenetre)
   pygame.display.flip()
   clock.tick(60)  # Limite la boucle à 60 images par seconde

pygame.quit()