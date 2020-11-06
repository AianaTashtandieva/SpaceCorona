import pygame
from pygame import mixer
import random
import math

# initialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# background
background = icon = pygame.image.load('background.png')

# background song
mixer.music.load("backgroundsong.wav")
mixer.music.play(-1)


# title and icon
pygame.display.set_caption("COVID-19")
icon = pygame.image.load('corona.png')
pygame.display.set_icon(icon)

# player
playerImg = pygame.image.load('protective-wearr.png')
playerX = 370
playerY = 480
playerX_change = 0

# virus
virusImg = []
virusX = []
virusY = []
virusX_change = []
virusY_change = []
num_of_virus = 5

for i in range(num_of_virus):
    virusImg.append(pygame.image.load('virus.png'))
    virusX.append(random.randint(0, 800))
    virusY.append(random.randint(50, 150))
    virusX_change.append(4)
    virusY_change.append(40)


# bullet

# ready - you cant see the bullet on screen
# fire - the bullet is currently moving

bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# font

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

# game over text
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))


def virus(x, y):
    screen.blit(virusImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 50, y + 10))


def iscollision(virusx, virusy, bulletx, bullety):
    distance1 = math.sqrt(math.pow(virusx-bulletx, 2))
    distance2 = + (math.pow(virusy-bullety, 2))
    distance = distance1 + distance2
    if distance < 27:
        return True
    else:
        return False


# game loop
running = True
while running:

    # RGB
    screen.fill((0, 0, 0))
    # background image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether is right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_Sound = mixer.Sound('laser.wav')
                    bullet_Sound.play()

                    # get the current x coordinate of protective-wear
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # 5 = 5 + -0.1 -> 5 = 5 - 0.1
    # 5 = 5 + 0.1

    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # virus movement
    for i in range(num_of_virus):

        # game over
        if virusY[i] > 440:
            for j in range(num_of_virus):
                virusY[j] = 2000
            game_over_text()
            break

        virusX[i] += virusX_change[i]
        if virusX[i] <= 0:
            virusX_change[i] = 2
            virusY[i] += virusY_change[i]
        elif virusX[i] >= 736:
            virusX_change[i] = - 2
            virusY[i] += virusY_change[i]

        # collision
        collision = iscollision(virusX[i], virusY[i], bulletX, bulletY)
        if collision:
            explosion_Sound = mixer.Sound('explosion.wav')
            explosion_Sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            virusX[i] = random.randint(0, 736)
            virusY[i] = random.randint(50, 150)

        virus(virusX[i], virusY[i], )

    # bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)

    pygame.display.update()
