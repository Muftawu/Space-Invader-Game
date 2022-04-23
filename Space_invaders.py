import pygame
import math
import random

pygame.init()
WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")
run = True
font = pygame.font.Font('moochio/MOOCHIO.ttf', 40)
score = 0
scoreX, scoreY = 30, 30

# SPACESHIP PARAMETERS
spaceship = pygame.image.load("spaceship.png")
spaceship = pygame.transform.scale(spaceship, (90, 90))
spaceshipX, spaceshipY = 350, 700
spaceshipX_change = 0

# INVADER PARAMETERS
invader = []
invaderX, invaderY = [], []
invaderX_change = []
invader_num = 4

for i in range(0, invader_num):
    invader.append(pygame.transform.scale(
        pygame.image.load("monster.png"), (90, 90)))
    invaderX.append(350)
    invaderY.append(10)
    invaderX_change.append(0.2)


# BULLET PARAMETERS
bullet = pygame.image.load("bullet.png")
bullet = pygame.transform.scale(bullet, (80, 80))
bulletX, bulletY = 350, spaceshipY
bulletState = "ready"

# BACKGROUND PARAMETETS
background = pygame.image.load("background.png")
background = pygame.transform.scale(background, (800, 800))
backgroundX, backgroundY = 250, 10

# Use of functional programming


def showSpaceship(x, y):
    screen.blit(spaceship, (x, y))


def showInvader(x, y, i):
    screen.blit(invader[i], (x[i], y[i]))


def showBackground(x, y):
    screen.blit(background, (x, y))


def firebullet(x, y):
    global bulletState
    bulletState = "fire"
    screen.blit(bullet, (x+20, y-10))


def check_collision(x1, y1, x2, y2):
    x_distance = x1 - x2
    y_distance = y1 - y2
    distance = math.sqrt(x_distance**2 + y_distance**2)
    if distance < 27:
        return True


def showScore(x, y):
    gamescore = font.render(f"Score: {score}", True, ((255, 0, 255)))
    screen.blit(gamescore, (x, y))

while run:
    showBackground(0, 0)

    for events in pygame.event.get():
        if events.type == pygame.QUIT:
            run = False

        if events.type == pygame.KEYDOWN:
            if events.key == pygame.K_LEFT:
                spaceshipX_change = -0.7
            if events.key == pygame.K_RIGHT:
                spaceshipX_change = 0.7
            if events.key == pygame.K_UP:
                if bulletState == "ready":
                    # spaceshipX = bulletX
                    bulletX = spaceshipX
                    firebullet(bulletX, bulletY)

        if events.type == pygame.KEYUP:
            if events.key == pygame.K_LEFT:
                spaceshipX_change = 0
            if events.key == pygame.K_RIGHT:
                spaceshipX_change = 0

    spaceshipX += spaceshipX_change

    if bulletState == "fire":
        firebullet(bulletX, bulletY)
        bulletY -= 1.5

    if bulletY <= 0:
        bulletY = spaceshipY
        bulletState = "ready"

    if spaceshipX >= 700:
        spaceshipX = 700
    if spaceshipX <= 0:
        spaceshipX = 0

    for i in range(0, invader_num):
        invaderX[i] += invaderX_change[i]
        if invaderX[i] >= 700:
            invaderX_change[i] = -0.2
            invaderY[i] += 30
        if invaderX[i] <= 0:
            invaderX_change[i] = 0.2
            invaderY[i] += 30

        showInvader(invaderX, invaderY, i)
        collision1 = check_collision(bulletX, bulletY, invaderX[i], invaderY[i])
    
        if collision1:
            invaderX[i], invaderY[i] = random.randint(10, 700), random.randint(0, 30)
            score += 1
    showScore(scoreX, scoreY)

    showSpaceship(spaceshipX, spaceshipY)

    pygame.display.update()
