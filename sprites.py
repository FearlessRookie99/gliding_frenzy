import pygame
import os
from settings import *
import random
from abc import ABC, abstractmethod

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)  # Richtiges Initialisieren

        
        self.image_dict = {}
        for nr in range(1, 9):
            self.image_dict["coin"+str(nr)] = pygame.image.load('sprites/coin'+str(nr)+'.png')


        # Animation
        self.max_frames = 8
        self.akt_frame = random.randint(1, 8)
        self.anim_rate = 1
        self.image = self.image_dict["coin"+str(self.akt_frame)]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.timer = 0



    def update(self,game_speed):
        
        self.rect.x -= game_speed
        self.timer += 1
        if self.timer > self.anim_rate:
            self.timer = 0
            self.akt_frame += 1
            if self.akt_frame > self.max_frames:
                self.akt_frame = 1
            self.image = self.image_dict["coin"+str(self.akt_frame)]


class ZapperHiro(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.image_dict = {}
        for nr in range(1, 9):
            self.image_dict["Zapper_waage"+str(nr)] = pygame.image.load('sprites/Zapper_waage'+str(nr)+'.png')

        
        self.x = x
        self.y = y
        self.max_frames = 8
        self.akt_frame = random.randint(1, 8)
        self.anim_rate = 1
        self.image = self.image_dict["Zapper_waage"+str(self.akt_frame)]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        hitbox_width = 255
        hitbox_height = 35
        self.hitbox = pygame.Rect(self.x + 22 , self.y + 18, hitbox_width, hitbox_height)
        self.timer = 0

    def update(self,game_speed):
        self.rect.x -= game_speed
        self.hitbox.x -= game_speed
        self.x -= game_speed 
        if self.rect.right < 0:
            self.kill()
        self.timer += 1
        if self.timer > self.anim_rate:
            self.timer = 0
            self.akt_frame += 1
            if self.akt_frame > self.max_frames:
                self.akt_frame = 1
            self.image = self.image_dict["Zapper_waage"+str(self.akt_frame)]
            self.image = pygame.transform.scale(self.image , (300 , 70))
    
class ZapperVer(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        
        self.image_dict = {}
        for nr in range(1, 9):
            self.image_dict["Zapper_senk"+str(nr)] = pygame.image.load('sprites/Zapper_senk'+str(nr)+'.png')

        self.x = x
        self.y = y
        self.max_frames = 8
        self.akt_frame = random.randint(1, 8)
        self.anim_rate = 1
        self.image = self.image_dict["Zapper_senk"+str(self.akt_frame)]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.hitbox_width = 35
        self.hitbox_height = 255
        self.hitbox = pygame.Rect(self.x + 18 , self.y + 22, self.hitbox_width, self.hitbox_height)
        self.timer = 0


    def update(self,game_speed):
        
        self.rect.x -= game_speed
        self.hitbox.x -= game_speed
        self.x -= game_speed
        if self.rect.right < 0:
            self.kill() 
        self.timer += 1
        if self.timer > self.anim_rate:
            self.timer = 0
            self.akt_frame += 1
            if self.akt_frame > self.max_frames:
                self.akt_frame = 1
            self.image = self.image_dict["Zapper_senk"+str(self.akt_frame)]
            self.image = pygame.transform.scale(self.image , (70 , 300))


class Rocket(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("sprites/rocket.png")
        self.image = pygame.transform.scale(self.image, (50, 50))  # Adjust size as needed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.hitbox = self.rect
        self.fire_animation = FireAnimation(self.rect.x, self.rect.y)

    def update(self,game_speed):
        
        self.rect.x -= game_speed + 7  # Rockets move faster than the game speed
        self.hitbox.x -= game_speed
        self.fire_animation.rect.x = self.rect.x + 30
        self.fire_animation.rect.y = self.rect.y - 35   # 
        self.fire_animation.update()
        if self.rect.right < 0:
            self.kill()  

class FireAnimation(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image_dict = {}
        for nr in range(1, 5):
            self.image_dict["fire_"+str(nr)] = pygame.image.load('sprites/fire_'+str(nr)+'.png')

        
        self.max_frames = 4
        self.akt_frame = random.randint(1, 4)
        self.anim_rate = 4
        self.image = self.image_dict["fire_"+str(self.akt_frame)]
        self.rect = self.image.get_rect()
        self.timer = 0

    def update(self):
        self.timer += 1
        if self.timer > self.anim_rate:
            self.timer = 0
            self.akt_frame += 1
            if self.akt_frame > self.max_frames:
                self.akt_frame = 1
            self.image = self.image_dict["fire_"+str(self.akt_frame)]
            self.image = pygame.transform.scale(self.image , (200 , 120))
            


class WarningSign(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.image_dict = {}
        for nr in range(1, 7):
            self.image_dict["exclamat"+str(nr)] = pygame.image.load('sprites/exclamat'+str(nr)+'.png')

        self.max_frames = 6
        self.akt_frame = random.randint(1, 6)
        self.anim_rate = 1
        self.image = self.image_dict["exclamat"+str(self.akt_frame)]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.timer = 0

    def update(self):
        self.timer += 1
        if self.timer > self.anim_rate:
            self.timer = 0
            self.akt_frame += 1
            if self.akt_frame > self.max_frames:
                self.akt_frame = 1
                    #self.timer = 0
            self.image = self.image_dict["exclamat"+str(self.akt_frame)]
            self.image = pygame.transform.scale(self.image , (50 , 50)) 

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, player):
        pygame.sprite.Sprite.__init__(self)  
        self.player = player
        self.type = random.choice(["invincibility", "shield", "score_bonus"])
        self.image = pygame.image.load("powerUp pngs/donut.png")         
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH  
        self.rect.y = random.randint(50, HEIGHT - 50)  # Random height

    def update(self,game_speed):
        self.rect.x -= game_speed #von rechts nach links über den Bildschirm schweben

    def apply_effect(self): # abhängig von der random.choice bei self.type
        if self.type == "invincibility":
            pygame.mixer.Sound('sounds/timer.mp3').play()
            self.player.activate_invincibility(10 * FPS)  # Für 10 Sekunden inv
        if self.type == "shield":
            pygame.mixer.Sound('sounds/shield-guard.mp3').play()
            self.player.activate_shield() 
        if self.type == "score_bonus":
            pygame.mixer.Sound('sounds/cha-ching.mp3').play()
            self.player.score += 1500  # Erhöhung des scores um 1500

