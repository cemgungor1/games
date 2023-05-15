import pygame
import random
import math
import os

# Initialize the pygame
pygame.init()

# Creating the screen
screen = pygame.display.set_mode((800, 600))
game_is_on = True

currentDir = os.getcwd()
background = pygame.image.load(r"{}//pygame//stars.jpg".format(currentDir))

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load(r"{}//pygame//ufo.png".format(currentDir))
pygame.display.set_icon(icon)

# SPACE SHIP
spaceship = pygame.image.load(r"{}//pygame//battleship.png".format(currentDir))
playerX = 368
playerY = 520
playerX_change = 0
playerY_change = 0

# EXPLOSION
explosion = pygame.image.load(r"{}//pygame//explosion.png".format(currentDir))


def show_explosion(x, y):
    screen.blit(explosion, (x, y))


# ENEMY
# Enemy random movement
speed_list = [-0.3, 0.3]

enemyNumber = 6
enemy_img = []
enemyX = []
enemyY = []
enemyX_change = []
for i in range(enemyNumber):
    choose = random.randint(0, 1)
    enemy_img.append(pygame.image.load(r"{}//pygame//alien.png".format(currentDir)))
    enemyX.append(random.randint(0, 740))
    enemyY.append(random.randint(0, 100))
    if choose == 1:
        enemyX_change.append(speed_list[0])
    else:
        enemyX_change.append(speed_list[1])

enemyY_change = 0.055

# BULLET
bullet_img = pygame.image.load(r"{}//pygame//bullet.png".format(currentDir))
bulletX = 0
bulletY = 480
bulletY_change = 0.95
bullet_state = "ready"


# Can't fire a bullet if its not ready

# Display bullet in screen
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x + 20, y + 25))


# Display player in screen
def player(x, y):
    screen.blit(spaceship, (x, y))


# Display enemy in screen
def enemy(x, y, a):
    screen.blit(enemy_img[a], (x, y))


# Collision
def collision(enemyX, enemyY, bulletX, bulletY, lenght):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    if distance < lenght:
        return True
    else:
        return False


# Game Over
over_font = pygame.font.Font("freesansbold.ttf", 64)


def game_over_text():
    over = over_font.render("GAME OVER!", True, (255, 0, 0))
    screen.blit(over, (200, 250))


# SCORE
score_value = 0
font = pygame.font.Font("freesansbold.ttf", 26)
textX = 10
textY = 10
is_show_score = True


def show_score(x, y):
    if is_show_score:
        score = font.render("Score: " + str(score_value), True, (255, 255, 255))
        screen.blit(score, (x, y))


# GAME LOOP
while game_is_on:
    # Filling the screen with RGB colors
    screen.fill((0, 0, 0))
    # Background image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_is_on = False
        # Check whether keystroke is pressed and whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.7
            elif event.key == pygame.K_RIGHT:
                playerX_change = 0.7
            if event.key == pygame.K_SPACE and bullet_state == "ready":
                bulletX = playerX
                fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerY_change = 0
                playerX_change = 0

    if playerX >= 799:
        playerX = -63
    elif playerX <= -64:
        playerX = 798
    # ENEMY MOVEMENT

    for i in range(enemyNumber):
        # GAME OVER
        if enemyY[i] >= 484:
            for j in range(enemyNumber):
                enemyY[j] = 2000
            game_over_text()
            score = font.render("Your final score is: " + str(score_value), True, (255, 255, 255))
            screen.blit(score, (285, 320))
            is_show_score = False
            playerX_change = 0
            playerY_change = 0
        # --------------------------------
        enemyY[i] += enemyY_change
        enemyX[i] += enemyX_change[i]
        if enemyX[i] > 741:
            enemyX_change[i] = -0.35
        elif enemyX[i] < 0:
            enemyX_change[i] = 0.35
        if enemyY[i] >= 484:
            enemyY_change = 0
            for r in range(enemyNumber):
                enemyX_change[r] = 0
        # COLLISION
        if enemyY[i] < 484:
            collision_ = collision(enemyX[i], enemyY[i], bulletX, bulletY, 24)
            if collision_ is True:
                bulletY = 480
                bullet_state = "ready"
                score_value += 1
                enemyX[i] = random.randint(0, 740)
                enemyY[i] = random.randint(0, 100)

        enemy(enemyX[i], enemyY[i], i)
    # ------------------------------
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
    if bulletY <= -10:
        bullet_state = "ready"
        bulletY = 480

    playerX += playerX_change
    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
