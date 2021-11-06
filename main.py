import pygame
import random
import math

# init the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# background image
backgroundImage = pygame.image.load("background.jpg")

# title and icon
icon = pygame.image.load("spaceship.png")
pygame.display.set_caption("Space war")
pygame.display.set_icon(icon)

# player
playerImage = pygame.image.load("player.png")
playerX = 370
playerY = 480
playerXChange = 0
playerXSpeed = 2

# enemy
enemyImage = pygame.image.load("enemy.png")
enemyX = random.randint(0, 736)
enemyY = random.randint(0, 100)
enemyXChange = 1
enemyXSpeed = 2
enemyYSpeed = 20

# bullet
bulletImage = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletYChange = 1
bulletYSpeed = 10
# bullet state: ready, fire: the bullet is moving
bulletState = "ready"

score = 0

def player(x, y):
    screen.blit(playerImage, (x, y))


def enemy(x, y):
    screen.blit(enemyImage, (x, y))


def fireBullet(x, y):
    global bulletState
    bulletState = "fire"
    screen.blit(bulletImage, (x + 16, y - 20))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    if distance < 27:
        return True
    else:
        return False


# game loop
running = True
while running:
    # setup background color
    screen.fill((0, 0, 0))
    screen.blit(backgroundImage, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # check keystroke
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerXChange = -playerXSpeed
            if event.key == pygame.K_RIGHT:
                playerXChange = playerXSpeed
            if event.key == pygame.K_SPACE:
                if bulletState is "ready":
                    bulletX = playerX
                    fireBullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            playerXChange = 0

    # move player
    playerX += playerXChange

    if playerX <= 0:
        playerX = 0
    if playerX >= 736:
        playerX = 736
    player(playerX, playerY)

    # bullet movement
    if bulletY <= 0:
        bulletY = 480
        bulletState = "ready"
    if bulletState is "fire":
        fireBullet(bulletX, bulletY)
        bulletY -= bulletYSpeed

    # move enemy
    if enemyX <= 0:
        enemyXChange = enemyXSpeed
        enemyY += enemyYSpeed
    if enemyX >= 736:
        enemyXChange = -enemyXSpeed
        enemyY += enemyYSpeed
    enemyX += enemyXChange
    enemy(enemyX, enemyY)

    # detect collision
    collision = isCollision(enemyX, enemyY, bulletX, bulletY)
    if collision:
        bulletState = "ready"
        bulletY = 480
        score += 1
        print(score)
        enemyX = random.randint(0, 736)
        enemyY = random.randint(0, 100)
    pygame.display.update()
