import random
import pygame
from settings import *




class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.init_y = HEIGHT - 100
        self.x = 120
        self.booster = False
        self.counter = 0
        self.image = None  # This will be set in subclasses
        self.hitbox_width = 25
        self.hitbox_height = 80
        self.rect = pygame.Rect(self.x  , self.init_y , self.hitbox_width, self.hitbox_height)
        self.score = 0
        self.collected_coins = 0
        self.state=NormalState()
        self.is_invincible = False
        self.invincibility_duration = 0
        self.has_shield = False
        self.shield_invincibility_duration = 0
        self.y_velocity = 0
        self.image_width = 135
        self.image_height = 185
        self.x_offset = -60
        self.y_offset = -50
        self.jetpack_image_size = (45,60)
        self.jetpack_x_offset = 18
        self.jetpack_y_offset = 25
        self.image_dict = {}
        self.image_dict["jetpack_off"] = pygame.image.load("luffy pngs/jetpack_off.png")
        self.image_dict["jetpack_off"] = pygame.transform.scale(self.image_dict["jetpack_off"], self.jetpack_image_size)            
        self.image_dict["jetpack_on"] = pygame.image.load("luffy pngs/jetpack_on.png")
        self.image_dict["jetpack_on"] = pygame.transform.scale(self.image_dict["jetpack_on"], self.jetpack_image_size)
        self.image_dict["shield"]= pygame.image.load("powerUp pngs/shield.png")  
        self.image_dict["inv"]= pygame.image.load("powerUp pngs/hour-glass.png")
        

    def update(self):
        self.counter = (self.counter + 1) % 40
        self.state.update(self)
        if self.is_invincible:
            self.invincibility_duration -= 1
            if self.invincibility_duration <= 0:
                self.is_invincible = False
                self.state = NormalState()
        if not self.has_shield and self.shield_invincibility_duration > 0:
            self.shield_invincibility_duration -= 1
            if self.shield_invincibility_duration <= 0:
                self.state = NormalState()
       
    def activate_invincibility(self, duration):
        self.is_invincible = True
        self.invincibility_duration = duration
        self.state = InvincibilityState(10*FPS)
    
    def activate_shield(self):
        self.has_shield = True
        self.state = ShieldState()

    def use_shield(self):
        self.has_shield = False
        self.shield_invincibility_duration = FPS  # 1 Sekunde Unverwundbarkeit
        self.state = InvincibilityState(FPS)
        self.is_invincible = True
    def draw(self, screen):
        raise NotImplementedError("This method should be implemented in subclasses")
        
    def draw_jetpack_power_ups(self, screen):
        # Logic for drawing jetpack
        if self.booster:
            jetpack_image = self.image_dict["jetpack_on"]
        else:
            jetpack_image = self.image_dict["jetpack_off"]

        screen.blit(jetpack_image, (self.rect.x - self.jetpack_x_offset, self.rect.y + self.jetpack_y_offset))

        # Logic for drawing shield and invincibility power-ups
        if isinstance(self.state, ShieldState):
            hat_position = (self.x , self.rect.y - 10)  # Adjust offsets as needed
            screen.blit(self.image_dict["shield"], hat_position)
        if isinstance(self.state, InvincibilityState):
            inv_position = (self.x - 10, self.rect.y - 10)  # Adjust offsets as needed
            screen.blit(self.image_dict["inv"], inv_position)
    # keep player within the screen 
    def check_colliding(self, decke, boden):
        coll = [False, False]
        if self.rect.colliderect(boden):
            coll[0] = True
        elif self.rect.colliderect(decke):
            coll[1] = True
        return coll
    # coin collection logic
    def collect_coins(self, coins_group):
        collect_coin_sound = pygame.mixer.Sound('sounds/collectcoin.mp3')
        coll_coins = pygame.sprite.spritecollide(self, coins_group, True, pygame.sprite.collide_rect)
        if coll_coins:
            collect_coin_sound.play()
        self.collected_coins += len(coll_coins)
        return len(coll_coins)
    # collision detection
    def RectVsRect(self, rect1, rect2):
        return (rect1.x < rect2.x + rect2.width and
                rect1.x + rect1.width > rect2.x and
                rect1.y < rect2.y + rect2.height and
                rect1.y + rect1.height > rect2.y)


class LuffyPlayer(Player):
    def __init__(self):
        super().__init__()
        for nr in range(1, 9):
            self.image_dict["player_"+str(nr)] = pygame.image.load('luffy pngs/sprite_'+str(nr)+'.png')
            self.image_dict["player_"+str(nr)] = pygame.transform.scale(self.image_dict["player_"+str(nr)], (self.image_width, self.image_height))            
        self.image_dict["player_fly"] = pygame.image.load("luffy pngs/sprite_fly.png")
        self.image_dict["player_fly"] = pygame.transform.scale(self.image_dict["player_fly"], (self.image_width, self.image_height))


    def draw(self, screen):
        if self.rect.y == self.init_y:
            player_image = self.image_dict["player_1"]
        elif self.rect.y < self.init_y:
            player_image = self.image_dict["player_fly"]
        else:
            player_image = self.image_dict[f"player_{(self.counter // 5) + 1}"]
        screen.blit(player_image, (self.rect.x + self.x_offset, self.rect.y + self.y_offset))
        self.draw_jetpack_power_ups(screen)

class NamiPlayer(Player):
    def __init__(self):
        super().__init__()

        for nr in range(1, 9):
            self.image_dict["player_"+str(nr)] = pygame.image.load('nami pngs/sprite_'+str(nr)+'.png')
            self.image_dict["player_"+str(nr)] = pygame.transform.scale(self.image_dict["player_"+str(nr)], (self.image_width, self.image_height))            
        self.image_dict["player_fly"] = pygame.image.load("nami pngs/sprite_fly.png")
        self.image_dict["player_fly"] = pygame.transform.scale(self.image_dict["player_fly"], (self.image_width, self.image_height))

    def draw(self, screen):

        if self.rect.y == self.init_y:
            player_image = self.image_dict["player_1"]
        elif self.rect.y < self.init_y:
            player_image = self.image_dict["player_fly"]
        else:
            player_image = self.image_dict[f"player_{(self.counter // 5) + 1}"]
        screen.blit(player_image, (self.rect.x + self.x_offset, self.rect.y + self.y_offset))
        self.draw_jetpack_power_ups(screen)

class BoaPlayer(Player):
    def __init__(self):
        super().__init__()

        for nr in range(1, 9):
            self.image_dict["player_"+str(nr)] = pygame.image.load('boa pngs/sprite_'+str(nr)+'.png')
            self.image_dict["player_"+str(nr)] = pygame.transform.scale(self.image_dict["player_"+str(nr)], (self.image_width, self.image_height))            
        self.image_dict["player_fly"] = pygame.image.load("boa pngs/sprite_fly.png")
        self.image_dict["player_fly"] = pygame.transform.scale(self.image_dict["player_fly"], (self.image_width, self.image_height))

    def draw(self, screen):
        if self.rect.y == self.init_y:
            player_image = self.image_dict["player_1"]
        elif self.rect.y < self.init_y:
            player_image = self.image_dict["player_fly"]
        else:
            player_image = self.image_dict[f"player_{(self.counter // 5) + 1}"]
        screen.blit(player_image, (self.rect.x + self.x_offset, self.rect.y + self.y_offset))
        self.draw_jetpack_power_ups(screen)

class RobinPlayer(Player):
    def __init__(self):
        super().__init__()
        for nr in range(1, 9):
            self.image_dict["player_"+str(nr)] = pygame.image.load('robin pngs/sprite_'+str(nr)+'.png')
            self.image_dict["player_"+str(nr)] = pygame.transform.scale(self.image_dict["player_"+str(nr)], (self.image_width, self.image_height))            
        self.image_dict["player_fly"] = pygame.image.load("robin pngs/sprite_fly.png")
        self.image_dict["player_fly"] = pygame.transform.scale(self.image_dict["player_fly"], (self.image_width, self.image_height))

    def draw(self, screen):
        if self.rect.y == self.init_y:
            player_image = self.image_dict["player_1"]
        elif self.rect.y < self.init_y:
            player_image = self.image_dict["player_fly"]
        else:
            player_image = self.image_dict[f"player_{(self.counter // 5) + 1}"]
        screen.blit(player_image, (self.rect.x + self.x_offset, self.rect.y + self.y_offset))
        self.draw_jetpack_power_ups(screen) 

class SanjiPlayer(Player):
    def __init__(self):
        super().__init__()
        for nr in range(1, 9):
            self.image_dict["player_"+str(nr)] = pygame.image.load('sanji pngs/sprite_'+str(nr)+'.png')
            self.image_dict["player_"+str(nr)] = pygame.transform.scale(self.image_dict["player_"+str(nr)], (self.image_width, self.image_height))            
        self.image_dict["player_fly"] = pygame.image.load("sanji pngs/sprite_fly.png")
        self.image_dict["player_fly"] = pygame.transform.scale(self.image_dict["player_fly"], (self.image_width, self.image_height))

    def draw(self, screen):
        if self.rect.y == self.init_y:
            player_image = self.image_dict["player_1"]
        elif self.rect.y < self.init_y:
            player_image = self.image_dict["player_fly"]
        else:
            player_image = self.image_dict[f"player_{(self.counter // 5) + 1}"]
        screen.blit(player_image, (self.rect.x + self.x_offset, self.rect.y + self.y_offset))
        self.draw_jetpack_power_ups(screen)

        

class ZoroPlayer(Player):
    def __init__(self):
        super().__init__()

        for nr in range(1, 9):
            self.image_dict["player_"+str(nr)] = pygame.image.load('zoro pngs/sprite_'+str(nr)+'.png')
            self.image_dict["player_"+str(nr)] = pygame.transform.scale(self.image_dict["player_"+str(nr)], (self.image_width, self.image_height))            
        self.image_dict["player_fly"] = pygame.image.load("zoro pngs/sprite_fly.png")
        self.image_dict["player_fly"] = pygame.transform.scale(self.image_dict["player_fly"], (self.image_width, self.image_height))
            

    def draw(self, screen):
        if self.rect.y == self.init_y:
            player_image = self.image_dict["player_1"]
        elif self.rect.y < self.init_y:
            player_image = self.image_dict["player_fly"]
        else:
            player_image = self.image_dict[f"player_{(self.counter // 5) + 1}"]
        screen.blit(player_image, (self.rect.x + self.x_offset, self.rect.y + self.y_offset))
        self.draw_jetpack_power_ups(screen)

        
        


class PlayerFactory:
    def create_player(self, player_type):
        if player_type == "luffy":
            return LuffyPlayer()
        if player_type == "nami":
            return NamiPlayer()
        if player_type == "boa":
            return BoaPlayer()
        if player_type == "robin":
            return RobinPlayer()
        if player_type == "sanji":
            return SanjiPlayer()
        if player_type == "zoro":
            return ZoroPlayer()



class PlayerState: 
    def handle_collision(self, player):
        pass

    def update(self, player):
        pass

class InvincibilityState(PlayerState):
    def __init__(self, duration): # Übergabe von duration, da dieser State auch von Shield verwendet wird (mit nur einer Sekunde)
        self.duration = duration  

    def update(self, player):
        self.duration -= 1 #herunterzählen des Timers
        if self.duration <= 0: #zurück in normalState, wenn Timer abgelaufen
            player.state = NormalState()  
    
    def handle_collision(self, player):
        pass


class ShieldState(PlayerState):
    def handle_collision(self, player):
        if player.has_shield: 
            player.has_shield = False
            player.is_invincible = True
            player.invincibility_duration = FPS  # 1 sec inv
            player.state = InvincibilityState(FPS)
    pass

class NormalState(PlayerState):
    def handle_input(self, player):
            pass