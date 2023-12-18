import pygame
from player import *
from settings import *
from sprites import *
from menu import Menu 
from bg import *

# read current game stats
file = open('game_stats.txt', 'r')
load = file.readlines()
high_score = int(load[0])
lifetime_score = int(load[1])
high_coins = int(load[2])
lifetime_coins = int(load[3])
file.close()


# variables for locking and unlocking characters 
unlock_zoro= False
unlock_robin= False
unlock_sanji= False
unlock_boa= False

# requirments to unlock characters
if high_score >= 10000:
    unlock_zoro = True
if lifetime_score >= 50000:
    unlock_robin = True
if high_coins >= 100:
    unlock_sanji = True
if lifetime_coins >= 500:
    unlock_boa = True

# saving game stats
def save_stats():
    global high_score, lifetime_score,high_coins,lifetime_coins
    if player.score > high_score:
        high_score = player.score
    lifetime_score += player.score
    if player.collected_coins > high_coins:
        high_coins = player.collected_coins
    lifetime_coins += player.collected_coins
    file = open('game_stats.txt', 'w')
    file.write(str(int(high_score)) + '\n')
    file.write(str(int(lifetime_score))+ '\n')
    file.write(str(int(high_coins))+ '\n')
    file.write(str(int(lifetime_coins))+ '\n')
    file.close()

# restarts the game 
def reset_game_state():
    global player,  coin_group, zapper_group, y_velocity, rocket_group,power_up_group,player_factory,player,sprites_group
    player = Player()
    power_up_group = pygame.sprite.Group()
    coin_group = pygame.sprite.Group()
    zapper_group = pygame.sprite.Group()
    rocket_group = pygame.sprite.Group()
    sprites_group= pygame.sprite.Group()
    y_velocity = 0 
    player_factory = PlayerFactory()
    player = player_factory.create_player(player_type)


# py game init
pygame.init()
clock = pygame.time.Clock()

# sound init and sounds imports
pygame.mixer.init()
pygame.mixer.music.load("parallax-industrial-pack/Industrial Theme Music/industrial.wav")
jetpack_sound = pygame.mixer.Sound('sounds/jetpacksound.mp3')
die_sound = pygame.mixer.Sound('sounds/dead.mp3')
shielddrop_sound = pygame.mixer.Sound('sounds/shielddrop.mp3')





# adjust diffuclty 
def adjust_game_speed():
    global game_speed 
    if game_speed <= 10:
        game_speed = 4 + (player.score // 500)/50  
    else:
        game_speed = 10
    
# menu init for game states
menu = Menu(screen)  

# game ending collision
def handle_collision(player, obstacle_group):
    for obstacle in obstacle_group:
        if player.RectVsRect(player.rect, obstacle.hitbox):
            if isinstance(player.state, ShieldState): # wenn der player ein Schild hat, geht dieses nun kaputt
                player.state.handle_collision(player)
                shielddrop_sound.play()
                
            if not player.is_invincible: # wenn player inv, dann passiert nichts
                die_sound.play()
                menu.set_state('END') # player "stirbt"
                menu.update()
                current_score()
                jetpack_sound.stop()
                




def draw_text_with_outline(text, position,font_size, fill_color=(255, 255, 255), outline_color=(58, 188, 230)):
    font = pygame.font.SysFont(pygame.font.get_default_font(), font_size)
    text_surface = font.render(text, True, fill_color)
    outline_surface = font.render(text, True, outline_color)
    outline_offset = 2  
    text_rect = text_surface.get_rect(center=position)
    # Render the outline by blitting the outline_surface around the position
    outline_positions = [
        (position[0] - outline_offset, position[1]),  # Left
        (position[0] + outline_offset, position[1]),  # Right
        (position[0], position[1] - outline_offset),  # Up
        (position[0], position[1] + outline_offset),  # Down
        (position[0] - outline_offset, position[1] - outline_offset),  # Top left
        (position[0] + outline_offset, position[1] - outline_offset),  # Top right
        (position[0] - outline_offset, position[1] + outline_offset),  # Bottom left
        (position[0] + outline_offset, position[1] + outline_offset)   # Bottom right
    ]

    for outline_position in outline_positions:
        outline_rect = outline_surface.get_rect(center=outline_position)
        screen.blit(outline_surface, outline_rect)

   # Render the filled text on top
    screen.blit(text_surface, text_rect)


# draw game stats in menus 
def menu_score():
    draw_text_with_outline(f'highest coins: {round(high_coins)}',(450, 350),36)
    draw_text_with_outline(f'high_score: {round(high_score)}',(450, 400),36)
    draw_text_with_outline(f'coins lifetime: {lifetime_coins}',(700, 350),36)
    draw_text_with_outline(f'score lifetime: {round(lifetime_score)}',(700, 400),36)

# draw current stats in menus 
def current_score():
    draw_text_with_outline(f'coins: {player.collected_coins}',(200, 350),36)
    draw_text_with_outline(f'score: {round(player.score)}',(200 , 400),36)

# draw stats while in run 
def run_score():
    draw_text_with_outline(f'coins: ',(40, 20),30)
    draw_text_with_outline(f'{player.collected_coins}',(100, 20),30)
    draw_text_with_outline(f'score: ',(40, 40),30)
    draw_text_with_outline(f'{round(player.score)}',(100, 40),30)
    draw_text_with_outline(f'high coins:',(60, 60),30)
    draw_text_with_outline(f'{round(high_coins)}',(145, 60),30)
    draw_text_with_outline(f'high score: ',(65, 80),30)
    draw_text_with_outline(f'{round(high_score)}',(155, 80),30)



# init
coin_group = pygame.sprite.Group()
power_up_group = pygame.sprite.Group()
zapper_group = pygame.sprite.Group()
rocket_group = pygame.sprite.Group()
warning_group = pygame.sprite.Group()
sprites_group= pygame.sprite.Group()
player_factory = PlayerFactory()
player_type = None
player = None

# warning needed vars
warning_displayed = False
warning_timer_start = 0
warning_duration = 2000 

# background music
pygame.mixer.music.play(-1)

running = True
while running:
# game state handling 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if menu.state == 'WELCOME':
            menu.update()
            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_RETURN:
                    menu.set_state('PLAYER_SELECTION')
                if event.key == pygame.K_ESCAPE:
                    pygame.quit
        
        # character selection and drawing black and white images if character is locked
        if menu.state == 'PLAYER_SELECTION':
            menu.update()
            if not unlock_zoro: 
                image_zoro = pygame.image.load("zoro pngs/sprite_b.png")
                image_zoro = pygame.transform.scale(image_zoro, (140,200))
                screen.blit(image_zoro, (390,100))
            if not unlock_robin: 
                image_robin = pygame.image.load("robin pngs/sprite_b.png")
                image_robin = pygame.transform.scale(image_robin, (140,200))
                screen.blit(image_robin, (520,100))
            if not unlock_sanji: 
                image_sanji = pygame.image.load("sanji pngs/sprite_b.png")
                image_sanji = pygame.transform.scale(image_sanji, (140,200))
                screen.blit(image_sanji, (650,100))
            if not unlock_boa: 
                image_boa = pygame.image.load("boa pngs/sprite_b.png")
                image_boa = pygame.transform.scale(image_boa, (140,200))
                screen.blit(image_boa, (780,100))

        # Player selection logic
        # if player is locked logic
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    player_type = "luffy"
                    menu.set_state('START')
                elif event.key == pygame.K_2:
                    player_type = "nami"
                    menu.set_state('START')
                elif event.key == pygame.K_3:
                    if unlock_zoro: 
                        player_type = "zoro"
                        menu.set_state('START')
                elif event.key == pygame.K_4:
                    if unlock_robin: 
                        player_type = "robin"
                        menu.set_state('START')
                elif event.key == pygame.K_5:
                    if unlock_sanji: 
                        player_type = "sanji"
                        menu.set_state('START')
                elif event.key == pygame.K_6:
                    if unlock_boa: 
                        player_type = "boa"
                        menu.set_state('START')
                # Create player based on selection
                if player_type:
                    player = player_factory.create_player(player_type)
                if event.key == pygame.K_ESCAPE:
                    menu.set_state('WELCOME')

        if menu.state == 'START':
            menu.update()
            menu_score()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    menu.set_state('RUNNING')
                if event.key == pygame.K_ESCAPE:
                    menu.set_state('PLAYER_SELECTION')

        if menu.state == 'RUNNING':
            # Handle running state events
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu.set_state('PAUSED')
                elif event.key == pygame.K_SPACE:
                    player.booster = True
                    jetpack_sound.play() 
            elif event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                player.booster = False
                jetpack_sound.stop()

        
        if menu.state == 'PAUSED':
            menu.update()
            player.booster = False 
            menu_score()
            current_score()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    menu.set_state('RUNNING')
        
        if menu.state == 'END':
            save_stats()
            menu.update()
            current_score()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    reset_game_state()
                    menu.set_state('START')
                if event.key == pygame.K_ESCAPE:
                    reset_game_state()
                    menu.set_state('PLAYER_SELECTION')                

    
    if menu.state == 'RUNNING' and player :
        # Update game logic
        
        screen.fill((0, 0, 0))
        fugen, decke, boden = drawScreen(fugen)
        player.update()
        power_up_group.draw(screen)
        player.draw(screen)        
        coin_group.draw(screen)
        zapper_group.draw(screen)
        
        # update rocket and fire animation
        for rocket in rocket_group:
            rocket.update(game_speed)
            rocket.fire_animation.update()

        # blitt rocker and fire animation
        for rocket in rocket_group:
            screen.blit(rocket.fire_animation.image, rocket.fire_animation.rect)
            screen.blit(rocket.image, rocket.rect)
        
        
        warning_group.draw(screen)
        warning_group.update()

        # handle collision for each obstacle type 
        handle_collision(player, zapper_group)
        handle_collision(player, rocket_group)

        # stats logic 
        coins_collected = player.collect_coins(coin_group)
        player.score += game_speed 
        if player.score > high_score:
            high_score = player.score
        if player.collected_coins > high_coins:
            high_coins = player.collected_coins
        # draw in run stats
        run_score()
        if player.is_invincible:
            invincibility_timer = round(player.invincibility_duration / FPS, 1)  
            draw_text_with_outline(f'Invincibility: {invincibility_timer}',(85, 100),30)

        # keep player in screen bounds
        colliding = player.check_colliding(decke,boden)

        # Player movement logic
        if player.booster:
            player.y_velocity -= gravity
        else:
            player.y_velocity += gravity
        if (colliding[0] and player.y_velocity > 0) or (colliding[1] and player.y_velocity < 0):
            player.y_velocity = 0
        player.rect.y += player.y_velocity
 
        # Coin spawning logic
        if random.randint(1, 60) == 1:
            new_coin = Coin(WIDTH, random.randint(50, HEIGHT - 50))
            coin_group.add(new_coin)
            sprites_group.add(new_coin)

        # power up collection logic
        for power_up in power_up_group:
            if pygame.sprite.collide_rect(player, power_up):
                power_up.apply_effect()
                power_up_group.remove(power_up)
        # power up spawn logic
        if random.randint(1, 1000) == 1:  
            new_power_up = PowerUp(player)  
            power_up_group.add(new_power_up)
            sprites_group.add(new_power_up)
        # zapper spawn logic
        if len(zapper_group) < 5 : 
            if len(zapper_group) % 2 == 0 : 
                if random.randint(1, 150) == 1:
                    new_zapper = ZapperHiro(WIDTH, random.randint(0, HEIGHT - 40))
                    zapper_group.add(new_zapper)
                    sprites_group.add(new_zapper)
            elif len(zapper_group) % 2 == 1 :
                if random.randint(1, 150) == 1:
                    new_zapper = ZapperVer(WIDTH, random.randint(0, HEIGHT - 255))
                    zapper_group.add(new_zapper)
                    sprites_group.add(new_zapper)

        # warning spawn logic
        if random.randint(1, 400) == 1 and not warning_displayed:
            new_warning = WarningSign(WIDTH - 50, player.rect.y)
            warning_group.add(new_warning)
            warning_timer_start = pygame.time.get_ticks()
            warning_displayed = True
        current_time = pygame.time.get_ticks()
        # rocket spawn logic 
        if warning_displayed and current_time - warning_timer_start > warning_duration:
            for warning in warning_group:
                new_rocket = Rocket(WIDTH, warning.rect.y)
                rocket_group.add(new_rocket)
                warning.kill()
            warning_displayed = False

    	# update sprite 
        for sprite in sprites_group:
            sprite.update(game_speed)
        
        adjust_game_speed()
    
        
    pygame.display.flip()
    clock.tick(FPS)
pygame.mixer.music.stop()
pygame.quit()