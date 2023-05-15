import pygame
import random
from find_max import find_max
from pygame import mixer
import os

# Initialize the pygame
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()
pygame.mixer.init()
game_on = True
currentDir = os.getcwd()

# Create the screen
width = 800
height = 800
screen = pygame.display.set_mode((width, height))

# CRASH SOUND
crash_sound = pygame.mixer.Sound(r"{}//pygame//carcrash.mp3".format(currentDir))

# IMAGES
green = pygame.image.load(r"{}//pygame//green.jpg".format(currentDir)).convert()
grey = pygame.image.load(r"{}//pygame//grey.jpg".format(currentDir)).convert()
tiles = pygame.image.load(r"{}//pygame//road.png".format(currentDir))
car = pygame.image.load(r"{}//pygame//car.png".format(currentDir))
tree = pygame.image.load(r"{}//pygame//tree.png".format(currentDir))
enemy = pygame.image.load(r"{}//pygame//encar1.png".format(currentDir))
follower = pygame.image.load(r"{}//pygame//encar2.png".format(currentDir))

# TITLE & ICON
pygame.display.set_caption("Race")
icon = pygame.image.load(r"{}//pygame//racing-flag.png".format(currentDir))
pygame.display.set_icon(icon)

# ROAD
road_Y = 20
roadY_change = 1
roadX = 368
roadY = list()
road_img = list()
road_number = 8
for i in range(road_number):
    roadY.append(road_Y)
    road_img.append(tiles)
    road_Y += 128


def show_road(img, x, y):
    screen.blit(img, (x, y))


# CAR
carleft_speed = -1.6
carright_speed = 1.6
carX_change = 0
carX = 368
carY = 680


def show_car(x, y):
    screen.blit(car, (x, y))


# TREE
treeX = 24
treeY = 24
tree_X = []
tree_Y = []
treeY_change = 1
tree_number = 16
for i in range(tree_number):
    tree_X.append(treeX)
    tree_Y.append(treeY)
    if i % 2 == 1:
        treeY += 96
    if i % 4 == 0:
        treeX += 600
    elif i % 4 == 1:
        treeX -= 490
    elif i % 4 == 2:
        treeX += 600
    elif i % 4 == 3:
        treeX -= 710


def show_tree(x, y):
    screen.blit(tree, (x, y))


# GAME OVER
game_over_font = pygame.font.Font("freesansbold.ttf", 64)


def game_over():
    gameover = game_over_font.render("GAME OVER!", True, (255, 0, 0))
    screen.blit(gameover, (190, 350))


# ENEMY
enemyX = []
enemyY = []
enemyY_change = 0.8
enemy_number = 3
for i in range(enemy_number):
    enemyX.append(random.randint(204, 532))
    enemyY.append(-56)


def show_enemy(x, y):
    screen.blit(enemy, (x, y))


# FOLLOWER ENEMY
followerX = 250
followerY = -56
followerY_change = 0.7
followerX_change = 0.18
follower_round = 10


def show_follower(x, y):
    difference = x - carX
    screen.blit(follower, (x, y))
    if difference >= 0:
        x -= followerX_change
        return x
    elif difference < 0:
        x += followerX_change
        return x


# ROUNDS
round_font = pygame.font.Font("freesansbold.ttf", 25)
round_number = 0


def show_rounds():
    rounds = round_font.render("Rounds: " + str(round_number), True, (0, 0, 0))
    screen.blit(rounds, (15, 15))


# RECORD
record_number = find_max()


def show_record():
    record = round_font.render("RECORD: " + record_number, True, (0, 0, 0))
    screen.blit(record, (635, 15))


bir_kere_yazdirma = 0
collision = False
background = pygame.Surface((width, height))
background.blit(green, (0, 0))
background.blit(grey, (200, 0))
background.blit(green, (600, 0))


# GAME LOOP
while game_on:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_on = False
        # CHECKING IF A KEY IS "PRESSED"
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                carX_change = carleft_speed
            elif event.key == pygame.K_RIGHT:
                carX_change = carright_speed

        # CHECKING IF A KEY IS "DROPPED"
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                carX_change = 0

    # BOUNDARIES OF THE CAR
    if carX >= 546:
        carX = 546
    elif carX <= 194:
        carX = 194

    # SHOWING THE TREES
    for i in range(tree_number):
        if i % 2 == 0:
            roadIndex = int(i / 2)
            show_road(road_img[roadIndex], roadX, roadY[roadIndex])
            roadY[roadIndex] += roadY_change
            if roadY[roadIndex] >= 800:
                roadY[roadIndex] = 20
        show_tree(tree_X[i], tree_Y[i])
        tree_Y[i] += treeY_change
        if tree_Y[i] >= 776:
            tree_Y[i] = 24

    # COUNTING THE SCORE
    if collision is False:
        if enemyY[enemy_number -1] < -99:
            round_number += 1
        # SPEEDING UP THE GAME
        if roadY_change <= 3.9:
            roadY_change += 0.00145
            treeY_change += 0.00145
            enemyY_change += 0.0015
            carleft_speed -= 0.00018
            carright_speed += 0.00018
            followerY_change += 0.0015

    # SHOWING THE ENEMY
    for i in range(enemy_number):
        show_enemy(enemyX[i], enemyY[i])
        enemyY[i] += enemyY_change
        if enemyY[i] >= 800:
            enemyX[i] = random.randint(204, 532)
            enemyY[i] = -100

        # COLLISION
        if enemyY[enemy_number-1] > 700:
            car_rect = pygame.Rect(carX + 15, carY, 34, 64)
            follower_rect = pygame.Rect(followerX + 13, followerY, 38, 64)
            enemy_rect = pygame.Rect(enemyX[i] + 13, enemyY[i], 38, 64)
            collide1 = car_rect.colliderect(enemy_rect)
            collide2 = car_rect.colliderect(follower_rect)
            enemy_collide = enemy_rect.colliderect(follower_rect)
            if collide1 or collide2:
                crash_sound.play()
                carright_speed = 0
                carleft_speed = 0
                treeY_change = 0
                enemyY_change = 0
                roadY_change = 0
                collision = True
                for i in range(enemy_number):
                    enemyY[i] = 1000
                followerY = 2000
                followerY_change = 0
                game_over()
                if bir_kere_yazdirma == 0:
                    file = open("score.txt", "a")
                    file.write(str(round_number) + "\n")
                    bir_kere_yazdirma += 1

    if round_number >= follower_round:
        enemy_number = 2
        followerX = show_follower(followerX, followerY)
        if followerY >= 800:
            followerY = -100
            followerX = random.randint(204, 532)
        followerY += followerY_change

    show_record()
    show_rounds()
    show_car(carX, carY)
    carX += carX_change
    pygame.display.update()

