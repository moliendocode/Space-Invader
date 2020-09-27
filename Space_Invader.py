import random
import math
import pygame
from pygame import mixer


pygame.init()

# Creacion de la ventana
screen = pygame.display.set_mode((800,600))

# fondo
background = pygame.image.load('2362730.png')
mixer.music.load('fondo.wav')
mixer.music.play(-1)

# Titulo y icono
pygame.display.set_caption("Space Invaders")
icono = pygame.image.load('spaceinvaders.png')
pygame.display.set_icon(icono)

# Player    
playerImg = pygame.image.load('nae.png')
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0

# Enemigo
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemigo.png'))
    enemyX.append(random.randint(0,735))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(2)
    enemyY_change.append(40)

# Balas
# ready: no se ve la bala
# fire: la bala esta en movimiento
bulletImg = pygame.image.load('bala.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf',32)

textX = 10
textY = 10

# Game over text
over_font = pygame.font.Font('freesansbold.ttf',64)


def show_score(x,y):
    score = font.render("Puntaje: " + str(score_value), True, (255,255,255))
    screen.blit(score, (x,y))

def game_over_text():
    over_text = over_font.render("PERDISTE WEY", True, (255,255,255))
    screen.blit(over_text, (150,250))

def player(x,y):
    screen.blit(playerImg, (x,y))

def enemy(x,y,i):
    screen.blit(enemyImg[i], (x,y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x+16,y+10))

def isCollision(enemyX,enemyY,bulletX,bulletY):
    distance = math.sqrt((math.pow(enemyX-bulletX,2) + math.pow(enemyY-bulletY,2)))
    if distance < 27:
        return True
    else:
        return False

# Game Loop
running = True
while running:

    # Color de fondo
    screen.fill((128,128,128))
    # imagen fondo
    screen.blit(background, (0,0))


    for event in pygame.event.get():
        # Exit con la X
        if event.type == pygame.QUIT:
            running = False

        # Checkea si se apretan teclas
        if event.type == pygame.KEYDOWN:
            # Flechas
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound('disparo.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX,bulletY)

        # Checkea si se sueltan teclas
        if event.type == pygame.KEYUP:
            # Flechas
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0


        
    # Nae

    # Movimiento 
    playerX += playerX_change
    # Que no salga de la pantalla
    if playerX <=0:
        playerX = 0
    elif playerX >=736:
        playerX = 736

    for i in range(num_of_enemies):

        # Game over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        #
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <=0:
            enemyX_change[i] = 2
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >=736:
            enemyX_change[i] = -2
            enemyY[i] += enemyY_change[i]

        collision = isCollision(enemyX[i],enemyY[i],bulletX,bulletY)
        if collision:
            explosion_sound = mixer.Sound('colision.wav')
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0,735)
            enemyY[i] = random.randint(50,150)
        
        enemy(enemyX[i],enemyY[i], i)

    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX,bulletY)
        bulletY -= bulletY_change



    player(playerX,playerY)
    show_score(textX,textY)
    # Refresh
    pygame.display.update()