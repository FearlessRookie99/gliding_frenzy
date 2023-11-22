import pygame
from player import Player
from settings import *
from sprites import *




# Der Rest des Codes bleibt unverändert
foreground_speed = 0.4
buildings_speed = 0.2
far_buildings_speed = 0.1
fugen = [0, WIDTH / 4, WIDTH / 2, 3 * WIDTH / 4]
foreground_speed = 0.4  # Geschwindigkeit für "skill-foreground"
buildings_speed = 0.2    # Geschwindigkeit für "buildings"
far_buildings_speed = 0.1  # Geschwindigkeit für "far-buildings" (angepasst)
fugen = [0, WIDTH / 4, WIDTH / 2, 3 * WIDTH / 4]
# Bildschirm initialisieren
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED)
pygame.display.set_caption("Prog2")

clock = pygame.time.Clock()

def load_and_scale_image(image_path, width):
    image = pygame.image.load(image_path)
    return pygame.transform.scale(image, (width, image.get_height() * WIDTH / image.get_width()))

# Hintergrund laden
background = load_and_scale_image("parallax-industrial-pack/Sprites/bg.png", WIDTH)

# Vordergrundbilder laden und skalieren
background_images =["foreground", "buildings", "far_buildings"]

foreground = load_and_scale_image("parallax-industrial-pack/Sprites/foreground.png", WIDTH)
buildings = load_and_scale_image("parallax-industrial-pack/Sprites/buildings.png", WIDTH)
far_buildings = load_and_scale_image("parallax-industrial-pack/Sprites/far_buildings.png", WIDTH)

# Positionen der Bilder
foreground_x = 0
buildings_x = 0
far_buildings_x = 0
def move_and_draw_image(image, x, y):
    screen.blit(image, (x, HEIGHT - image.get_height()))
    screen.blit(image, (x + WIDTH, HEIGHT - image.get_height()))

# Endlos Boden und Decke bewegen
def drawScreen(fugen_liste):
    global foreground_x, buildings_x, far_buildings_x  # Auf die globalen Variablen zugreifen
    screen.blit(background, (0, 0))  # Hintergrund zeichnen

    # Bilder von links nach rechts bewegen und zeichnen
    move_and_draw_image(far_buildings, far_buildings_x, HEIGHT - far_buildings.get_height())
    move_and_draw_image(buildings, buildings_x, HEIGHT - buildings.get_height())
    move_and_draw_image(foreground, foreground_x, HEIGHT - foreground.get_height())

    decke = pygame.draw.rect(screen, 'gray', [0, 0, WIDTH, 10])
    boden = pygame.draw.rect(screen, 'gray', [0, HEIGHT - 20, WIDTH, 40])

    # Aktualisiere die Positionen der Bilder und Fugen
    far_buildings_x -= far_buildings_speed  # Geschwindigkeit für "far-buildings" (angepasst)
    if far_buildings_x <= -WIDTH:
        far_buildings_x = 0

    buildings_x -= buildings_speed  # Geschwindigkeit nur für das "buildings"-Bild
    if buildings_x <= -WIDTH:
        buildings_x = 0

    foreground_x -= foreground_speed  # Geschwindigkeit für "skill-foreground"
    if foreground_x <= -WIDTH:
        foreground_x = 0

    for i in range(len(fugen_liste)):
        pygame.draw.line(screen, 'black', (fugen_liste[i], 0), (fugen_liste[i], 10), 3)
        pygame.draw.line(screen, 'black', (fugen_liste[i], HEIGHT - 20), (fugen_liste[i], HEIGHT), 3)
        fugen_liste[i] -= game_speed
        if fugen_liste[i] < 0:
            fugen_liste[i] = WIDTH
    return fugen_liste , decke , boden 
# Einstellungen


# Bildschirm initialisieren
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED)
pygame.display.set_caption("Gliding Frenzy")

clock = pygame.time.Clock()

# Der Rest des Codes bleibt unverändert

# Hier sollten die globalen Variablen und Initialisierungen folgen

pygame.init()
pygame.mixer.init()

# game settings und initialisierende Variablen

distance = 0
y_velocity = 0

# Bildschirm initialisieren
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED)
pygame.display.set_caption("Prog2")

clock = pygame.time.Clock()


coin_group = pygame.sprite.Group()

# Spieler initialisieren
player = Player()

# In der Schleife können Sie jetzt die Hintergrund- und Spieler-Objekte verwenden
running = True
pause = False
while running:
    dt = clock.tick(FPS) / 1000

    # Hintergrund zeichnen
    fugen, decke, boden = drawScreen(fugen)
   
    # Spieler zeichnen
    
    clock.tick(FPS)
    if player.counter < 40:
        player.counter += 1
    else:
        player.counter = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if pause:
                    pause = False
                else:
                    pause = True
            if event.key == pygame.K_SPACE and not pause:
                player.booster = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                player.booster = False
    if random.randint(1, 60) == 1:  ## Münzen erscheinen in zufälligen Abständen
        new_coin = Coin(WIDTH, random.randint(50, HEIGHT - 50))
        coin_group.add(new_coin)

        # Hier entstehen die Münzen
    coin_group.update()
    coin_group.draw(screen)
    
    player.player = player.draw(screen)
    

    colliding = player.check_colliding(decke,boden)
    pygame.display.flip()

    if not pause:
        distance += game_speed
        if player.booster:
            y_velocity -= gravity
        else:
            y_velocity += gravity
        if (colliding[0] and y_velocity > 0) or (colliding[1] and y_velocity < 0):
            y_velocity = 0
        player.player_y += y_velocity


# Aufräumen und Spiel beenden
pygame.quit()
