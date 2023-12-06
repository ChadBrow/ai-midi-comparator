# The Pygame UI for the midi comparator
# Chad Brown
# Last updated: 06/12/2023

import pygame
import pygame_gui
import os

TICK = pygame.USEREVENT + 1
GOOD = pygame.USEREVENT + 2
RUSHING = pygame.USEREVENT + 3
DRAGGING = pygame.USEREVENT + 4

class PygameUI():
    def __init__(self, img):
        pygame.init()

        #create our window. We start it full screen
        pygame.display.set_caption('Quick Start')
        self.screen = pygame.display.set_mode((1280, 1024), pygame.FULLSCREEN)
        self.width, self.height = self.screen.get_size()
        self.manager = pygame_gui.UIManager((self.width, self.height))

        #create background
        self.background = pygame.Surface((self.width, self.height))
        self.background.fill(pygame.Color('#000000'))

        #text font
        self.font = pygame.font.Font(None, 32)

        #colors
        self.backgroundColor = (80, 80, 80)

        #labels
        self.beat = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(0.8 * self.width, 0.1 * self.height, 200, 50),
                                                   text="Beat", manager=self.manager)
        self.status = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(0.8 * self.width, 0.3* self.height, 200, 50),
                                                   text="Status: GOOD", manager=self.manager)
        
        #sheet music
        self.musicPage = pygame_gui.elements.UIImage(relative_rect=pygame.Rect(0.1 * self.width, 0.1 * self.height, 0.4 * self.width, 0.8 * self.height),
                                                   image_surface=pygame.image.load(os.path.abspath(img)), 
                                                   manager=self.manager)
        
        #exit button
        self.exitButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(0.8 * self.width, 0.5 * self.height, 200, 50),
                                                   text="Exit", manager=self.manager)

        # background = pygame.Surface((800, 600))
        # background.fill(pygame.Color('#000000'))

        #start threads
        # self.guiLoop()
    
    def quit(self):
        pygame.quit()
    
    def guiLoop(self):
        while(True):
            for event in pygame.event.get():
                if event.type == pygame.QUIT: #check for exit
                    self.quit()
                if event.type == TICK:
                    pass
                self.manager.process_events(event)
            
            # #update all our elements
            # self.screen.blit(self.background, (0, 0))
            # self.manager.update(10)
            # #draw screen
            # self.manager.draw_ui(self.screen)
            # pygame.display.flip()
            
    def tick(self, delta):
        #update all our elements
        self.screen.blit(self.background, (0, 0))
        self.manager.update(10)
        #draw screen
        self.manager.draw_ui(self.screen)
        pygame.display.flip()
        


