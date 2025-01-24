import pygame
from pygame.locals import *
from random import randint


LARGEUR = 600
HAUTEUR = 600

pygame.init()

pesanteur_haut: int = 2
pesanteur_bas: int = 8

fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
clock = pygame.time.Clock()

# initialiser le score
score = 0
checkpoint = 50

# texte pour le score
police = pygame.font.Font('assets/fonts/PixelOperator8.ttf', 50)
texte = pygame.sprite.Sprite()
pygame.sprite.Sprite.__init__(texte)
texte.image = police.render(f"Score:{score}", True, (0, 0, 0))  # Texte noir
rect_texte = texte.image.get_rect(center=(LARGEUR / 2, HAUTEUR / 2))
texte.rect = texte.image.get_rect()
texte.rect.centerx = fenetre.get_rect().centerx
texte.rect.centery = 50

# textes pour le tuto
texte_tuto1 = pygame.sprite.Sprite()
texte_tuto2 = pygame.sprite.Sprite()
police2 = pygame.font.Font('assets/fonts/PixelOperator8.ttf', 18)
pygame.sprite.Sprite.__init__(texte_tuto1)
pygame.sprite.Sprite.__init__(texte_tuto2)
texte_tuto1.image = police2.render("Utilisez A, D et la barre d'espace", True, (255, 255, 255))
texte_tuto2.image = police2.render("pour vous déplacer", True, (255, 255, 255))
texte_tuto1.rect = texte_tuto1.image.get_rect()
texte_tuto2.rect = texte_tuto2.image.get_rect()
texte_tuto1.rect.centerx = fenetre.get_rect().centerx
texte_tuto2.rect.centerx = fenetre.get_rect().centerx
texte_tuto1.rect.bottom = fenetre.get_rect().height - 35
texte_tuto2.rect.bottom = fenetre.get_rect().height - 15


# la classe du joueur, son constructeur et ses mouvements
class Joueur(pygame.sprite.Sprite):
    def __init__(self):
       super().__init__() #Appel obligatoire
       self.image = pygame.image.load("assets/knight.png").convert_alpha()
       self.image = pygame.transform.scale_by(self.image, 2)
       self.rect = self.image.get_rect()
       self.rect.x = 175
       self.rect.y = 100 #HAUTEUR/2
       self.vitesse = 5
       self.saut = False
       self.est_dans_lair = False
       self.hauteur_saut = 10
       self.vitesse_de_saut = 0
       self.distance_parcourue = 0


    # fonction pour voir si le joueur saute
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
            GrilleDeJeu.bouger(int("-1") * self.vitesse)

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
            GrilleDeJeu.bouger(self.vitesse)

    # fonction pour remettre le joueur à son point de départ
    def reinitialiser(self):
        self.rect.x = 175
        self.rect.y = 100  # Revenir à la position de départ
        self.saut = False
        self.est_dans_lair = False
        self.vitesse_de_saut = 0
        self.distance_parcourue = 0


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

# classe de la grille et son constructeur
class Grille():
    def __init__(self):
        self.blocks = []
    def bouger(self, offset):
        for block in self.blocks:
            block.rect.x += offset
    def get_blocks(self):
        return self.blocks
    def add_to_blocks(self, object):
        self.blocks.append(object)

    # fonction pour redémarrer la grille
    def reinitialiser(self):
        self.blocks.clear()  # Vider les blocs existants
        liste_des_sprites.empty()  # Réinitialiser tous les sprites
        for i in range(7):  # Recréer l'arrière-plan
            background = Background([86 * i, 0])
            liste_des_sprites.add(background)
        liste_des_sprites.add(joueur)  # Réajouter le joueur
        liste_des_sprites.add(texte)  # Réajouter le score
        self.creer()  # Régénérer les plateformes

    def creer(self):
        lrg = 1000
        haut = 5
        listeDeGrille = [[] for _ in range(lrg)]
        for largeur in range(lrg):
            listee = [0] * haut
            for hauteur in range(haut):
                if hauteur == 0:
                    listee[hauteur] = 1
                if (listee[hauteur] == 1 and hauteur != haut - 1) or (listee[hauteur] == 2 and hauteur != haut - 1):
                    random_nombre = randint(0, 5)
                    if random_nombre != 0:
                        listee[hauteur + 1] = 2
                    else:
                        break
            listeDeGrille[largeur] = listee

        #agrandir la liste horizontale
        for liste in listeDeGrille:
            for i in range (4):
                liste.append(0)

        # création des trous et du déplacement horizontal d'éléments
        trou = 0
        for largeur in range(lrg):
            rn = randint(0, 1)
            if rn == 0 and trou < 3:
                listeDeGrille[largeur] = []
                trou += 1
            else:
                trou = 0
                rn2 = randint(0, 4)
                for i in range(rn2 - 1):
                    listeDeGrille[largeur].insert(0, 0)
                    listeDeGrille[largeur].pop()

        # créer une plattforme sur laquelle le joueur apparait
        if not listeDeGrille[5]:
            listeDeGrille[5] = [1]

        # traduction de la liste en une grille
        pos_x = 0
        for ligne in listeDeGrille:
            pos_y = 10*32
            for element in ligne:
                if element == 0:
                    pos_y += 32
                    continue
                if element == 1:
                    block = Herbe(pos_x, pos_y)
                if element == 2:
                    block = Terre(pos_x, pos_y)
                if element == 3:
                    block = Interrogation(pos_x,pos_y)
                liste_des_sprites.add(block)
                self.blocks.append(block)
                pos_y += 32
            pos_x += 32

def afficher_ecran_game_over(fenetre):
    fenetre.fill((0, 0, 255))  # Fond bleu
    police = pygame.font.Font('assets/fonts/PixelOperator8.ttf', 50)
    police2 = pygame.font.Font('assets/fonts/PixelOperator8.ttf', 20)
    texte = police.render("GAME OVER", True, (255, 255, 255))  # couleur du texte: blanc
    texte2 = police.render(f"SCORE: {score}", True, (255, 255, 255))  # couleur du texte: blanc
    texte3 = police2.render("cliquez pour rejouer", True, (255, 255, 255))
    rect_texte = texte.get_rect(center=(LARGEUR / 2, HAUTEUR / 2 - 50))
    rect_texte2 = texte.get_rect(center=(LARGEUR / 2, HAUTEUR / 2 + 50))
    rect_texte3 = texte.get_rect(center=(LARGEUR / 2, HAUTEUR / 2 + 150))
    fenetre.blit(texte, rect_texte)
    fenetre.blit(texte2, rect_texte2)
    fenetre.blit(texte3, rect_texte3)
    pygame.display.flip()
    #pygame.time.wait(3000)  # Attendre 3 secondes

def afficher_ecran_titre(fenetre):
    fenetre.fill((0, 0, 255))  # Fond bleu
    police = pygame.font.Font('assets/fonts/PixelOperator8.ttf', 30)
    texte = police.render("Cliquez pour commencer", True, (255, 255, 255))  # Texte blanc
    rect_texte = texte.get_rect(center=(LARGEUR / 2, HAUTEUR / 2))
    fenetre.blit(texte, rect_texte)
    pygame.display.flip()



# classe de l'arrière plan
class Background(pygame.sprite.Sprite):
    def __init__(self, location):
        image = "assets/ap.png"
        super().__init__()
        self.image = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale_by(self.image, 0.045)
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

running = False
ecran_titre = True
ecran_gameover = False

droite_appuye = False
gauche_appuye = False

bouger = True

# création de la grille
GrilleDeJeu = Grille()
GrilleDeJeu.creer()

liste_des_sprites.add(texte_tuto1)
liste_des_sprites.add(texte_tuto2)

GrilleDeJeu.add_to_blocks(texte_tuto1)
GrilleDeJeu.add_to_blocks(texte_tuto2)

while running or ecran_gameover or ecran_titre:
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
        if event.type == MOUSEBUTTONDOWN and ecran_titre:
            if event.button == 1:
                ecran_titre = False
                running = True
        if event.type == MOUSEBUTTONDOWN and ecran_gameover:
            if event.button == 1:
                ecran_gameover = False
                ecran_titre = True
                score = 0 #réinitialiser le score
                joueur.reinitialiser()
                GrilleDeJeu.reinitialiser()


   if gauche_appuye and bouger:
       joueur.bouger_gauche()
   if droite_appuye and bouger:
       joueur.bouger_droite()

   joueur.actualiser()

   # affichache de l'écran "game-over"
   if joueur.rect.y > HAUTEUR:
       bouger = False
       ecran_gameover = True
       running = False



   # gestion des collisions
   for bloc in GrilleDeJeu.get_blocks():
       if bloc != texte_tuto1 and bloc != texte_tuto2:
           if joueur.rect.colliderect(bloc.rect):
               if joueur.vitesse_de_saut <= 0 and joueur.rect.bottom <= bloc.rect.top + 10:
                   joueur.rect.bottom = bloc.rect.top
                   joueur.saut = False
                   joueur.est_dans_lair = False
                   joueur.vitesse_de_saut = 0

   #  calcul du score
   if joueur.distance_parcourue >= checkpoint:
      score += 1
      texte.image = police.render(f"Score:{score}", True, (0, 0, 0))
      joueur.distance_parcourue -= checkpoint #pour que le checkpoit "se déplace" vers la droite

   if ecran_titre:
       afficher_ecran_titre(fenetre)
   elif ecran_gameover:
       afficher_ecran_game_over(fenetre)
   elif running:
       fenetre.fill((255, 255, 255))
       liste_des_sprites.draw(fenetre)
   pygame.display.flip()
   clock.tick(60)  # Limite la boucle à 60 images par secondes

pygame.quit()