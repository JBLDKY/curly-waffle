import pygame
from pygame.locals import *
import sys
import pygame.image
import pygame.key
pygame.init()
import math
pygame.font.init()
import random
import pygame.mouse
#myscripts
from game_Constants import *

# #SIMPLE FUNCTIONS
# # 
# # 
# # 
# # #RNG BEGIN
def getRandomInt(a, b):
    return random.randint(a, b)
    
# # RNG END
##INT INCREASER
# def increase_int(x, a, b):
#     x += 1
#     if x == b:
#         x = a
#     return x


def mousepos():# always get mouseposition
    return pygame.mouse.get_pos()
def integer_coords(x):
    int_x_c = int(xCoords[x])
    int_y_c = int(yCoords[x])
    return int_x_c, int_y_c

v_lmb = False
v_mmb = False
v_rmb = False
def mousebuttonpressed():
    if pygame.mouse.get_pressed() == (True, False, False):
        return v_lmb 
    if pygame.mouse.get_pressed() == (False, True, False):
        return v_mmb 
    if pygame.mouse.get_pressed() == (False, False, True):
        return v_rmb 

###PAUSE GAME################

pause = False
def pausegame():
    global pause
    if pause == True:
        pause = False
        print("game paused")   
    elif pause == False:
        pause = True
        print("game unpaused")
        
def enemy_attack_animation(a_speed, e_atk):
    #bluefirebalx
    global bluefireball_index, bluefireball_surf, animation_start_y, animation_start_x, iterations #global variables yay
        
    bluefireball_index += 0.2 # EVERYTIME FUNCTION RUNS, INCREASE INDEX BY .2
    if bluefireball_index >= len(bluefireball_animations):bluefireball_index = 0 #RESET INDEX TO 0 AT THE END OF UR LOOP
    bluefireball_surf = bluefireball_animations[int(bluefireball_index)] #bluefireball_surf calls the updated image
    bluefireball_rect = bluefireball_surf.get_rect(center = (animation_start_x, animation_start_y))
    screen.blit(bluefireball_surf, bluefireball_rect)
    animation_start_x -= 11
def reset_enemy_attack_animation(pos):
    global animation_start_x
    animation_start_x = 768
    
    
#### SPAWNLOGIC


###BLIT TEXT AND INTS
def displaynumber(name, prefix, text, color, size, x, y):
            apply_size = pygame.font.Font("C:\WINDOWS\Fonts\cambriab.ttf", size) #picks the font and the size, only the size is variable
            str_text = prefix + str(text)   #stringifies the integer
            rendered_text = apply_size.render(str_text, False, color) #converts text to image
            name = rendered_text.get_rect(midleft = (x, y)) #assign the text a rectangle in variable "name"
            screen.blit(rendered_text, name)    #place image on screen
def displaynumbercenter(name, prefix, text, color, size, x, y):
            apply_size = pygame.font.Font("C:\WINDOWS\Fonts\cambriab.ttf", size) #picks the font and the size, only the size is variable
            str_text = prefix + str(text)   #stringifies the integer
            rendered_text = apply_size.render(str_text, False, color) #converts text to image
            name = rendered_text.get_rect(center = (x, y)) #assign the text a rectangle in variable "name"
            screen.blit(rendered_text, name)    #place image on screen
def displaynumberright(name, prefix, text, color, size, x, y):
            apply_size = pygame.font.Font("C:\WINDOWS\Fonts\cambriab.ttf", size) #picks the font and the size, only the size is variable
            str_text = prefix + str(text)   #stringifies the integer
            rendered_text = apply_size.render(str_text, False, color) #converts text to image
            name = rendered_text.get_rect(midright = (x, y)) #assign the text a rectangle in variable "name"
            screen.blit(rendered_text, name)    #place image on screen
            
# def displaymylevels():
#     displaynumber("exp", "", player_info.exp, "yellow", 15, 850, 25)
#     displaynumber("level", "level:", player_info.level, "yellow",15, 960, 40) 
#     displaynumber("exp_req", "/", player_info.exp_required, "yellow", 15, 930, 25)
#     displaynumber("detailedstats", "skelarmy1:", skelarmy1.showdetailedstats(), "white", 15, 1, 600)
#     displaynumber("detailedstats", "candle1:", candle1.showdetailedstats(), "white", 15, 1, 615)
    
#     displaynumber("trashmob", "", trashmob_group, "red", 15, 1, 585)
#     displaynumber("pla_sprite", "", pla_sprite, "red", 15, 1, 570)
#     print("fuckoff")            
            
def speed_up():
    global time
    time = time * 2
def speed_down():
    global time
    time = time / 2