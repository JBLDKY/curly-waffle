## SPRITE CLASSES
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
#my scripts
from game_simplefunctions import *
from game_constants import *


pla_sprite_pos = 0
# CIRCLE STUFF BEGIN
totalDegrees = 360
radius = 250 # Radius as a variable 
xCoords = [] # array of x coordinates
yCoords = [] # array of y coordinates 
angle = 0 # angle in degrees
circle_x_pos = 500 
circle_y_pos = 375
# start_tuple = (xCoords[0], yCoords[0])
def integer_coords(x):
    int_x_c = int(xCoords[x])
    int_y_c = int(yCoords[x])
    return int_x_c, int_y_c

while angle <= totalDegrees: # calculate coordinates for certain amount of angels
    xCoords.append((math.cos(angle)*radius)+circle_x_pos) #multiple by radius because its not a unit circle, then offset by +500 because the circle is not centered around origin
    yCoords.append((math.sin(angle)*radius)+circle_y_pos)
    angle += ((2*math.pi)/totalDegrees) # repeat for certain amount of angels
    #CIRCLE STUFF END
    
    ##SPIRTES 



class her_sprite(pygame.sprite.Sprite):
        def __init__(self, image, pos_x, pos_y):
            super(her_sprite, self).__init__()
            self.image = image
            self.pos_x = pos_x
            self.pos_y = pos_y
            self.rect = self.image.get_rect()
            self.rect.center = [xCoords[self.pos_x], yCoords[self.pos_y]]
        def player_walkpls(self, loc): 
            if pause == False:
                self.pos_x = int(loc + 1)
                self.pos_y = int(loc + 1)
                self.rect.center = [xCoords[self.pos_x], yCoords[self.pos_y]]
class trashmob(pygame.sprite.Sprite):
        def __init__(self,image, pos_x, pos_y):
            super(trashmob,self).__init__()
            self.image = image
            self.pos_x = pos_x
            self.pos_y = pos_y
            self.rect = self.image.get_rect()
            self.rect.center = [xCoords[self.pos_x], xCoords[self.pos_y]]
            self.count = 0
        def spawn(self, loc):
            self.pos_x = loc
            self.pos_y = loc
            self.rect.center = [xCoords[self.pos_x], yCoords[self.pos_y]]
        def spawned(self):
            self.count += 1
        def despawned(self):
            self.count -= 1
        def expand(self):
            self.rect[2] = int(self.rect[2] * 1.5)
            self.rect[3] += int(self.rect[3] * 1.5)
class boss(pygame.sprite.Sprite):
        def __init__(self, image, pos_x, pos_y):
            super(boss, self).__init__()
            self.image = image #draws the image
            self.rect = self.image.get_rect() #draws a rectangle for the image
            self.rect.center = [pos_x, pos_y]
            self.count = 0
        def spawned(self):
            self.count += 1
        def despawned(self):
            self.count -= 1 
class environment(pygame.sprite.Sprite):
        x = 0
        def __init__(self, image, pos_x, pos_y):
            super(environment,self).__init__()
            self.pos_x = pos_x
            self.pos_y = pos_y
            self.image = image
            self.rect = self.image.get_rect() 
            self.rect.center = pos_x, pos_y
        def animate(self, image):
            self.image = image
class attackanimations(pygame.sprite.Sprite):
        def __init__(self, image, pos_x, pos_y):
            super(attackanimations,self).__init__()
            self.pos_x = pos_x
            self.pos_y = pos_y
            self.image = image
            self.rect = self.image.get_rect()
            self.rect.center = [500, 500]
        def animate(self, distance):
            self.pos_x = int(self.pos_x - distance)

## COMBAT CLASSES
class hero():
        health_scaling = 1.2
        attack_scaling = 1.2
        defense_scaling = 1.2
        a_speed_scaling = 0.90
        def __init__(self, health, attack, defense, a_speed, evade, health_regen, exp, exp_required, level, talent_count, available_talent_points):
            self.health = health
            self.max_health = health
            self.attack = attack
            self.defense = defense
            self.a_speed = a_speed
            self.evade = evade
            self.health_regen = health_regen
            self.exp = exp 
            self.exp_required = exp_required
            self.level = level
            self.talent_count = talent_count
            self.available_talent_points = available_talent_points
        def showstats(self):
            return "{} {} {} {} {}".format(self.health, self.attack, self.defense, self.a_speed, self.evade)
        def regenerate_healthpoint(self):
            self.health = int(self.health + 1)
            self.health_regen = int(self.health_regen + 3000)
        def regenerate_tick(self):
            self.health_regen = int(self.health_regen - 50)
        def regenerate_reset(self):self.health_regen = 3000
        def gain_exp(self, amount):
            self.exp = int(self.exp + amount)
        def scale_exp(self):
            self.exp_required = int(self.level * self.level * 1.01) * 250
        def levelup(self):
            if self.exp >= self.exp_required:
                self.level = int(self.level + 1)
                self.exp = 0
                self.scale_exp()
                self.available_talent_points += 0.5
                if self.level == 3:
                    talent_select_screen = True
        # def talentupdate(self, i):
        #     talent_select_screen = False
        #     self.talent_count += 1
        #     print("SUCCES!")
        #     if i == 0:
        #         self.acquire_genocide_talent()
        #     if i == 1:
        #         bigman_talent = True
        #     if i == 2:
        #         counterattack_talent = True
        # def acquire_genocide_talent(self):
        #     self.attack += 0.5
class enemies():
    health_scaling = 1.05
    attack_scaling = 1.05
    defense_scaling = 1.1
    a_speed_scaling = 0.95
    exp_scaling = 2

    def __init__(self, health, attack, defense, a_speed, evade, base_cooldown, killcount, cooldown, name, exp):
        self.health = health
        self.attack = attack
        self.defense = defense
        self.a_speed = a_speed
        self.evade = evade
        self.base_cooldown = base_cooldown
        self.killcount = killcount
        self.cooldown = cooldown
        self.count = 0
        self.max_health = health
        self.name = name
        self.exp = exp

    def prepareforcombat(self):
        self.health = self.max_health
    
    def showstats(self):
        return "{} {} {} {} {}".format(self.health, self.attack, self.defense, self.a_speed, self.evade)

    def showdetailedstats(self):
        detailedstats = "{} {} {} {} {}".format(self.health, self.attack, self.defense, self.a_speed, self.evade)
        array = detailedstats.split()
        return "health:"+array[0]+" "+"attack:"+ array[1]+" "+"defense:"+array[2]+" "+"a_speed:"+array[3]+" "+"evade:"+array[4]
        
    def apply_scaling(self, lc):
        self.health = int(self.health * lc *enemies.health_scaling)
        self.attack = int(self.attack * lc *enemies.attack_scaling)
        self.defense = int(self.defense * lc *enemies.defense_scaling)
        self.a_speed = int(self.a_speed * enemies.a_speed_scaling**lc)
        self.exp = int(self.exp * lc *enemies.exp_scaling)
        print("scaled!")
    def cooldown_tick(self):
        self.base_cooldown = int(self.base_cooldown - 50)
    def cooldown_refresh(self):
        self.base_cooldown = int(self.base_cooldown + self.cooldown)
    def despawned(self):
        self.count -= 1
    def spawned(self):
        self.count += 1

####SPRITE GROUPS #####
##SPRITE GROUPS OUTSIDE MAIN FUNC
testdummy_group = pygame.sprite.Group()
trashmob_group = pygame.sprite.Group()
boss_group = pygame.sprite.Group()
environment_group = pygame.sprite.GroupSingle()
attackanimations_group = pygame.sprite.Group()

###CALL INSTANCES
    ###PLAYER
pla_all = (player_health, player_attack, player_defense, player_a_speed, player_evade, health_regen, player_exp, player_exp_required, player_level, player_talent_count, player_available_talent_points)
player_info = hero(pla_all[0], pla_all[1], pla_all[2], pla_all[3], pla_all[4], pla_all[5], pla_all[6], pla_all[7], pla_all[8], pla_all[9], pla_all[10])
pla_img = pygame.image.load('player.png').convert_alpha()
pla_sprite = her_sprite(pla_img, 0, 0)
pla_group = pygame.sprite.Group()
pla_group.add(pla_sprite)

    ###TESTDUMMY
testdummy = enemies(test_all[0], test_all[1], test_all[2], test_all[3], test_all[4], test_all[5], test_all[6], test_all[7], test_all[8], test_all[9])
    ###CANDLE
candle1 = enemies(can_all[0], can_all[1], can_all[2], can_all[3], can_all[4], can_all[5], can_all[6], can_all[7], can_all[8], can_all[9])
    ###SKELARMY
skelarmy1 = enemies(ske_all[0], ske_all[1], ske_all[2], ske_all[3], ske_all[4], ske_all[5], ske_all[6], ske_all[7], ske_all[8], ske_all[9])

###SPRITE CALLS
ske_sprite = trashmob(img_skelarmy, int(xCoords[getRandomInt(0, 360)]),int(yCoords[getRandomInt(0, 360)]))
can_sprite = trashmob(img_candle, int(xCoords[getRandomInt(0, 360)]), int(yCoords[getRandomInt(0, 360)]))
test_sprite = trashmob(img_testdummy, int(xCoords[10]), int(yCoords[10]))
trashmob_group.empty()


### INITIAL SPRITE INITIATION
def initial_call_and_delete():        
    ske_sprite = trashmob(img_skelarmy, int(xCoords[getRandomInt(0, 360)]),int(yCoords[getRandomInt(0, 360)]))
    can_sprite = trashmob(img_candle, int(xCoords[getRandomInt(0, 360)]), int(yCoords[getRandomInt(0, 360)]))
    test_sprite = trashmob(img_testdummy, int(xCoords[10]), int(yCoords[10]))
    trashmob_group.empty()
    ##player
    pla_sprite = her_sprite(pla_img, 0, 0)   
    pla_group.add(pla_sprite)

#PAUSE GAME
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
        
#####
for event in pygame.event.get():
            if event.type == (pygame.KEYDOWN):
                if event.key == pygame.K_p:
                    pausegame()

#MOOVEMENEEMT
pla_sprite_pos = increase_int(pla_sprite_pos, 0, 360) #pla_sprite_pos = 0, increase int adds 1 and reset it to 0 if its 360
pla_sprite.player_walkpls(increase_int(pla_sprite_pos, 0, 360)) #updates the instance to go to set location to next point on circle

#SPAWNLOGIC
#### SPAWNLOGIC
def spawn_testdummy():
    _ = 120
    testdummy_group.add(test_sprite) 
    testdummy_group.draw(screen)
    test_sprite.spawn(_)
    test_sprite.spawned()
def spawn_candle():
    _ = random.randint(1, 360)
    trashmob_group.add(can_sprite)
    can_sprite.spawn(_)
    can_sprite.spawned()
def spawn_skelarmy():
    _ = random.randint(1, 360)
    trashmob_group.add(ske_sprite)
    ske_sprite.spawn(_)
    ske_sprite.spawned()
def spawn_kella():
    _ = random.randint(1, 360)
    img_kella = pygame.image.load("Kella.png").convert_alpha()
    kel_sprite = boss(img_kella, 200, 200)
    boss_group.add(kel_sprite)
    kel_sprite.spawned()
def drawSprite():
    trashmob_group.draw(screen)
    boss_group.draw(screen)
    pla_group.draw(screen)
    testdummy_group.draw(screen)

# #RNG BEGIN
def getRandomInt(a, b):
    c = random.randint(a, b)
    return c
# # RNG END
##INT INCREASER
def increase_int(x, a, b):
    if x == b:
        x = a
    x += 1
    return x
def mousepos():# always get mouseposition
    return pygame.mouse.get_pos()

lmb = False
mmb = False
rmb = False
def mousebuttonpressed():
    if pygame.mouse.get_pressed() == (True, False, False):
        return lmb 
    if pygame.mouse.get_pressed() == (False, True, False):
        return mmb 
    if pygame.mouse.get_pressed() == (False, False, True):
        return rmb 

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
def displaymylevels():
    displaynumber("exp", "", player_info.exp, "yellow", 15, 850, 25)
    displaynumber("level", "level:", player_info.level, "yellow",15, 960, 40) 
    displaynumber("exp_req", "/", player_info.exp_required, "yellow", 15, 930, 25)
    displaynumber("detailedstats", "skelarmy1:", skelarmy1.showdetailedstats(), "white", 15, 1, 600)
    displaynumber("detailedstats", "candle1:", candle1.showdetailedstats(), "white", 15, 1, 615)
    
    displaynumber("trashmob", "", trashmob_group, "red", 15, 1, 585)
    displaynumber("pla_sprite", "", pla_sprite, "red", 15, 1, 570)
    print("fuckoff")            
def speed_up():
    global time
    time = time * 2
def speed_down():
    global time
    time = time / 2

# def enemyselect():
# ##TESTDUMMY################################
#     collidelist_testdummy = pygame.sprite.spritecollide(pla_sprite, testdummy_group, False)
#     collidelist_trash = pygame.sprite.spritecollide(pla_sprite, trashmob_group, False)

#     if test_sprite in collidelist_testdummy:
#         return [testdummy, test_sprite, testdummy_group]
#         ## END TESTDUMMY #########
        
#         ##TRASHMOBS##########################
#     if ske_sprite in collidelist_trash:
#         return [skelarmy1, ske_sprite, trashmob_group]
#     if can_sprite in collidelist_trash:
#         return [candle1, can_sprite, trashmob_group]
                    
    
    
    
    
##################CONSTANTS##########################
##################CONSTANTS##########################
##################CONSTANTS##########################
##################CONSTANTS##########################
##################CONSTANTS##########################
##################CONSTANTS##########################
pla_sprite_pos = 0
test_font = pygame.font.Font("C:\WINDOWS\Fonts\cambriab.ttf", 50)
screen = pygame.display.set_mode((1024, 680))
color = (255, 0, 0)

background = pygame.image.load("roguebgbig.png").convert_alpha()
battlebg = pygame.image.load("battlebg.png").convert_alpha()
# p_pos_v = 0
zero = 0
loop_start = True

#PLAYERSPRITE???#
# pla_sprite_pos = 0
pla_img = pygame.image.load('player.png').convert_alpha()
pla_group = pygame.sprite.Group()


#GAME INFORMATION
battletime = 50
# time = 100


####CIRCLE STUFF
pla_sprite_pos = 0
# CIRCLE STUFF BEGIN
totalDegrees = 360
radius = 250 # Radius as a variable 
xCoords = [] # array of x coordinates
yCoords = [] # array of y coordinates 
angle = 0 # angle in degrees
circle_x_pos = 500 
circle_y_pos = 375
# start_tuple = (xCoords[0], yCoords[0])
# def integer_coords(x):
#     int_x_c = int(xCoords[x])
#     int_y_c = int(yCoords[x])
#     return int_x_c, int_y_c

while angle <= totalDegrees: # calculate coordinates for certain amount of angels
    xCoords.append((math.cos(angle)*radius)+circle_x_pos) #multiple by radius because its not a unit circle, then offset by +500 because the circle is not centered around origin
    yCoords.append((math.sin(angle)*radius)+circle_y_pos)
    angle += ((2*math.pi)/totalDegrees) # repeat for certain amount of angels
    #CIRCLE STUFF END
    

######PLAYER INFORMATION
#preset for fetchgin: player(pla_all[0], pla_all[1], pla_all[2], pla_all[3], pla_all[4], pla_all[5])

player_health = 200
player_attack = 20
player_defense = 15
player_a_speed = 1000
player_evade = 6
health_regen = 3000
player_exp = 0
player_exp_required = 50
player_level = 1
player_talent_count = 0
player_available_talent_points = 0
pla_all = (player_health, player_attack, player_defense, player_a_speed, player_evade, health_regen, player_exp, player_exp_required, player_level, player_talent_count, player_available_talent_points)
# player_info = hero(pla_all[0], pla_all[1], pla_all[2], pla_all[3], pla_all[4], pla_all[5], pla_all[6], pla_all[7], pla_all[8], pla_all[9], pla_all[10])
# def talent_selector():
# if player_info.level > 1:
#     plswork = 1
    
###talent
bigman_talent = False
genocide_talent = False
counterattack_talent = False

### END PLAYER INFORMATION

#TEST DUMMY FOR TESTING I GUESS
testdummy_count = 0
testdummy_health = 10000
testdummy_attack = 1
testdummy_defense = 0
testdummy_a_speed = 3000
testdummy_evade = 4
testdummy_cooldown = 5000
testdummy_base_cooldown = 3000
testdummy_killcount = 0
testdummy_name = "testdummy"
testdummy_exp = 1000
test_all = (testdummy_health, testdummy_attack, testdummy_defense, testdummy_a_speed, testdummy_evade, testdummy_base_cooldown, testdummy_killcount, testdummy_cooldown, testdummy_name, testdummy_exp)
# testdummy = enemies(test_all[0], test_all[1], test_all[2], test_all[3], test_all[4], test_all[5], test_all[6], test_all[7], test_all[8], test_all[9])
testdummy_spawn = False
alitestdummy_e = False
testdummy_killcount = 0
prev_candle_killcount = 0

#CANDLE ENEMY INFORMATION#
candle_count = 0
candle_health = 100
candle_attack = 3
candle_defense = 2
candle_a_speed = 2000
candle_evade = 4
candle_cooldown = 5000
candle_base_cooldown = 3000
candle_killcount = 0
candle_name = "candle"
candle_exp = 100
can_all = (candle_health, candle_attack, candle_defense, candle_a_speed, candle_evade, candle_base_cooldown, candle_killcount, candle_cooldown, candle_name, candle_exp)
# candle1 = enemies(can_all[0], can_all[1], can_all[2], can_all[3], can_all[4], can_all[5], can_all[6], can_all[7], can_all[8], can_all[9])
candlespawn = False
candle_alive = False
candle_killcount = 0
prev_candle_killcount = 0
e_CandleB = pygame.image.load("candleB.png").convert_alpha()
candle_rect = e_CandleB.get_rect(center = (1400, 0))

#SKELARMY ENEMY INFORMATION
skelarmy_count = 0
skelarmy_health = 120
skelarmy_attack = 9
skelarmy_defense = 4
skelarmy_a_speed = 2500
skelarmy_evade = 4
skelarmy_cooldown = 3000
skelarmy_base_cooldown = 15000
skelarmy_killcount = 0
skelarmy_name = "skelarmy"
skelarmy_exp = 150
ske_all = (skelarmy_health, skelarmy_attack, skelarmy_defense, skelarmy_a_speed, skelarmy_evade, skelarmy_base_cooldown, skelarmy_killcount, skelarmy_cooldown, skelarmy_name, skelarmy_exp)
skelarmyspawn = False
skelarmy_alive = False
prev_skelarmy_killcount = 0
# skelarmy1 = enemies(ske_all[0], ske_all[1], ske_all[2], ske_all[3], ske_all[4], ske_all[5], ske_all[6], ske_all[7], ske_all[8], ske_all[9])
img_skelarmy = pygame.image.load("skellarmy.png").convert_alpha()

####IMPORTANT FUCKING VARIABLES
loopcount = 0
time = 250

####IMAGES FOR STATIC 
img_topmenu = pygame.image.load("topmenubar.png").convert_alpha()
####END IMAGES FOR STATIC
###IMAGES FOR TALENTS
img_talent_genocide = pygame.image.load("talent_genocide.png")
img_talent_bigman = pygame.image.load("talent_bigman.png")
img_talent_counterattack = pygame.image.load("talent_counterattack.png")
img_talent_array = [img_talent_genocide, img_talent_bigman, img_talent_counterattack] # array of talent IMAGES
img_talent_array_id = [img_talent_genocide, img_talent_bigman, img_talent_counterattack] # array of talent IMAGES
####END IMAGES FOR STATIS
##ANIMATION FUNCTIONS #################################
animation_start_x = 768
animation_start_y = 360
iterations = 0

##LOAD ENEMY ASSETS
img_candle = pygame.image.load("candleB.png").convert_alpha()
img_skelarmy = pygame.image.load("skellarmy.png").convert_alpha()
img_testdummy = pygame.image.load("testdummy.png").convert_alpha()

##ANIMATION PICTURES
img_campfire1 = pygame.image.load("campfire1.png").convert_alpha()
img_campfire2 = pygame.image.load("campfire2.png").convert_alpha()
img_campfire3 = pygame.image.load("campfire3.png").convert_alpha()
img_campfire4 = pygame.image.load("campfire4.png").convert_alpha()
campfire_animations = [img_campfire1, img_campfire2, img_campfire3, img_campfire4]
img_bluefireball1 = pygame.image.load("bluefireball1.png").convert_alpha()
img_bluefireball2 = pygame.image.load("bluefireball2.png").convert_alpha()
img_bluefireball3 = pygame.image.load("bluefireball3.png").convert_alpha()
img_bluefireball4 = pygame.image.load("bluefireball4.png").convert_alpha()
bluefireball_animations = [img_bluefireball1, img_bluefireball2, img_bluefireball3, img_bluefireball4]
bluefireball_index = 0
bluefireball_surf = bluefireball_animations[bluefireball_index]

###TALENT MENU#################
# talent_menu_button_rect_pressed = False
img_talent_menu_button_static = pygame.image.load("talentmenubuttonstatic.png")
img_talent_menu_button_hovered = pygame.image.load("talentmenubuttonhovered.png")
img_talent_menu_button_pressed = pygame.image.load("talentmenubuttonpressed.png")
# img_talent_menu_button_array = [img_talent_menu_button_static, img_talent_menu_button_hovered, img_talent_menu_button_pressed]
talent_menu_button_rect = img_talent_menu_button_static.get_rect(midright = (635, 40))




def integer_coords(x):
    int_x_c = int(xCoords[x])
    int_y_c = int(yCoords[x])
    return int_x_c, int_y_c