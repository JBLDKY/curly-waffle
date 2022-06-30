
import pygame
from pygame.locals import *
import sys
from pygame.constants import K_ESCAPE
import pygame.image
import pygame.key
pygame.init()
import math
pygame.font.init()
import random
import pygame.mouse
from futurefunctiondefinitions import talent_select
pause = False

def secondpause():
    global pause
    if pause == True:
            pause = False
    elif pause == False:
        pause = True   
    
    while pause == True: 
        for event in pygame.event.get():
                if event.type == (pygame.KEYDOWN):
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit
                    if event.key == K_p:
                        pause = False
                        break
    pygame.time.delay(100)
    pygame.display.update()