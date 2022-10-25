import random

import pygame
from pygame.locals import *
from pygame import mixer

pygame.init()

WIDTH = 1000
HEIGHT = 600

x = 125
y = HEIGHT / 2

y_vel = 0

MAX_ITEMS = 4

jump_force = 10

jump = False

died = False

items = []

click = False

score = 0

rocks = []

detectSound = False

reloadJump = 0

fuel = 10

jumpSound = mixer.Sound("sound/jump.wav")

pointSound = mixer.Sound("sound/point.wav")

boomSound = mixer.Sound("sound/boom.wav")

start = False

gravity = 0.55
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Air Strikers X")

player_img = pygame.image.load("img/player.png")
player_img = pygame.transform.scale(player_img, (50, 35))            
player = player_img.get_rect(center=(x, y))
angle = 0

item_img = pygame.image.load("img/item.png")
item_img = pygame.transform.scale(item_img, (35, 35))

rock_img = pygame.image.load("img/rock.png")
rock_img = pygame.transform.scale(rock_img, (35, 35))     

play_button_img = pygame.image.load("img/button.png")
play_button_img = pygame.transform.scale(play_button_img, (250, 125))
play_button = play_button_img.get_rect(center=(WIDTH/2 - 25, HEIGHT - 225))

backdrop = pygame.image.load("img/backdrop.png")
backdrop = pygame.transform.scale(backdrop, (WIDTH, HEIGHT))

homescreen = pygame.image.load("img/homescreen.png")
homescreen = pygame.transform.scale(homescreen, (WIDTH, HEIGHT))

crs = pygame.Rect(1, 1, 1, 1)

def draw_window():
    screen.blit(backdrop, (0, 0))
    
    for item in items:
        screen.blit(item_img, (item.x, item.y))
        
    for rock in rocks:
        screen.blit(rock_img, (rock.x, rock.y))
    
    Player.Movement()
    Player.UI()
    pygame.display.update()
    
class Player():
    
    def Movement():
        
        global detectSound
        global x
        global y
        global y_vel
        global angle
        global fuel
        global start
        global died
        global jump
        global jumpSound
        global reloadJump
        keys = pygame.key.get_pressed()
        
        y_vel -= gravity
        
        if (keys[pygame.K_SPACE] and fuel > 0.1) and reloadJump < 0.1:
            jump = True
            reloadJump = 1
            jumpSound.play()
        else:
            jump = False
            detectSound = False
            
        if reloadJump > 0.1:
            reloadJump -= 0.045

        if jump == True:
            y_vel = 11.55
            angle -= 1
            if angle > -45:
                angle = -45
            angle %= 360
            surf = pygame.transform.rotate(player_img, (angle*-1))
            screen.blit(surf, (player.x, player.y))
            fuel -= 1
        else:
            angle += 1
            if angle > 45:
                angle = 45
            angle %= 360
            surf = pygame.transform.rotate(player_img, (angle*-1))
            screen.blit(surf, (player.x, player.y))

        if player.y > HEIGHT - 1:
            start = False
            died = True
        else:
            if player.y < 1:
                y = 2
                y_vel = 0
                          
        y -= y_vel
        
        player.x = x
        player.y = y
        
        pygame.display.update()
        
    def ItemSpawning():
        global items
        global fuel
        
        if len(items) < MAX_ITEMS:
            item = item_img.get_rect(center=(WIDTH - 1, random.randint(100, WIDTH - 100)))
            items.append(item)
            
        if len(rocks) < 1:
            rock = rock_img.get_rect(center=(WIDTH - 1, random.randint(100, WIDTH - 100)))
            rocks.append(rock)
            
    def ItemAI():
        global items
        global fuel
        global score
        global pointSound
        global boomSound
        
        for item in items:
            item.x -= 6.5

            if item.x < 1:
                items.remove(item)
                
            if item.colliderect(player):
                items.remove(item)
                fuel += 1
                score += 1
                pointSound.play()
                
        for rock in rocks:
            rock.x -= 6.5

            if rock.x < 1:
                rocks.remove(rock)
                
            if rock.colliderect(player):
                fuel %= 2
                rocks.remove(rock)
                boomSound.play()
                
    def UI():
        screen_text = font.render("fuel: ", True, "white")
        screen.blit(screen_text, (50, 50))
        screen_text = font.render(str(round(fuel)), True, "white")
        screen.blit(screen_text, (135, 50))
        screen_text = font.render("score: ", True, "white")
        screen.blit(screen_text, (WIDTH - 175, 50))
        screen_text = font.render(str(round(score)), True, "white")
        screen.blit(screen_text, (WIDTH - 60, 50))
        pygame.display.update()

font = pygame.font.SysFont(None, 50)

def HomeScreen():
    
    global died
    
    screen.blit(homescreen, (0, 0))
    screen.blit(play_button_img, (play_button.x, play_button.y))
    
    if died == True:
        screen_text = font.render("You Died!", True, "white")
        screen.blit(screen_text, (WIDTH / 2 - 100, HEIGHT - 100))
    else:
        if died == False:
            screen_text = font.render("Start Game", True, "white")
            screen.blit(screen_text, (WIDTH / 2 - 100, HEIGHT - 100))
                        
    pygame.display.update()

def main_loop():
    
    global fuel
    global start
    global y_vel
    global x
    global y
    global score
    global jump
    global angle
    global click
    
    gameExit = False
    while gameExit == False:
        
        mx, my = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True    
        
        if start == True:
            draw_window()
            Player.UI()
            Player.ItemSpawning()
            Player.ItemAI()
            Player.UI()
            
        else:
            
            mixer.music.load("sound/soundtrack.wav")
            mixer.music.play(-1)
            
            if start == False:
                HomeScreen()
                crs.x = mx
                crs.y = my
                
                if crs.colliderect(play_button):
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        start = True
                        
                        for item in items:
                            items.remove(item)
                            
                        for rock in rocks:
                            rocks.remove(rock)
                            
                        x = 125
                        y = HEIGHT / 2
                        
                        fuel = 10
                        
                        score = 0
                        
                        y_vel = 0
      
        if crs.colliderect(play_button):
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
            else:
                click = False

    pygame.quit()

if __name__ == "__main__":
    main_loop()