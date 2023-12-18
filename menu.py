import pygame


class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.font = None
        self.running = True
        self.state = 'WELCOME'

    def draw_text_with_outline(self, text, position,font_size, fill_color=(255, 255, 255), outline_color=(58, 188, 230)):
        self.font = pygame.font.SysFont(pygame.font.get_default_font(), font_size)
        text_surface = self.font.render(text, True, fill_color)
        outline_surface = self.font.render(text, True, outline_color)

        outline_offset = 2  # Adjust the outline offset as needed
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
            self.screen.blit(outline_surface, outline_rect)

        # Render the filled text on top
        self.screen.blit(text_surface, text_rect)
    
    

    
    def welcome_menu(self):
        self.screen.fill((0, 0, 0))
        
        
        self.image_title = pygame.image.load("menu pngs/title.png")
        self.image_title = pygame.transform.scale(self.image_title, (self.screen.get_width(), self.screen.get_height()))
        self.rect = self.image_title.get_rect()
        self.screen.blit(self.image_title, (self.rect.x , self.rect.y ))
        self.image_fh = pygame.image.load("menu pngs/fh.png")
        self.image_fh = pygame.transform.scale(self.image_fh, (200, 50))
        self.screen.blit(self.image_fh, ( self.screen.get_width() - 201 , self.screen.get_height() - 51 ))

        self.draw_text_with_outline("Press Enter to continue",  (self.screen.get_width() / 2 - 18, self.screen.get_height() / 2 + 150),30 )
        self.draw_text_with_outline("Press ESC to exit game", (100, 15),24 )       
        
        self.draw_text_with_outline("Developed by Taher Garada , Wares Aram , Martin Krawtzow , Al Farouk Ali",(225,self.screen.get_height() / 2 + 260 ),18)
        self.draw_text_with_outline("Mentored by Prof. Dr. Christian Krauss ",(120,self.screen.get_height() / 2 + 280 ),18)
    
    
    def player_selection(self):
        
        image_size = (140,200)
        self.screen.fill((127, 205, 230))
        self.image_1 = pygame.image.load("luffy pngs/sprite_4.png")
        self.image_1 = pygame.transform.scale(self.image_1, image_size)
        self.screen.blit(self.image_1, (130,100))
        self.draw_text_with_outline("1: Luffy",(200,self.screen.get_height() / 2 ),24)

        self.image_2 = pygame.image.load("nami pngs/sprite_4.png")
        self.image_2 = pygame.transform.scale(self.image_2, image_size)
        self.screen.blit(self.image_2, (260,100))
        self.draw_text_with_outline("2: Nami",(330,self.screen.get_height() / 2 ),24)

        self.image_3 = pygame.image.load("zoro pngs/sprite_4.png")
        self.image_3 = pygame.transform.scale(self.image_3, image_size)
        self.screen.blit(self.image_3, (390,100))
        self.draw_text_with_outline("3: Zoro",(460,self.screen.get_height() / 2 ),24)
        self.draw_text_with_outline("highscore 10.000",(460,90),20)

        self.image_4 = pygame.image.load("robin pngs/sprite_4.png")
        self.image_4 = pygame.transform.scale(self.image_4, image_size)
        self.screen.blit(self.image_4, (520,100))
        self.draw_text_with_outline("4: Robin",(590,self.screen.get_height() / 2 ),24)
        self.draw_text_with_outline("Lifetime Score 50.000",(590,90),20)

        self.image_5 = pygame.image.load("sanji pngs/sprite_4.png")
        self.image_5 = pygame.transform.scale(self.image_5, image_size)
        self.screen.blit(self.image_5, (650,100))
        self.draw_text_with_outline("5: Sanji",(715,self.screen.get_height() / 2 ),24)
        self.draw_text_with_outline("high coins 100",(715,90 ),20)

        self.image_6 = pygame.image.load("boa pngs/sprite_4.png")
        self.image_6 = pygame.transform.scale(self.image_6, image_size)
        self.screen.blit(self.image_6, (780,100))
        self.draw_text_with_outline("6: Boa",(850,self.screen.get_height() / 2 ),24)
        self.draw_text_with_outline("Lifetime coins 500",(850,90 ),20)

        self.draw_text_with_outline("Press number of character to select", (self.screen.get_width() / 2, self.screen.get_height() / 2 + 60), 24)
        self.draw_text_with_outline("Press ESC to go to home screen", (140, 15),25 ) 
    
    
    def start_menu(self):
        self.screen.fill((127, 205, 230))
        self.draw_text_with_outline("Press Enter to start", (self.screen.get_width() / 2, self.screen.get_height() / 2),40)
        self.draw_text_with_outline("Press ESC to go to character selection", (170, 15),25 ) 


    def pause_menu(self):
        overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA)        
        overlay.fill((127, 205, 230, 50))  # The last number (128) is the alpha value

        # Blit the semi-transparent surface onto the screen
        self.screen.blit(overlay, (0, 0))

        # Now draw the pause menu text
        self.draw_text_with_outline("Paused - Press Space to continue", (self.screen.get_width() / 2, self.screen.get_height() / 2),40)
        
    def end_menu(self):
        self.screen.fill((127, 205, 230))
        self.draw_text_with_outline("Game Over - Press Enter to restart", (self.screen.get_width() / 2, self.screen.get_height() / 2),40)
        self.draw_text_with_outline("Press ESC to go to character selection", (170, 15),24 ) 
    

    def update(self):
        if self.state == 'START':
            self.start_menu()
        elif self.state == 'PAUSED':
            self.pause_menu()
        elif self.state == 'END':
            self.end_menu()
        elif self.state == 'PLAYER_SELECTION':
            self.player_selection()
        elif self.state == 'WELCOME':
            self.welcome_menu()


    def set_state(self, state):
        self.state = state
