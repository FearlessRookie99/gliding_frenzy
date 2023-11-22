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



    def update(self):
        self.rect.x -= game_speed
        self.timer += 1
        if self.timer > self.anim_rate:
            self.timer = 0
            self.akt_frame += 1
            if self.akt_frame > self.max_frames:
                self.akt_frame = 1
                #self.timer = 0
            self.image = self.image_dict["coin"+str(self.akt_frame)]


coin_group = pygame.sprite.Group()

