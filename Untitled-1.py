import pygame
from os import listdir
from pygame. constants import QUIT, K_DOWN, K_UP, K_LEFT,K_RIGHT
import random

pygame.init()

screen = width, height = 800, 600
print(
    screen
)
BLACK = 0,0,0
WHITE = 255,255,255
RED  = 255,0,0
GREEN = 0,255,0
IMG_PATH = 'goose'
NEW_COLOR = (random.randint(0, 155), random.randint(50, 255), random.randint(50, 255))
font = pygame.font.SysFont('Verdana',20)

main_surface=pygame.display.set_mode(screen)



# player = pygame.Surface((20,20))
# player.fill(WHITE)
player_imgs = [pygame.image.load(IMG_PATH + "/" + file).convert_alpha() for file in listdir(IMG_PATH)]
player = player_imgs[0]

# player.fill(WHITE)
player_rect = player.get_rect()

player_speed=3


def create_enemy():    
    enemy = pygame.image.load('enemy.png').convert_alpha()
    enemy = pygame.transform.scale(enemy, (enemy.get_width() // 3, enemy.get_height() // 3))
    # enemy.fill(RED)
    enemy_rect = enemy_rect = pygame.Rect(width, random.randrange(height - enemy.get_height()), *enemy.get_size())
    enemy_speed = random.randint(1, 3)
    return [enemy, enemy_rect, enemy_speed]

    
    


def create_bonus():
    bonus = pygame.image.load('bonus.png').convert_alpha()
    bonus = pygame.transform.scale(bonus, (bonus.get_width() // 2, bonus.get_height() // 2))
    # bonus.fill(GREEN)
    bonus_rect = pygame.Rect(random.randrange(width - bonus.get_width()),0, *bonus.get_size())

    bonus_speed = random.randint(1,1)
    return [bonus, bonus_rect, bonus_speed]

bg = pygame.transform.scale(pygame.image.load('background.png').convert(), screen)

bg_x = 0
bgX2 = bg.get_width()
bg_speed = 3

CREATE_ENEMY = pygame.USEREVENT +1
pygame.time.set_timer(CREATE_ENEMY, 1500)

CREATE_BONUS = pygame.USEREVENT +2
pygame.time.set_timer(CREATE_BONUS, 1500)

CHANGE_IMG = pygame.USEREVENT +3
pygame.time.set_timer(CHANGE_IMG, 125)

img_index = 0

scores = 0

bonuses = []
enemies = []

is_working = True
clock = pygame.time.Clock()
while is_working:
    for event in pygame.event.get():
        if event.type == QUIT:
            is_working = False

        if event.type == CREATE_BONUS:
            bonuses.append(create_bonus())
        
        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())

        if event.type == CHANGE_IMG:
            img_index += 1
            if img_index == len(player_imgs):
                img_index = 0
            player = player_imgs[img_index]
            

        
    
    # # Інтерактив для зміни кольору кульки в момент зіткнення
    # if player_rect.left <= 0 or player_rect.right >= width:
        
    #     new_color = (random.randint(0, 155), random.randint(50, 255), random.randint(50, 255))
    #     player.fill(new_color)

    # if player_rect.top <= 0 or player_rect.bottom >= height:
        
    #     new_color = (random.randint(0, 155), random.randint(50, 255), random.randint(50, 255))
    #     # player.fill(new_color)
    #     player.fill(WHITE)

    

    pressed_keys = pygame.key.get_pressed()

    
    # main_surface.fill((WHITE))
    # main_surface.blit(bg, (0,0))

    bg_x -= bg_speed
    bgX2 -= bg_speed

    if bg_x < -bg.get_width():
        bg_x = bg.get_width()

    if bgX2 < -bg.get_width():
        bgX2 = bg.get_width()

    main_surface.blit(bg, (bg_x,0))
    main_surface.blit(bg, (bgX2,0))

    main_surface.blit(player,player_rect)
    Color_source = main_surface.blit(font.render(str(scores), True, NEW_COLOR), (width-30,0))

    

    for bonus in bonuses:
        bonus[1] = bonus[1].move(0, bonus[2])
        main_surface.blit(bonus[0], bonus[1])

        if bonus[1].bottom > height:
            bonuses.remove(bonus)

        if player_rect.colliderect(bonus[1]):
            bonuses.pop(bonuses.index(bonus))
            scores +=1
        main_surface.blit(font.render(str(scores), True, NEW_COLOR), (width-30,0))
            
        
    for enemy in enemies:
        enemy[1] = enemy[1].move(-enemy[2], 0)
        main_surface.blit(enemy[0], enemy[1])

        if enemy[1].left < 0:
            enemies.remove(enemy)

        if player_rect.colliderect(enemy[1]):
            is_working = False

    if pressed_keys[K_DOWN] and not player_rect.bottom >=height:
        player_rect = player_rect.move(0, player_speed)
    
    if pressed_keys[K_UP] and not player_rect.top <= 0:
        player_rect = player_rect.move(0,-player_speed)

    if pressed_keys[K_RIGHT] and not player_rect.right >= width:
        player_rect = player_rect.move(player_speed,0)

    if pressed_keys[K_LEFT] and not player_rect.left <= 0:
        player_rect = player_rect.move(-player_speed,0)
    
    
    # print(len(bonuses))
    # print(len(enemies))
    # main_surface.fill((155,155,155))
    pygame.display.flip()
    clock.tick(80)
