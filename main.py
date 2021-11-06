import pygame
import random
import math
from pygame import mixer

# init the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# background sound
# mixer.music.load("background.wav")
# mixer.music.play(-1)

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
# enemies
enemiesImage = []
enemiesX = []
enemiesY = []
enemiesXChange = []
numOfEnemies = 6
enemyXSpeed = 2
enemyYSpeed = 10

for i in range(numOfEnemies):
    enemiesImage.append(pygame.image.load("enemy.png"))
    enemiesX.append(random.randint(0, 736))
    enemiesY.append(random.randint(0, 100))
    enemiesXChange.append(1)

# bullet
bulletImage = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletYChange = 1
bulletYSpeed = 10
# bullet state: ready, fire: the bullet is moving
bulletState = "ready"

# score
score = 0
font = pygame.font.Font("freesansbold.ttf", 32)
textX = 10
textY = 10

# game over
overFont = pygame.font.Font("freesansbold.ttf", 64)


def displayScore(x, y):
    scoreText = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(scoreText, (x, y))


def displayGameOver():
    overText = overFont.render("Game Over", True, (255, 255, 255))
    screen.blit(overText, (200, 250))


def player(x, y):
    screen.blit(playerImage, (x, y))


def enemy(x, y, i):
    screen.blit(enemiesImage[i], (x, y))


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
                    bulletSound = mixer.Sound("laser.wav")
                    bulletSound.play()
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
    for i in range(numOfEnemies):
        if enemiesY[i] > 470:
            for j in range(numOfEnemies):
                enemiesY[j] = 1000
            displayGameOver()
            break

        if enemiesX[i] <= 0:
            enemiesXChange[i] = enemyXSpeed
            enemiesY[i] += enemyYSpeed
        if enemiesX[i] >= 736:
            enemiesXChange[i] = -enemyXSpeed
            enemiesY[i] += enemyYSpeed
        enemiesX[i] += enemiesXChange[i]
        enemy(enemiesX[i], enemiesY[i], i)

        # detect collision
        collision = isCollision(enemiesX[i], enemiesY[i], bulletX, bulletY)
        if collision and bulletState is "fire":
            explosionSound = mixer.Sound("explosion.wav")
            explosionSound.play()
            bulletState = "ready"
            bulletY = 480
            score += 1
            print(score)
            enemiesX[i] = random.randint(0, 736)
            enemiesY[i] = random.randint(0, 100)

    displayScore(textX, textY)
    pygame.display.update()
