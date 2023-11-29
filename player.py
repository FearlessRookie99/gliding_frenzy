import pygame
from settings import * 
class Player:
    def __init__(self):
        self.init_y = HEIGHT - 130
        self.player_y = self.init_y
        self.x = 120
        self.booster = False
        self.counter = 0
        self.franky_width = 70
        self.franky_height = 105
        self.image_dict = {}
        self.image_dict["player_1"] = pygame.image.load("franky pngs/sprite_1.png")
        self.image_dict["player_1"] = pygame.transform.scale(self.image_dict["player_1"], (self.franky_width, self.franky_height))
        self.image_dict["player_2"] = pygame.image.load("franky pngs/sprite_2.png")
        self.image_dict["player_2"] = pygame.transform.scale(self.image_dict["player_2"], (self.franky_width, self.franky_height))
        self.image_dict["player_3"] = pygame.image.load("franky pngs/sprite_3.png")
        self.image_dict["player_3"] = pygame.transform.scale(self.image_dict["player_3"], (self.franky_width, self.franky_height))
        self.image_dict["player_4"] = pygame.image.load("franky pngs/sprite_4.png")
        self.image_dict["player_4"] = pygame.transform.scale(self.image_dict["player_4"], (self.franky_width, self.franky_height))
        self.image_dict["player_5"] = pygame.image.load("franky pngs/sprite_5.png")
        self.image_dict["player_5"] = pygame.transform.scale(self.image_dict["player_5"], (self.franky_width, self.franky_height))
        self.image_dict["player_fly"] = pygame.image.load("franky pngs/sprite_fly.png")
        self.image_dict["player_fly"] = pygame.transform.scale(self.image_dict["player_fly"], (self.franky_width, self.franky_height))
        self.image_dict["jetpack_off"] = pygame.image.load("franky pngs/jetpack_off.png")
        self.image_dict["jetpack_off"] = pygame.transform.scale(self.image_dict["jetpack_off"], (50, 60))
        self.image_dict["jetpack_on"] = pygame.image.load("franky pngs/jetpack_on.png")
        self.image_dict["jetpack_on"] = pygame.transform.scale(self.image_dict["jetpack_on"], (50, 60))
        self.hitbox = pygame.Rect(self.x, self.player_y, 40, 80)
        self.rect = self.hitbox  # Alias hitbox as rect for Pygame compatibility
        self.score = 0  # Initial score


    def update(self):
        # ... code to update player's position ...
        self.hitbox.x = self.x
        self.hitbox.y = self.player_y
        self.rect = self.hitbox  # Update the rect as well

    def draw(self, screen):

        hitbox_width = 40
        hitbox_height = 80
        y_faktor = 20
        x_offset = -15 
        y_offset = -15
       
        if self.booster:
                jetpack = pygame.rect.Rect((self.x - 15, self.player_y + 50), (25, 40))
                screen.blit(self.image_dict["jetpack_on"], jetpack)
        else: 
            jetpack = pygame.rect.Rect((self.x - 15, self.player_y + 50), (25, 40))
            screen.blit(self.image_dict["jetpack_off"], jetpack)
        if self.player_y == self.init_y:
            player = pygame.rect.Rect((self.x, self.player_y + y_faktor), (hitbox_width, hitbox_height))
            screen.blit(self.image_dict["player_5"], (player.x + x_offset, player.y + y_offset))
        if self.player_y < self.init_y :
            player = pygame.rect.Rect((self.x, self.player_y + y_faktor), (hitbox_width, hitbox_height))
            screen.blit(self.image_dict["player_fly"], (player.x + x_offset, player.y + y_offset))
        if self.player_y > self.init_y:
            if self.counter < 5:
                player = pygame.rect.Rect((self.x, self.player_y + y_faktor), (hitbox_width, hitbox_height))
                screen.blit(self.image_dict["player_3"], (player.x + x_offset, player.y + y_offset))
            elif 5 <= self.counter < 10:
                player = pygame.rect.Rect((self.x, self.player_y + y_faktor), (hitbox_width, hitbox_height))
                screen.blit(self.image_dict["player_4"], (player.x + x_offset, player.y + y_offset - 3))
            elif 10 <= self.counter < 15:
                player = pygame.rect.Rect((self.x, self.player_y + y_faktor), (hitbox_width, hitbox_height))
                screen.blit(self.image_dict["player_2"], (player.x + x_offset, player.y + y_offset))
            elif 15 <= self.counter < 20:
                player = pygame.rect.Rect((self.x, self.player_y + y_faktor), (hitbox_width, hitbox_height))
                screen.blit(self.image_dict["player_5"], (player.x + x_offset, player.y + y_offset))
            elif 20 <= self.counter < 25:
                player = pygame.rect.Rect((self.x, self.player_y + y_faktor), (hitbox_width, hitbox_height))
                screen.blit(self.image_dict["player_3"], (player.x + x_offset, player.y + y_offset))
            elif 25 <= self.counter < 30:
                player = pygame.rect.Rect((self.x, self.player_y + y_faktor), (hitbox_width, hitbox_height))
                screen.blit(self.image_dict["player_4"], (player.x + x_offset, player.y + y_offset - 3))
            elif 30 <= self.counter < 35:
                player = pygame.rect.Rect((self.x, self.player_y + y_faktor), (hitbox_width, hitbox_height))
                screen.blit(self.image_dict["player_3"], (player.x + x_offset, player.y + y_offset))
            else:
                player = pygame.rect.Rect((self.x, self.player_y + y_faktor), (hitbox_width, hitbox_height))
                screen.blit(self.image_dict["player_5"], (player.x + x_offset, player.y + y_offset))
        pygame.draw.rect(screen, 'green', player, 5)
        
        
        return player

    def check_colliding(self, decke, boden):
        coll = [False, False]
        if self.player.colliderect(boden):
            coll[0] = True
        elif self.player.colliderect(decke):
            coll[1] = True
        return coll
        
    def collect_coins(self, coins_group):
        collected_coins = pygame.sprite.spritecollide(self, coins_group, True, pygame.sprite.collide_rect)
        self.score += len(collected_coins)  # Erhöhe den Score für jede gesammelte Münze
        return len(collected_coins)

