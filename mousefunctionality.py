import pygame
import sys
import pygame.mouse

def lmb():
    if pygame.mouse.get_pressed() == (True, False, False):
        return True
def mmb():
    if pygame.mouse.get_pressed() == (False, True, False):
        return True
def rmb():
    if pygame.mouse.get_pressed() == (False, False, True):
        return True
    
def mousepos():# always get mouseposition
    return pygame.mouse.get_pos()