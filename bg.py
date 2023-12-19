import pygame
from settings import *


foreground_speed = 0.4  
buildings_speed = 0.2    
far_buildings_speed = 0.1   
fugen = [0, WIDTH / 4, WIDTH / 2, 3 * WIDTH / 4]




def load_and_scale_image(image_path, width):
    image = pygame.image.load(image_path)
    return pygame.transform.scale(image, (width, image.get_height() * WIDTH / image.get_width()))

# Hintergrund laden
background = load_and_scale_image("parallax-industrial-pack/Sprites/bg.png", WIDTH)

# Vordergrundbilder laden und skalieren
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
    global foreground_x, buildings_x, far_buildings_x  , game_speed # Auf die globalen Variablen zugreifen
    screen.blit(background, (0, 0))  # Hintergrund zeichnen

    # Bilder von links nach rechts bewegen und zeichnen
    move_and_draw_image(far_buildings, far_buildings_x, HEIGHT - far_buildings.get_height())
    move_and_draw_image(buildings, buildings_x, HEIGHT - buildings.get_height())
    move_and_draw_image(foreground, foreground_x, HEIGHT - foreground.get_height())

    decke = pygame.draw.rect(screen, 'gray', [0, 0, WIDTH, 10])
    boden = pygame.draw.rect(screen, 'gray', [0, HEIGHT - 20, WIDTH, 40])

    # Aktualisiere die Positionen der Bilder und Fugen
    far_buildings_x -= far_buildings_speed + (game_speed /100)   # Geschwindigkeit für "far-buildings" (angepasst)
    if far_buildings_x <= -WIDTH:
        far_buildings_x = 0

    buildings_x -= buildings_speed + (game_speed /100) # Geschwindigkeit nur für das "buildings"-Bild
    if buildings_x <= -WIDTH:
        buildings_x = 0

    foreground_x -= foreground_speed + (game_speed /100) # Geschwindigkeit für "skill-foreground"
    if foreground_x <= -WIDTH:
        foreground_x = 0

    for i in range(len(fugen_liste)):
        pygame.draw.line(screen, 'black', (fugen_liste[i], 0), (fugen_liste[i], 10), 3)
        pygame.draw.line(screen, 'black', (fugen_liste[i], HEIGHT - 20), (fugen_liste[i], HEIGHT), 3)
        fugen_liste[i] -= game_speed
        if fugen_liste[i] < 0:
            fugen_liste[i] = WIDTH
    return fugen_liste , decke , boden 

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED)
pygame.display.set_caption("Gliding Frenzy")