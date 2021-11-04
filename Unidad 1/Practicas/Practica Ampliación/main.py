# Import the pygame module
import contextvars
import random
import sqlite3
import os
import time
import pygame
from pygame import RLEACCEL
from pygame.locals import *

directorio = os.path.dirname(__file__)
recursos = os.path.join(directorio, 'resources')

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT
)

# Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
BLACK = (0,0,0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 12)
BLUE = (135, 206, 255)

#Puntuacion
puntuacion = 0

#Nivel
nivel = 1

# Define a Player object by extending pygame.sprite.Sprite
# The surface drawn on the screen is now an attribute of 'player'
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load(os.path.join(recursos, "jet.png")).convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()
        # Disparos
        self.cadencia = 750
        self.ultimo_disparo = pygame.time.get_ticks()


    # Move the sprite based on user keypresses
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
            move_up_sound.play()
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
            move_down_sound.play()
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)
        if pressed_keys[K_SPACE]:
            ahora = pygame.time.get_ticks()
            if ahora - self.ultimo_disparo > self.cadencia:
                self.disparo()
                self.ultimo_disparo= ahora

        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

    def disparo(self):
        bala = Disparos(self.rect.centerx, self.rect.centery)
        balas.add(bala)

# Define a Player object by extending pygame.sprite.Sprite
# The surface drawn on the screen is now an attribute of 'disparos'
class Disparos (pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("Resources/bala.png").convert(), (20, 20))
        self.image.set_colorkey((0,0,0), RLEACCEL)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
    def update(self):
        self.rect.x +=25
        if self.rect.bottom < 0:
            self.kill()

# Define the enemy object by extending pygame.sprite.Sprite
# The surface you draw on the screen is now an attribute of 'enemy'
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load(os.path.join(recursos, "missile.png")).convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(5+2*nivel,10+3*nivel)

    # Move the sprite based on speed
    # Remove the sprite when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

# Define the cloud object by extending pygame.sprite.Sprite
# The surface you draw on the screen is now an attribute of 'cloud'
class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pygame.image.load(os.path.join(recursos, "cloud.png")).convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(
            center = (
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )

    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()

def draw_text(text, font, surface, x, y, main_color, background_color=None):
    textobj = font.render(text, True, main_color, background_color)
    textrect = textobj.get_rect()
    textrect.centerx = x
    textrect.centery = y
    surface.blit(textobj, textrect)

def connexio():
    try:
        connexio = sqlite3.connect("bd.bd")
        crear_db(connexio)
        return connexio
    except sqlite3.OperationalError:
        print("ERROR")

def crear_db(con):

    cursor = con.cursor()
    try:
        cursor.execute("CREATE TABLE IF NOT EXISTS Puntuacion(max INT)")
        cursor.execute("INSERT INTO Puntuacion VALUES (0)")
        print("La tabla puntuacion se ha creado");
    except sqlite3.OperationalError:
        print("Ya existe")

con = connexio()

def update(puntuacion):
    cursor = con.cursor()
    cursor.execute("UPDATE Puntuacion SET max={}".format(puntuacion))
    con.commit()

def read():
    cursor = con.cursor()
    var_cursor = cursor.execute("SELECT max FROM Puntuacion").fetchone()
    return var_cursor[0]

# Setup for sounds. Defaults are goos.
pygame.mixer.init()

# Initialize pygame
pygame.init()

# Load and play background music
pygame.mixer.music.load(os.path.join(recursos, "Apoxode_-_Electric_1.ogg"))
pygame.mixer.music.play(loops=-1)

# Load all sound files
# Sound sources: Jon Fincher
move_up_sound = pygame.mixer.Sound(os.path.join(recursos,"Rising_putter.ogg"))
move_down_sound = pygame.mixer.Sound(os.path.join(recursos,"Falling_putter.ogg"))
collision_sound = pygame.mixer.Sound(os.path.join(recursos,"Collision.ogg"))


# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Window titlebar
pygame.display.set_caption('BIENVENIDO AL JUEGO DEL AVION')
pygame.display.set_icon(pygame.image.load(os.path.join(recursos, "jet.png")).convert())

default_font = pygame.font.Font(None, 28)

# Create a custom event for adding a new enemy
ADDENEMY = pygame.USEREVENT + 1

# Create a custom event for adding a new cloud
ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 1000)

# Create a custom event for change weather
CHANGEW = pygame.USEREVENT + 3
pygame.time.set_timer(CHANGEW, 10000)

# Instantiate player. Right now, this is just a rectangle.
player = Player()

# Create groups to hold enemy
# Create group to hold cloud
enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
balas = pygame.sprite.Group()

#tipo letra
letra18 = pygame.font.SysFont("Arial", 18, True)
letra50 = pygame.font.SysFont("segoe print", 50, GREEN)

#Change weather
tiempo = True
c_t = BLUE

# - enemies is used for collision detection and position updates
# - all_sprites is used for rendering
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Setup the clock for a decent framerate
clock = pygame.time.Clock()

seguir = True

#First Screen
while seguir:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

    screen.fill((0 ,0 ,0))
    bienvenido = letra50.render("BIENVENIDO",1 ,(0,255,0));
    recors_actual = letra18.render("Record Actual: "+str(read()),1,(0,255,0));
    start = letra18.render("Para continuar,tienes que pulsar la letra P", 1, (0,255,0));

    screen.blit(recors_actual,(300,350))
    screen.blit(bienvenido, (200, 200))
    screen.blit(start, (250, 500))

    tecla = pygame.key.get_pressed()

    if tecla[pygame.K_p]:
        seguir = False

    pygame.display.update()

#pujar cohetes
cambio = 0

running = True
# Main loop
while running:
    #Cambiar la salida de los enemigos cuando subimos de nivel
    formula = int(50+200/nivel)
    if cambio != formula:
        cambio = formula
        pygame.time.set_timer(ADDENEMY, formula)

    # Look at every event in the queue
    for event in pygame.event.get():
        # Did the user hit a key?
        if event.type == KEYDOWN:
            # Was it the Escape key? If so, stop the loop.
            if event.key == K_ESCAPE:
                running = False
            # Did the user click the window close button? If so, stop the loop
        elif event.type == QUIT:
            running = False

        # Add a new enemy?
        elif event.type == ADDENEMY:
            # Create the new enemy and add it to sprite groups
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

        # Add a new cloud?
        elif event.type == ADDCLOUD:
            # Create the new enemy and add it to sprite groups
            new_cloud = Cloud()
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)

        # Cambiar tiempo
        elif event.type == CHANGEW:
            if tiempo == True:
                c_t = (BLUE)
                tiempo = False
            else:
                c_t = (BLACK)
                tiempo = True

    # Get all the keys currently pressed
    pressed_keys = pygame.key.get_pressed()

    # Update the player sprite based on user keypresses
    player.update(pressed_keys)

    # Update enemy position
    enemies.update()

    #Update cloud position
    clouds.update()

    balas.update()

    #Creamos  la colision entre cohete y bala
    colision = pygame.sprite.groupcollide(enemies, balas,True, True)

    if colision:
        puntuacion += 10

    # Fill the screen with blue
    screen.fill((c_t))

    # Draw all sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    # Check if any enemies have collided with the player
    if pygame.sprite.spritecollideany(player, enemies):
        # If so, then remove the player and stop the loop
        player.kill()
        #Sound of collision
        collision_sound.play()
        time.sleep(1)
        running = False

        #Guardamos la puntuacion maxima
        puntuacion_max = read()

        #Pantalla final
        seguir = True
        while seguir:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

            #Guardar nuevo record
            if puntuacion > read():
                update(puntuacion)

            #Comprobar si hay nuevo record
            if puntuacion_max < puntuacion:
                enhorabuena = letra18.render("Enhorabuena, Nuevo Record: " + str(read()), 1, (0, 0, 225))
                screen.blit(enhorabuena, (450, 400))
            else:
                record = letra18.render("Record: " + str(read()), 1, (0, 0, 255))
                screen.blit(record, (450, 400))

            game_over = letra50.render("GAME OVER", 1, (0, 0, 255))
            salir = letra18.render("Para salir pulse 'Espacio'", 1, (0, 0, 255))
            mostrar_p = letra18.render("Puntuacion: " +str(puntuacion),1, (0, 0, 255))

            screen.blit(game_over,(200, 200))
            screen.blit(salir, (250, 500))
            screen.blit(mostrar_p, (150, 400))

            tecla = pygame.key.get_pressed()

            if tecla[pygame.K_SPACE]:
                seguir = False

            pygame.display.update()

    for i in enemies:
        if i.rect.right < 10:
            puntuacion+=10
            if puntuacion%500 == 0:
                nivel += 1

    # Flip everything to the display
    pygame.display.flip()

    # Draw the player on the screen
    # screen.blit(player.surf, (SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
    screen.blit(player.surf, player.rect)

    balas.draw(screen)

    imagenPuntos = letra18.render('Puntos '+str(puntuacion), True, (0,0,255))
    rectanguloPuntos = imagenPuntos.get_rect()
    rectanguloPuntos.left = 10
    rectanguloPuntos.top = 10
    screen.blit(imagenPuntos, rectanguloPuntos)

    imagenNivel = letra18.render('Nivel '+str(nivel), True, (0, 0, 255))
    rectanguloNivel = imagenNivel.get_rect()
    rectanguloNivel.left = 10
    rectanguloNivel.top = 40
    screen.blit(imagenNivel, rectanguloNivel)

    # Update the display
    pygame.display.flip()

    # Ensure program maintains a rate of 30 frames per second
    clock.tick(30)

# All done! Stop and quit the mixer.
pygame.mixer.music.stop()
pygame.mixer.quit()
