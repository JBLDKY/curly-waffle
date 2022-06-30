
from os import X_OK
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
from game_Cardsystem import *
from mousefunctionality import *
from game_Constants import *
from futurefunctiondefinitions import talent_select, talent_selected
from game_pause import secondpause
from game_Lootsystem import *
from collections import Counter
from game_Proper_A_Star import get_path
# import collections

#maybe make a class for the circle relations
###fix inventory list toolltip$#$$
#classes
clock = pygame.time.Clock()
fps = 60
time = 13
start_point = None
inv_index = None
dontspamequips = 0
# equipped_yn = [weapon_equipped, chest_equipped, shield_equipped, helm_equipped, ring_equipped]
loopcount = 0
## SPRITE CLASSES
######### HERO
class her_sprite(pygame.sprite.Sprite):
        def __init__(self, image, pos_x, pos_y):
            super(her_sprite, self).__init__()
            self.image = image
            self.pos_x = pos_x
            self.pos_y = pos_y
            self.tuple = [pos_y, pos_x]
            self.rect = self.image.get_rect()
            self.rect.center = [xCoords[self.pos_x], yCoords[self.pos_y]]
        def player_walkpls(self, loc): 
            global loopcount
            if pause == False:
                # print(walking_coords_list[loc])
                # print(self.rect.center)
                self.rect.center = (walking_coords_list[loc])
                self.tuple = walking_coords_list[loc]
            else: print("paused")    
            if self.tuple == walking_coords_list[-1]:
                loopcount += 1
            
######### ITEMS TO EQUIP            
class equips(pygame.sprite.Sprite):
    def __init__(self, img, equiptype, x, y, bool):
        (super, equips).__init__()
        self.img = img
        self.equiptype = equiptype
        self.x = x
        self.y = y
        self.bool = bool
            
######## TRASHMOBS
class trashmob(pygame.sprite.Sprite):
        def __init__(self,imagelist, pos_x, pos_y, dupe_tr):
            super(trashmob,self).__init__()
            self.multi_combat = 1
            self.image = imagelist[self.multi_combat-1]
            self.image_list = imagelist
            self.pos_x = pos_x
            self.pos_y = pos_y
            self.dupe = 0
            self.dupe_tr = dupe_tr
            self.rect = self.image.get_rect()
            self.rect.center = [xCoords[self.pos_x], xCoords[self.pos_y]]
            self.count = 0
            self.spawn_loc = None
        def spawn(self, loc):
            possible_spawn_locs = []
            for x in path_detect_list:
                if x.monster == None and x.spawntype == "any":
                    possible_spawn_locs.append(x)
                    x.monster == "taken"
                    self.spawn_loc = x
            self.spawn_loc = random.choice(possible_spawn_locs)
            self.rect.center = self.spawn_loc.rect.center
        
        def spawned(self):
            self.count += 1
        def despawned(self):
            self.count -= 1
            if self.spawn_loc in path_detect_list:
                self.spawn_loc.monster = None
        # def expand(self):
            # self.rect[2] = int(self.rect[2] * 1.5)
            # self.rect[3] += int(self.rect[3] * 1.5)
        def duplicate(self):
            if self.count > 0:
                self.dupe += time
            if self.dupe > self.dupe_tr:
                self.dupe = 0
                if self.multi_combat < 4:
                    self.multi_combat += 1
                    self.image = self.image_list[self.multi_combat-1]
                self.rect.center = self.spawn_loc.rect.center
######## BOSSES
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
        def set_loc(self, start_point):
            self.rect.center = start_point.rect.center
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
            self.stun = 1
            self.counter = 1
            self.spikes = 1
            self.taunt = 1
            self.crit = 1
            self.crit_damage = 1
            self.lifesteal = 1
            self.block = 1
            
        def showstats(self):
            return "{} {} {} {} {}".format(self.health, self.attack, self.defense, self.a_speed, self.evade, self.stun, self.lifesteal)
        def regenerate_healthpoint(self):
            self.health = int(self.health + 1)
            self.health_regen = int(self.health_regen + 3000)
        def regenerate_tick(self):
            self.health_regen = int(self.health_regen - 50)
        def regenerate_reset(self):self.health_regen = 3000
        def gain_exp(self, amount):
            self.exp = int(self.exp + amount)
            if talent_list[0] == True: ##GENOCIDE TALENT
                self.attack += 0.5
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
        def player_take_damage(self, e_atk):
            self.health -= e_atk
        def talentupdate(self, name):
            if name == "genocide": #0
                talent_list[0] = True
                talent_names.append(name)
            if name == "bigman": #1
                talent_list[1] = True
                talent_names.append(name)
            if name == "counterattack": #5
                talent_list[2] = True
                talent_names.append(name)
            if name == "victoryrush": #3
                talent_list[3] = True   
                talent_names.append(name)
            if name == "sweep": #6
                talent_list[4] = True
                talent_names.append(name)
            if name == "necromancer": #6
                talent_list[5] = True
                talent_names.append(name)
        # def gain_gear_stats(self):
        #     self.attack = self.__dict__["attack"] + gear_stats_dict["attack"]
        #     # pass
        def showdetailedstats(self):
            detailedstats = "{} {} {} {} {} {}".format(self.health, self.attack, self.defense, self.a_speed, self.evade, self.health_regen)
            array = detailedstats.split()
            return "health:"+array[0]+" "+"attack:"+ array[1]+" "+"defense:"+array[2]+" "+"a_speed:"+array[3]+" "+"evade:"+array[4]+" "+"health_regen"+array[5] 
talent_list = [False, False, False, False, False, False]
talent_names = []
bool(talent_list)

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
        self.swing = 0
        self.attacked = False
        self.evade = evade
        self.base_cooldown = base_cooldown
        self.killcount = killcount
        self.cooldown = cooldown
        self.count = 0
        self.max_health = health
        self.name = name
        self.exp = exp
        self.hit = 0

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
#### GRID STUFF
# grid_exists = False
##### GRID STUFF


def get_start_point():
    global start_point
    for i in range(len(build_grid)):
        for x in build_grid[i]:
            if x.start_point == True:
                start_point = x

# #RNG BEGIN
def getRandomInt(a, b):
    c = random.randint(a, b)
    return c
# # RNG END
##INT INCREASER
def increase_int(x, a, b):
    if x != b:
        x += 1

    if x == b:
        x = a
    return x

    

pause = False
##END INCREASER
screen = pygame.display.set_mode((1600, 900))
# loopcount = 0
talent_select_screen = False
###EQUIP ITEMS###########
equip_wep_spr = pygame.sprite.GroupSingle() #equipped item sprites
equip_rin_spr = pygame.sprite.GroupSingle() #
equip_rin_spr = pygame.sprite.GroupSingle() #equipped item sprites
equip_che_spr = pygame.sprite.GroupSingle() #
equip_hel_spr = pygame.sprite.GroupSingle() #
equip_shi_spr = pygame.sprite.GroupSingle() #
equip_list = [equip_wep_spr, equip_rin_spr, equip_che_spr, equip_hel_spr, equip_shi_spr] # array of equipped items  
        
def draw_equips():
    screen.blit(weapon_slot_img, weapon_slot_rect)
    screen.blit(chest_slot_img, chest_slot_rect)
    screen.blit(helm_slot_img, helm_slot_rect)
    screen.blit(shield_slot_img, shield_slot_rect)
    screen.blit(ring1_slot_img, ring1_slot_rect)
    screen.blit(ring1_slot_img, ring2_slot_rect)
def inv_slot_index():
    global inv_index
    for x in range(len(inventory_list)):
        if inventory_list[x].rect.collidepoint(mousepos()) == True:
            inv_index = x
            return int(inv_index)

def equip_slot_index():
    global weapon_equipped, eq_wep
    for x in equip_list:
        if len(x.sprites()) > 0:
            a = x.sprites()[0]
            if x.sprites()[0].rect.collidepoint(mousepos()) == True:
                return x.sprites()[0].equiptype
                
    # if len(equip_wep_spr.sprites()) > 0:
    #     # weapon_equipped = True
    #     eq_wep = equip_wep_spr.sprites()[0]
    #     if equip_wep_spr.sprites()[0].rect.collidepoint(mousepos()) == True:
    #         return "weapon"


                
###TOOLTIP DISPLAY###
def tooltip_display():
    #display inventory weapon
    x = inv_slot_index()
    if x != None: 
        t, c = inventory_list[x].tooltip()
        displaynumbercenter("name","", inventory_list[x].name, c, 18, 1300, 285) 
        y_pos = 300
        for x in range(len(t)):
            displaynumbercenter(str(x), str(t[x][0])+": ", t[x][1], "red", 15, 1300, y_pos+(x*15))

    #display equipped weapon
    if len(equip_wep_spr.sprites()) >= 0: 
        y = equip_slot_index()
        if y == "weapon":
            w = equip_wep_spr.sprites()[0]
            t, c = w.tooltip()
            displaynumbercenter("name","", w.name, c, 18, 1300, 285) 
            y_pos = 300
            for x in range(len(t)):
                displaynumbercenter(str(x), str(t[x][0])+": ", t[x][1], "red", 15, 1300, y_pos+(x*15))
        if y == "chest":
            w = equip_che_spr.sprites()[0]
            t, c = w.tooltip()
            displaynumbercenter("name","", w.name, c, 18, 1300, 285) 
            y_pos = 300
            for x in range(len(t)):
                displaynumbercenter(str(x), str(t[x][0])+": ", t[x][1], "red", 15, 1300, y_pos+(x*15))
        if y == "helm":
            w = equip_hel_spr.sprites()[0]
            t, c = w.tooltip()
            displaynumbercenter("name","", w.name, c, 18, 1300, 285) 
            y_pos = 300
            for x in range(len(t)):
                displaynumbercenter(str(x), str(t[x][0])+": ", t[x][1], "red", 15, 1300, y_pos+(x*15))
        if y == "shield":
            w = equip_shi_spr.sprites()[0]
            t, c = w.tooltip()
            displaynumbercenter("name","", w.name, c, 18, 1300, 285) 
            y_pos = 300
            for x in range(len(t)):
                displaynumbercenter(str(x), str(t[x][0])+": ", t[x][1], "red", 15, 1300, y_pos+(x*15))
        if y == "ring":
            w = equip_rin_spr.sprites()[0]
            t, c = w.tooltip()
            displaynumbercenter("name","", w.name, c, 18, 1300, 285) 
            y_pos = 300
            for x in range(len(t)):
                displaynumbercenter(str(x), str(t[x][0])+": ", t[x][1], "red", 15, 1300, y_pos+(x*15))
        
    
        
### TOOLTIP DISPLAY ###
##LOAD ENEMY ASSETS
img_candle = [pygame.image.load("J:\Python\Projects\game\Assets\candles\candle1.png").convert_alpha(), pygame.image.load("J:\Python\Projects\game\Assets\candles\candle1.png").convert_alpha(), pygame.image.load("J:\Python\Projects\game\Assets\candles\candle1.png").convert_alpha(), pygame.image.load("J:\Python\Projects\game\Assets\candles\candle4.png").convert_alpha()]
img_skelarmy = [pygame.image.load("J:\Python\Projects\game\Assets\Skeleton\skeleton1.png").convert_alpha(), pygame.image.load("J:\Python\Projects\game\Assets\Skeleton\skeleton2.png").convert_alpha(), pygame.image.load("J:\Python\Projects\game\Assets\Skeleton\skeleton3.png").convert_alpha(), pygame.image.load("J:\Python\Projects\game\Assets\Skeleton\skeleton4.png").convert_alpha()]
img_testdummy = [pygame.image.load("testdummy.png").convert_alpha(), pygame.image.load("testdummy.png").convert_alpha(), pygame.image.load("testdummy.png").convert_alpha(), pygame.image.load("testdummy.png").convert_alpha()]

##ANIMATION PICTURES
# img_campfire1 = pygame.image.load("J:\Python\Projects\game\Assets\smolcampfire16x16\campfire_1_smol.png").convert_alpha()
# img_campfire2 = pygame.image.load("J:\Python\Projects\game\Assets\smolcampfire16x16\campfire_2_smol.png").convert_alpha()
# img_campfire3 = pygame.image.load("J:\Python\Projects\game\Assets\smolcampfire16x16\campfire_3_smol.png").convert_alpha()
# img_campfire4 = pygame.image.load("J:\Python\Projects\game\Assets\smolcampfire16x16\campfire_4_smol.png").convert_alpha()
img_campfire1 = pygame.image.load("campfire1.png").convert_alpha()
img_campfire2 = pygame.image.load("campfire2.png").convert_alpha()
img_campfire3 = pygame.image.load("campfire3.png").convert_alpha()
img_campfire4 = pygame.image.load("campfire4.png").convert_alpha()
img_campfire1_res = pygame.transform.scale(img_campfire1, (16, 16))
img_campfire2_res = pygame.transform.scale(img_campfire2, (16, 16))
img_campfire3_res = pygame.transform.scale(img_campfire3, (16, 16))
img_campfire4_res = pygame.transform.scale(img_campfire4, (16, 16))
campfire_animations = [img_campfire1_res, img_campfire2_res, img_campfire3_res, img_campfire4_res]
campfire_rectangles = [img_campfire1_res.get_rect(), img_campfire2_res.get_rect(), img_campfire3_res.get_rect(), img_campfire4_res.get_rect()]
img_bluefireball1 = pygame.image.load("bluefireball1.png").convert_alpha()
img_bluefireball2 = pygame.image.load("bluefireball2.png").convert_alpha()
img_bluefireball3 = pygame.image.load("bluefireball3.png").convert_alpha()
img_bluefireball4 = pygame.image.load("bluefireball4.png").convert_alpha()
bluefireball_animations = [img_bluefireball1, img_bluefireball2, img_bluefireball3, img_bluefireball4]
bluefireball_index = 0
bluefireball_surf = bluefireball_animations[bluefireball_index]

###TALENT MENU#################
# talent_menu_button_rect_pressed = False
img_talent_menu_button_static = pygame.image.load("talentmenubuttonstatic.png").convert()
img_talent_menu_button_hovered = pygame.image.load("talentmenubuttonhovered.png").convert()
img_talent_menu_button_pressed = pygame.image.load("talentmenubuttonpressed.png").convert()
# img_talent_menu_button_array = [img_talent_menu_button_static, img_talent_menu_button_hovered, img_talent_menu_button_pressed]
talent_menu_button_rect = img_talent_menu_button_static.get_rect(midright = (635, 40))


def talent_menu_button_animation():
    if talent_menu_button_rect.collidepoint(mousepos()): #check is mouse is on button rect
        screen.blit(img_talent_menu_button_hovered, talent_menu_button_rect) #if mouse on button rect = draw hovered.ng
    if lmb() == True and talent_menu_button_rect.collidepoint(mousepos()): #check if LMB is also pressed
        screen.blit(img_talent_menu_button_pressed, talent_menu_button_rect) #if LMB is clicked  = draw pressed.png
        


####IMAGES FOR STATIC 
img_topmenu = pygame.image.load("topmenubar.png").convert_alpha()
####END IMAGES FOR STATIC
###IMAGES FOR TALENTS
img_talent_genocide = pygame.image.load("talent_genocide.png").convert()
img_talent_bigman = pygame.image.load("talent_bigman.png").convert()
img_talent_counterattack = pygame.image.load("talent_counterattack.png").convert()
img_talent_array = [img_talent_genocide, img_talent_bigman, img_talent_counterattack] # array of talent IMAGES
img_talent_array_id = [img_talent_genocide, img_talent_bigman, img_talent_counterattack] # array of talent IMAGES
####END IMAGES FOR STATIS
##ANIMATION FUNCTIONS #################################
animation_start_x = 768
animation_start_y = 360
iterations = 0
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


# CIRCLE STUFF BEGIN
totalDegrees = 360
radius = 250 # Radius as a variable 
xCoords = [] # array of x coordinates
yCoords = [] # array of y coordinates 
angle = 0 # angle in degrees
circle_x_pos = 800
circle_y_pos = 500 
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

#PLAYERSPRITE???#
# pla_sprite_pos = 0
pla_img = pygame.image.load('player.png').convert_alpha()
pla_sprite = her_sprite(pla_img, 0, 0)
pla_group = pygame.sprite.Group()
pla_group.add(pla_sprite)
## INITIATE SOME MONSTER SPRITES

    
##END INITIATING MONSTER SPRITES 
####EQUIPMENTSPRITES#################
equips_group = pygame.sprite.Group()


##SPRITE GROUPS OUTSIDE MAIN FUNC
testdummy_group = pygame.sprite.Group()
trashmob_group = pygame.sprite.Group()
boss_group = pygame.sprite.Group()
# environment_group = pygame.sprite.GroupSingle()
attackanimations_group = pygame.sprite.Group()
# inventory_spr_group = pygame.sprite.Group()

### END SPRITE GROUPS
# xzeroyzero = integer_coords(0)
# ###THIS IS DUMB:
# campfire1 = environment(img_campfire1_res, xzeroyzero[0], xzeroyzero[1])
# campfire2 = environment(img_campfire2_res,  xzeroyzero[0], xzeroyzero[1]) 
# campfire3 = environment(img_campfire3_res,  xzeroyzero[0], xzeroyzero[1]) 
# campfire4 = environment(img_campfire4_res,   xzeroyzero[0], xzeroyzero[1])
# environment_group.add(campfire1,campfire2,campfire3,campfire4)
campfire_index = 0
def animate_background():
    global campfire_index
    campfire_index = increase_int(campfire_index,0,4)
    # campfire_timer = int(campfire_timer + 1)
    # if campfire_timer == 3:
        # campfire_timer = 0
    # print(campfire_index)
    campfire_sprite_list = [img_campfire1_res, img_campfire2_res, img_campfire3_res, img_campfire4_res]
    # environment_group.add(campfire_sprite_list[campfire_timer])
    if len(walking_coords_list) > 0:
        screen.blit(campfire_sprite_list[campfire_index], start_point.rect.center)
    # environment_group.draw(screen)


ske_sprite = trashmob(img_skelarmy, int(xCoords[getRandomInt(0, 360)]),int(yCoords[getRandomInt(0, 360)]), 60)
can_sprite = trashmob(img_candle, int(xCoords[getRandomInt(0, 360)]), int(yCoords[getRandomInt(0, 360)]), 60)
test_sprite = trashmob(img_testdummy, int(xCoords[10]), int(yCoords[10]), 60000)
trashmob_group.empty()


###SPAWNING STUFFFF

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
    for x in equip_list:
        x.draw(screen)
    
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
def displaynumberleft(name, prefix, text, color, size, x, y):
    apply_size = pygame.font.Font("C:\WINDOWS\Fonts\cambriab.ttf", size) #picks the font and the size, only the size is variable
    str_text = prefix + str(text)   #stringifies the integer
    rendered_text = apply_size.render(str_text, False, color) #converts text to image
    name = rendered_text.get_rect(midleft = (x, y)) #assign the text a rectangle in variable "name"
    screen.blit(rendered_text, name)    #place image on screen
# def displaytext(name, text, color, size, x, y, pos):
#             apply_size = pygame.font.Font("C:\WINDOWS\Fonts\cambriab.ttf", size) #picks the font and the size, only the size is variable
#             rendered_text = apply_size.render(text, False, color) #converts text to image
#             name = rendered_text.get_rect(pos = (x, y)) #assign the text a rectangle in variable "name"
#             screen.blit(rendered_text, name)    #place image on screen

def main():
    global time 
    pla_sprite_pos = 0
    test_font = pygame.font.Font("C:\WINDOWS\Fonts\cambriab.ttf", 50)
    screen = pygame.display.set_mode((1600, 900))
    color = (255, 0, 0)

    # background = pygame.image.load("roguebgbig.png").convert_alpha() #art background
    background = screen.fill("black") #black background
    battlebg = pygame.image.load("battlebg.png").convert_alpha()
    p_pos_v = 0
    zero = 0
    loop_start = True

#GAME INFORMATION
    battletime = 50
    # time = 100
#PLAYER INFORMATION
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
    player_info = hero(pla_all[0], pla_all[1], pla_all[2], pla_all[3], pla_all[4], pla_all[5], pla_all[6], pla_all[7], pla_all[8], pla_all[9], pla_all[10])

    def gear_incr_stats(eq_spr):
        eq_wep_stats = {} #create new dict for only the weapon keys that are ints
        player_info_stats = {} #ditto for player dict
        # eq_wep = equip_wep_spr.sprites()[0] #shorter a variable name, eq_wep = the instance of the equipped weapon
        # if dontspamequips <= 0: #only if item equip cooldown is 0 do the stats update (to prevent bugs)
        for x in eq_spr.__dict__: #for x in the regular equipped weapon dictionary
            if isinstance(eq_spr.__dict__.get(x), int) == True:  #if the key = int
                eq_wep_stats[x]=eq_spr.__dict__.get(x) #append the key to the earlier created new Dict for only int keys
        for x in player_info.__dict__: #ditto for player dict
            if isinstance(player_info.__dict__.get(x), int) == True:
                player_info_stats[x]=player_info.__dict__.get(x)
                
        counter_a = Counter(eq_wep_stats) #create a counter object/list for the weapon stats dict
        # print("incr wep stats")
        # print(counter_a)
        counter_b = Counter(player_info_stats) #create a counter object/list for the player stats
        # print("incr pla stats")
        # print(counter_b)
        counter_c = counter_a + counter_b #compute difference between player and weapon stats
        # print("incr update")
        # print(counter_c)
        player_info.__dict__.update(counter_c) #update the player instance with the computed difference
    
    def gear_decr_stats(eq_spr):
        eq_wep_stats = {} #create new dict for only the weapon keys that are ints
        player_info_stats = {} #ditto for player dict
        # eq_wep = equip_wep_spr.sprites()[0] #shorter a variable name, eq_wep = the instance of the equipped weapon

        # if dontspamequips <= 0: #only if item equip cooldown is 0 do the stats update (to prevent bugs)
        for x in eq_spr.__dict__: #for x in the regular equipped weapon dictionary
            if isinstance(eq_spr.__dict__.get(x), int) == True:  #if the key = int
                eq_wep_stats[x]=0 - eq_spr.__dict__.get(x) #append the key to the earlier created new Dict for only int keys
        for x in player_info.__dict__: #ditto for player dict
            if isinstance(player_info.__dict__.get(x), int) == True:
                player_info_stats[x]=player_info.__dict__.get(x)
        counter_a = Counter(eq_wep_stats) #create a counter object/list for the weapon stats dict
        # print("decr wep stats")
        counter_b = Counter(player_info_stats) #create a counter object/list for the player stats
        # print("decr pla stats")
        counter_c = counter_b + counter_a
        # print("decr update")
        player_info.__dict__.update(counter_c) #update the player instance with the computed difference
            
    equip_cooldown = False
    def equip_item():
        # global dontspamequips
        global dontspamequips, weapon_equipped, equip_cooldown
        x = inv_slot_index() # x returns the number of the invent slot that u hover over

        if dontspamequips >= 0: #cooldown so that the entire invent doesnt equip
            dontspamequips -= (time*2)
            
        for event in pygame.event.get():
            # if event == MOUSEBUTTONDOWN:
            #     equip_cooldown = True
            if event != MOUSEBUTTONUP:
                equip_cooldown = False

        if x != None:
            if len(inventory_list) > 0 and inventory_list[x].rect.collidepoint(mousepos()) and lmb() == True and equip_cooldown == False: 
                equip_cooldown = True
                item = inventory_list[x]
                inventory_spr_group.remove(item) #removes the the item from the inventory sprite group

                if item.equiptype == "weapon":
                    eq_wep = item
                    if len(equip_wep_spr.sprites()) > 0:
                        gear_decr_stats(equip_wep_spr.sprites()[0])
                    equip_wep_spr.add(item) #this adds the selected item to the weaponslot
                    gear_incr_stats(eq_wep)
                    eq_wep.rect.center = [1400, 150] #moves the image to the weapon slot
                    
                if item.equiptype == "chest":    
                    eq_che = item
                    if len(equip_che_spr.sprites()) > 0:
                        gear_decr_stats(equip_che_spr.sprites()[0])
                    equip_che_spr.add(item) #this adds the selected item to the weaponslot
                    gear_incr_stats(eq_che)
                    eq_che.rect.center = [1450, 150] #moves the image to the weapon slot
                    
                if item.equiptype == "helm":
                    eq_hel = item
                    if len(equip_hel_spr.sprites()) > 0:
                        gear_decr_stats(equip_hel_spr.sprites()[0])
                    equip_hel_spr.add(item) #this adds the selected item to the weaponslot
                    gear_incr_stats(eq_hel)
                    eq_hel.rect.center = [1500, 150] #moves the image to the weapon slot    
                    
                if item.equiptype == "shield":
                    eq_shi = item 
                    if len(equip_shi_spr.sprites()) > 0:
                        gear_decr_stats(equip_shi_spr.sprites()[0])
                    equip_shi_spr.add(item) #this adds the selected item to the weaponslot
                    gear_incr_stats(eq_shi)
                    eq_shi.rect.center = [1400, 200] #moves the image to the weapon slot  
                    
                if item.equiptype == "ring":
                    eq_rin = item 
                    if len(equip_rin_spr.sprites()) > 0:
                        gear_decr_stats(equip_rin_spr.sprites()[0])
                    equip_rin_spr.add(item) #this adds the selected item to the weaponslot
                    gear_incr_stats(eq_rin)
                    eq_rin.rect.center = [1500, 200] #moves the image to the weapon slot
                
                
                inventory_list.pop(x) #removes the item from the invent
                inventory_spr_group.empty() #synchronizes the equipment sprites with the inventorylist
                inventory_spr_group.add(inventory_list)
                
                dontspamequips += 500 #sets a 1000 ms cooldown for equipping new items
                sortloot() #sort the inventory
                
    def equip_item2():
        global dontspamequips, weapon_equipped
        x = inv_slot_index() # x returns the number of the invent slot that u hover over
        
        if dontspamequips >= 0: #cooldown so that the entire invent doesnt equip
            dontspamequips -= time
        weapon_equipped = False
        if x != None:
            if len(inventory_list) > 0 and inventory_list[x].rect.collidepoint(mousepos()) and lmb() == True and dontspamequips <= 0:
                if weapon_equipped == True:
                    gear_decr_stats()
                inventory_spr_group.remove(inventory_list[x]) #removes the the item from the inventory sprite group
                if inventory_list[x].weapontype == "weapon":
                    inventory_list[x].rect.center = [1400, 150] #moves the image to the weapon slot
                if inventory_list[x].weapontype == "ring":
                    inventory_list[x].rect.center = [1450, 150] #moves the image to the weapon slot
                if inventory_list[x].weapontype == "chest":
                    inventory_list[x].rect.center = [1500, 150] #moves the image to the weapon slot
                if inventory_list[x].weapontype == "helm":
                    inventory_list[x].rect.center = [1200, 150] #moves the image to the weapon slot
                if inventory_list[x].weapontype == "shield":
                    inventory_list[x].rect.center = [1200, 150] #moves the image to the weapon slot
                equip_wep_spr.add(inventory_list[x]) #this adds the selected item to the weaponslot
                eq_wep = equip_wep_spr.sprites()[0]
                weapon_equipped = True
                inventory_list.pop(x) #removes the item from the invent
                inventory_spr_group.empty() #synchronizes the equipment sprites with the inventorylist
                inventory_spr_group.add(inventory_list)
                gear_incr_stats()
                dontspamequips += 500 #sets a 1000 ms cooldown for equipping new items
                sortloot() #sort the inventory

    ###talent
    bigman_talent = False
    genocide_talent = False
    counterattack_talent = False
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
    testdummy = enemies(test_all[0], test_all[1], test_all[2], test_all[3], test_all[4], test_all[5], test_all[6], test_all[7], test_all[8], test_all[9])
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
    candle1 = enemies(can_all[0], can_all[1], can_all[2], can_all[3], can_all[4], can_all[5], can_all[6], can_all[7], can_all[8], can_all[9])
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
    
    skelarmy1 = enemies(ske_all[0], ske_all[1], ske_all[2], ske_all[3], ske_all[4], ske_all[5], ske_all[6], ske_all[7], ske_all[8], ske_all[9])
    img_skelarmy = pygame.image.load("skellarmy.png").convert_alpha()
    
    def multi_combat_call(x):
        if x == 0: #0 = Skelarmy
            return enemies(ske_all[0], ske_all[1], ske_all[2], ske_all[3], ske_all[4], ske_all[5], ske_all[6], ske_all[7], ske_all[8], ske_all[9])
        if x == 1: #1 = Candle
            return enemies(can_all[0], can_all[1], can_all[2], can_all[3], can_all[4], can_all[5], can_all[6], can_all[7], can_all[8], can_all[9])

####ENEMYCOMBATSPAWNERS#############
####ENEMYCOMBATSPAWNERS#############   
####IMPORTANT FUCKING VARIABLES
    start_point = None
    # loopcount = 0
    time = 250
    display_inventory_tooltip = None
    def speed_up():
        global time
        time = time * 2

    def speed_down():
        global time
        time = time / 2
    # blue_border = False
    # green_border = False
####MAIN GAME LOOP###
    while True:
        create_grid()
        ###KEYBINDS
        for event in pygame.event.get():
            if event.type == (pygame.KEYDOWN):
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_2:
                    print(time)
                    if time <= 2000:
                        time = int(time *2)
                if event.key == pygame.K_1:
                    print(time)
                    if time >= 2:
                        time = int(time/2)
                # if event.key == pygame.K_t:
                # #     spawn_testdummy()
                #     testdummy_group.draw(screen)
                if event.key == pygame.K_F1:
                    player_info.health += 400000000
                    # player_info.defense += 400000000
                    print("faggot mode: ON\n +400mill health and defense")
                if event.key == pygame.K_F2:
                    player_info.attack -= 10
                if event.key == pygame.K_F3:
                    player_info.attack += 10
                if event.key == pygame.K_p:
                    secondpause()
                if event.key == pygame.K_w:
                    print(buildings)
                    print(player_card_hand)
                if event.key == pygame.K_e: 
                    loot_table(1,1)
                if event.key == pygame.K_3:
                    roll_cards_t1(3)           
                # if event.key == pygame.K_7:
                    
                if event.key == pygame.K_i:
                    player_info.defense += 5
                if event.key == pygame.K_o:
                    player_info.defense -+ 5
                if event.key == pygame.K_8:
                    pass
                # if event.key == pygame.K_6:
                #     walking_coords()
                if event.key == pygame.K_F9:
                    print(start_point.loc)
                    for x in grid_path_list_with_instances:
                        print(x.loc)
                if event.key == pygame.K_F8:
                    print("grid_path_list_with_instances:")
                    print(grid_path_list_with_instances)
                    print(len(grid_path_list_with_instances))

                    print("path_detect_list:")
                    print(path_detect_list)
                    print(len(path_detect_list))
                if event.key == pygame.K_y:
                    for x in grid_path_list_with_instances:
                        x.orange_border()
                if event.key == pygame.K_n:
                    if green_border == False:
                        green_border = True
                    else: green_border = False

                    for i in range(len(build_grid)):
                        for x in build_grid[i]:
                            x.green_border()

                if event.key == pygame.K_b:
                    if blue_border == False:
                        blue_border = True
                    else: blue_border = False

                    blue_border = True
                    for i in range(len(build_grid)):
                        for x in build_grid[i]:
                            x.blue_border()
                if event.key == pygame.K_t:
                    for i in range(len(build_grid)):
                        for x in range(len(build_grid[i])):
                            print(build_grid[i][x].loc)
                if event.key == pygame.K_u:
                    # print("routedgrid:")
                    # print(routed_grid)
                    # print(len(routed_grid))
                    
                    print("path_detect_list:")
                    print(path_detect_list)
                    print(len(path_detect_list))
                    
                if event.key == pygame.K_0:
                    for i in range(10):
                        for x in build_grid[i]:
                            print(x.grid_type)
                # if event.key == pygame.K_5:
                #     path_start(start_point)
                #     print(path)

                #     # path_cols = [] # array of path column values
                #     # path_rows = [] # array of path row values
                #     # for x in path:
                #     #     path_cols.append(x.col)
                #     #     path_rows.append(x.row)
                    # print(path_rows)
                    # print(path_cols)
                    # # print(build_grid)           
        if build_building() != None and lmb() != True:
            arg = build_building()
            arg1 = arg[0]
            arg2 = arg[1]
            arg3 = arg[2]
            arg4 = arg[3]
            builder_building(arg1, arg2, arg3, arg4)
            
#### GEARSTUFF #################
        # player_info.attack = player_info.attack + gear_stats_dict["attack"]
                    
### GEARSTUFF #############
        
###TALENT MENU SELECTOR###        
        if lmb() == True and talent_menu_button_rect.collidepoint(mousepos()): #check if LMB is also pressed
            talent_select()
            player_info.talentupdate(talent_selected())
        #### KEYBINDS END
###############################################################################
#GAME INFORMATION
        ####################################################################################################################################
        #draw the rest of the game
        def drawbackground():
            #background
            # screen.blit(background, (0, 0)) # set background 1
            screen.fill("black")
            # environment_group.draw(screen) #campfire
            screen.blit(img_topmenu, (0, 0))  #menu
            screen.blit(img_talent_menu_button_static, talent_menu_button_rect)
            talent_menu_button_animation()     
            draw_path()
            get_start_point() #has to happen after draw_path()
            animate_background()# draw_equips()
        drawbackground()
        #########SET START POINT, INCONVNIENT BUT IT HAS TO HAPPEN AFTER DRAW_PATH)
        # while start_point == None: #### set the start_location
        #     start_point = set_start(random.choice(path_detect_list))
        #     print(start_point.loc)
        #     print(start_point)
        ####################################################################################################################################
        #DEBUGGING#DEBUGGING      
        
        # for x in player_card_hand:
        #     print(x.mouseover)   
        #DEBUGGING#DEBUGGING         
        ####################################################################################################################################
        # displaynumberleft("cardlist", "Cards:", player_card_hand, "yellow",15, 5, 485)
        # displaynumberleft("cardlist", "Cards:", len(player_card_hand), "yellow",15, 5, 470)
        # # displaynumberleft("multicombat", "enemies: ", current_enemy_sprite.multicombat, "yellow",20, 5, 500)
        # # displaynumberleft("talentlist", "Active Talents:", talent_names, "yellow",20, 5, 500)
        # displaynumberleft("inventorylistobejcts", "inventory: ", inventory_list, "yellow",20, 5, 520)
        # displaynumberleft("length of invlist", "items in invent: ", len(inventory_list), "yellow",20, 5, 540)
        # displaynumberleft("inventorysprgroupobjects", "# sprites invent: ", inventory_spr_group.sprites(), "yellow",20, 5, 560)
        # displaynumberleft("sprites in invent", "grid index: ", grid_index(), "yellow" ,20, 5, 580)
        if grid_index() != None and grid_index()[0] != None and grid_index()[1] != None:
            displaynumberleft("sprites in invent", "grid index: ", str(build_grid[grid_index()[1]][grid_index()[0]].up) + str(str(build_grid[grid_index()[1]][grid_index()[0]].down)  + str(str(build_grid[grid_index()[1]][grid_index()[0]].left)) + str(str(build_grid[grid_index()[1]][grid_index()[0]].right))), "yellow" ,20, 5, 450)
        if grid_index() != None and grid_index()[0] != None and grid_index()[1] != None:
            displaynumberleft("sprites in invent", "grid index: ", str(build_grid[grid_index()[1]][grid_index()[0]].up) + str(str(build_grid[grid_index()[1]][grid_index()[0]].down)  + str(str(build_grid[grid_index()[1]][grid_index()[0]].left)) + str(str(build_grid[grid_index()[1]][grid_index()[0]].right))), "yellow" ,20, 5, 450)
        displaynumberleft("up,down,left,right", "UP, DOWN, LEFT, RIGHT: ","yellow", 0 , 20, 5 , 430)
        displaynumberleft("pathlength", "path length: ",str(len(path_detect_list)), "yellow", 20, 5 , 470)
        # displaynumberleft("equipped", "equips: ", equipped_yn, "yellow", 20, 5 , 490)
        # # displaynumberleft("length of invlist", "items in invent: ", len(inventory_list), "yellow",20, 5, 540)
        displaynumberleft("playertyple", "player pos: ",pla_sprite.tuple, "yellow", 15, 5, 40)
        displaynumberleft("playertyple", "player pos: ", walking_coords_list[5], "yellow", 15, 5, 55)
        # displaynumber("currentenemy_cb", "opponent:", trashmob_group, "white" ,15, 1, 75)
        displaynumber("playerattack", "Attack: ", player_info.attack, "white", 15, 1200, 400)
        displaynumber("playerattack", "A_Speed: ", player_info.a_speed, "white", 15, 1200, 415)
        displaynumber("playerattack", "Lifesteal: ", player_info.lifesteal - 1, "white", 15, 1200, 430)
        displaynumber("playerattack", "Health_regen: ", player_info.health_regen, "white", 15, 1200, 445)
        displaynumber("playerattack", "Health: ", player_info.max_health, "white", 15, 1200, 460)
        displaynumber("playerattack", "Defense: ", player_info.defense, "white", 15, 1200, 475)
        displaynumber("playerattack", "Crit: ", player_info.crit - 1, "white", 15, 1200, 490)
        displaynumber("playerattack", "Spikes: ", player_info.spikes - 1, "white", 15, 1200, 505)
        displaynumber("playerattack", "Taunt: ", player_info.taunt - 1, "white", 15, 1200, 520)
        displaynumber("playerattack", "Counter: ", player_info.crit_damage - 1, "white", 15, 1200, 535)
        displaynumber("playerattack", "Block: ", player_info.block - 1, "white", 15, 1200, 550)
        displaynumber("playerattack", "Evade: ", player_info.evade, "white", 15, 1200, 565)
        displaynumber("playerattack", "Stun: ", player_info.stun - 1, "white", 15, 1200, 580)
        # displaynumber("chest", "chest: ", equip_che_spr.sprites(), "white", 15, 1200, 415)
        # displaynumber("sword", "sword: ", equip_wep_spr.sprites(), "white", 15, 1200, 430)
        # displaynumber("ring", "ring: ", equip_rin_spr.sprites(), "white", 15, 1200, 445)
        # displaynumber("shield", "shield: ", equip_shi_spr.sprites(), "white", 15, 1200, 460)
        # ###GRID###
        # displaynumber("mouseovergridindex", "Grid: ", grid_index(), "white", 15, 1300, 10)
        
        ###LEVELS###
        def displaymylevels():
            if grid_index() != None and grid_index()[0] != None and grid_index()[1] != None:
                index1 = grid_index()[0] ### VARIABLE NAME IS CORRECT
                index0 = grid_index()[1]
                indextuple = (index0, index1)
                displaynumber("gridindex","Grid Index:", indextuple, "white", 15, 1300, 10)
            displaynumber("exp", "", player_info.exp, "yellow", 15, 850, 25)
            displaynumber("level", "level:", player_info.level, "yellow",15, 960, 40) 
            displaynumber("exp_req", "/", player_info.exp_required, "yellow", 15, 930, 25)
            # displaynumber("detailedstats", "skelarmy1:", skelarmy1.showdetailedstats(), "white", 15, 1, 600)
            # displaynumber("detailedstats", "candle1:", candle1.showdetailedstats(), "white", 15, 1, 615)
            # displaynumber("detailedstats", "player:", player_info.showdetailedstats(), "white", 15, 1, 630)
            
            displaynumberleft("mousepos: ", "mousepos: ", mousepos(), "white", 15, 1300, 25)
            # displaynumber(name, prefix, text, white,5, 30, 260) 
        displaymylevels()
        ####################################################################################################################################



    #player position  
        if len(walking_coords_list) > 0: 
            pla_sprite_pos = increase_int(pla_sprite_pos, 0, len(walking_coords_list)-1) #pla_sprite_pos = 0, increase int adds 1 and reset it to 0 if its 360
            pla_sprite.player_walkpls(increase_int(pla_sprite_pos, 0, len(walking_coords_list)-1)) #updates the instance to go to set location to next point on circle

        
    #player health regeneration
        def regen_health():
            if player_info.health < player_info.max_health: 
                player_info.regenerate_tick()
            if player_info.health_regen <= 0 and player_info.health != 100: #if the time spent is (3000/time) gameticks or more
                player_info.regenerate_healthpoint()
            if player_info.health_regen <= 0:
                player_info.regenerate_reset()   
        regen_health()

        #check levleup
        player_info.levelup()     
        
        displaynumber("loopcount_rect","", loopcount, "white", 50, 512, 340) # displays the bugged out loopcount
        displaynumber("playerhealth", "HP:", player_info.health, "green", 50, 150, 50) #displays "800"

        #rng
        # if p_pos_v == 1: #if player is at the camp
        #     c = random.randint(0, 360) 
        #     d = random.randint(0, 360)

        # #SPAWNING ENEMIES
        def spawn_main():
            #CANDLES
            if candle1.base_cooldown == 0 and candle1.count == 0:
                spawn_candle()
                candle1.spawned()
            
            if candle1.base_cooldown >= 0:
                candle1.cooldown_tick()
            
            if candle1.base_cooldown <= 0:
                candle1.base_cooldown = 0
                #END CANDLES

                #SKELARMY
            if skelarmy1.base_cooldown == 0 and skelarmy1.count == 0:
                spawn_skelarmy()
                skelarmy1.spawned()

            if skelarmy1.base_cooldown >= 0:
                skelarmy1.cooldown_tick()
            
            if skelarmy1.base_cooldown <= 0:
                skelarmy1.base_cooldown = 0
                #END SKELARMY
        # spawn_main()
        # #END SPAWNING ENEMIES



        
        # #COMBAT ENEMY DETECTOR
        def enemyselect():
            ##TESTDUMMY################################
            if test_sprite in collidelist_testdummy:
                return [testdummy, test_sprite, testdummy_group, "test"]
            ## END TESTDUMMY #########
            
            ##TRASHMOBS##########################
            if ske_sprite in collidelist_trash:
                return [skelarmy1, ske_sprite, trashmob_group, 0]

            if can_sprite in collidelist_trash:
                return [candle1, can_sprite, trashmob_group, 1]
                
        # #END COMBAT ENEMY DETECTOR

#SCUFFED COMBAT SYSTEM 8.0
        reset_enemy_attack_animation(768) 
        battle_event = False
        collidelist_testdummy = pygame.sprite.spritecollide(pla_sprite, testdummy_group, False)
        collidelist_trash = pygame.sprite.spritecollide(pla_sprite, trashmob_group, False)
        p_hit = 0
        battleclock = 0
        if pygame.sprite.spritecollide(pla_sprite, trashmob_group, False, None) or pygame.sprite.spritecollide(pla_sprite, testdummy_group, False, None):
                battle_event = True # start combat
                current_enemy = enemyselect()
                current_enemy_stats = current_enemy[0]
                current_enemy_sprite = current_enemy[1]
                current_sprite_group = current_enemy[2]
                current_enemy_stats.prepareforcombat()
                if loopcount > 0: 
                    current_enemy_stats.apply_scaling(loopcount)
                    
                    
                multi_combat_stats = [] #list of enemies for combat stats ## HAVE TO BE UNIQUE
                for x in range(current_enemy_sprite.multi_combat):
                    multi_combat_stats.append(multi_combat_call(current_enemy[3]))
                    multi_combat_stats[x].swing = ((x+1)/current_enemy_sprite.multi_combat) * current_enemy_stats.a_speed
                    
                    
                    
        pygame.time.get_ticks()
        # e_hit = " "
        p_hit = " "
        battleclock = 0
        p_atk = 0
        battleclock = 0
        enemy_attacked = False
        while battle_event == True:
            for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            sys.exit()
                        if event.key == pygame.K_F1:
                            player_info.health += 10000
                        if event.key == pygame.K_F2:
                            player_info.attack -=10
                        if event.key == pygame.K_F3:
                            player_info.attack +=10
                        if event.key == pygame.K_F4:
                            player_info.defense -=10
                        if event.key == pygame.K_F5:
                            player_info.defense +=10
            ###COMBAT DEBUGGIN################
            ###COMBAT DEBUGGING
            battletime = 50
            battleclock += battletime/50
            #RENDERING STATICS##
            screen.fill("black")    #battle background
            
            ##ENEMY POSITIONS################
            enemy_pos_x = 768
            enemy_pos_y = 380
            screen.blit(current_enemy_sprite.image,(768, 380))
            multi_combat_list = [] #list to add enemies to for blitting, these are sprites
            
                
            if current_enemy_sprite.multi_combat > 1:
                for x in range(current_enemy_sprite.multi_combat):
                    multi_combat_list.append([current_enemy_sprite.image, (enemy_pos_x, enemy_pos_y)])
                    enemy_pos_y += 50
                screen.blits(multi_combat_list)   #draw enemy 

            screen.blit(pla_sprite.image, (256, 380)) #player on the background
            displaynumber("currentenemy_cb", "opponent:", current_enemy_stats.count, "white" ,15, 1, 150)
            displaynumber("currentenemy_cb", "opponent:", current_enemy_stats.name, "white" ,15, 1, 165)
            displaynumber("currentenemy_cb", "current_enemy_list:", current_enemy, "white" ,15, 1, 180)
            displaynumberleft("multicombat", "enemies: ", current_enemy_sprite.multi_combat, "yellow",20, 5, 500)
            #END RENDERING STATICS########
            for x in range(len(multi_combat_stats)-1):
                if multi_combat_stats[x].health <= 0:
                    multi_combat_stats.pop(multi_combat_stats.index(multi_combat_stats[x]))
            #COMBAT SYSTEM ACTUAL BATTLE
            ##PLAYER ATTACK
            #
            if player_info.a_speed <= p_atk: ##if enough time elapsed, attack:
                    r_enemy = random.randint(0,len(multi_combat_stats)-1) #select random enemy
                    p_hit = random.randint(player_info.attack, int(4*player_info.attack)) - multi_combat_stats[r_enemy].defense #calculate damage hit

                    multi_combat_stats[r_enemy].health -= p_hit
                    p_atk = 0 #reset attack timer

            p_atk += battletime ##increase P_atk
            
            # for x in range(len(multi_combat_stats)):
            #         multi_combat_stats[r_enemy].health -= p_hit
            #         p_atk = 0 #reset attack timer
            #         break
            
            ### ENEMY ATTACK
            for x in range(len(multi_combat_stats)):
                if multi_combat_stats[x].a_speed <= multi_combat_stats[x].swing: #if atk speed threshold reached
                    e_hit_calc = random.randint(multi_combat_stats[x].attack, int(4*multi_combat_stats[x].attack))-player_info.defense #calculate a dmg value
                    multi_combat_stats[x].swing = 0 #reset timer
                    
                    if e_hit_calc > 0: #if the hit is positive
                        multi_combat_stats[x].attacked = True
                        multi_combat_stats[x].hit = e_hit_calc #add hit value to instance call
                        player_info.health -= multi_combat_stats[x].hit
                        # multi_combat_stats[x].hit = 0
                        e_hit_calc = 0

                    if multi_combat_stats[x].hit <= 0: #if the hit is negative, set hit value to 0 so that the strike doesnt heal
                        multi_combat_stats[x].hit = 0 
                        
                if multi_combat_stats[x].attacked == True:
                    displaynumberleft("hit","", multi_combat_stats[x].hit, "red", 25, 368, 380 + x*50) 
                    if multi_combat_stats[x].swing >= (1/4)*multi_combat_stats[x].a_speed:
                        multi_combat_stats[x].attacked = False
                multi_combat_stats[x].swing += battletime #else just increase the attack timer    
                    
                    
                    
            ##play erhitsplat display  for 1/10th of attack speed
            if player_info.a_speed * 1/10 < p_atk:
                displaynumber("playerhitvalue","",p_hit, "red",25,700,380)
                
                
##ATTACK ANIMATION HIT DELAY
            ##if 2250 < e_atk = render hitsplat
            for x in range(len(multi_combat_stats)):
                i = 0
                if multi_combat_stats[x].a_speed * 3/4  < multi_combat_stats[x].swing:
                    y_pos = 390
                    new_y_pos = y_pos + (20*i+1)
                    
                    
                    if time_pass < int(3/4*multi_combat_stats[x].a_speed) and multi_combat_stats[x].attacked == True:
                        multi_combat_stats[x].attacked = False
                        # enemy_attacked = True
                        
                        
                    # reset_enemy_attack_animation(768)
                    i+=1
        ##if 2250 >  e_atk = show animation
                if multi_combat_stats[x].a_speed * 3/4 >= multi_combat_stats[x].swing:
                    enemy_attack_animation(multi_combat_stats[x].a_speed, battletime)
                    multi_combat_stats[x].attacked
                    # enemy_attacked = False
##display playerhealth and other shit    
                    
            displaynumber("incombatplayerhealth","",player_info.health, "green", 50,50, 50) 
            displaynumber("incombatplayerhealth","",player_info.health, "green", 50,50, 50) 
            displaynumber("incombatplayerhealth","",len(multi_combat_stats), "green", 5,5, 50) 
            

            #display swing timer    
            for x in range(len(multi_combat_stats)):
                y_pos = 380
                new_y_pos_1 = y_pos + (25*x+1)
                new_y_pos_2 = y_pos + (50*x+1)
                new_y_pos_3 = y_pos + (25*x+1)
                displaynumberleft("swing","", multi_combat_stats[x].swing, "purple", 25, 880, new_y_pos_2) 
            #display health next to enemy
                # new_y_pos = y_pos + (25*x+1)
                if len(multi_combat_stats) > 0:
                    displaynumberleft("incombatneemyhealth","", multi_combat_stats[0].health, "green", 25, 800, 380)
                if len(multi_combat_stats) > 1:
                    displaynumberleft("incombatneemyhealth","", multi_combat_stats[1].health, "green", 25, 800, 430)
                if len(multi_combat_stats) > 2:
                    displaynumberleft("incombatneemyhealth","", multi_combat_stats[2].health, "green", 25, 800, 480) 
                if len(multi_combat_stats) > 3:
                    displaynumberleft("incombatneemyhealth","", multi_combat_stats[3].health, "green", 25, 800, 530)
            # displaynumberleft("incombatneemyhealth","", multi_combat_stats[1].health, "green", 25, 768, 405) 
            # displaynumberleft("incombatneemyhealth","", multi_combat_stats[2].health, "green", 25, 768, 430) 
            # displaynumberleft("incombatneemyhealth","", multi_combat_stats[3].health, "green", 25, 768, 455) 
            #hitsplat
                # # new_y_pos = y_pos + (25*x+1)
                # if multi_combat_stats[x].hit > 0: 
                #     displaynumberleft("hit","", multi_combat_stats[x].hit, "red", 25, 368, new_y_pos_2) 
            # displaynumberleft("hit","", multi_combat_stats[1].hit, "green", 25, 768, 405) 
            # displaynumberleft("hit","", multi_combat_stats[2].hit, "green", 25, 768, 430) 
            # displaynumberleft("hit","", multi_combat_stats[3].hit, "green", 25, 768, 455) 
            # displaymylevels() 
            
            if multi_combat_stats[len(multi_combat_stats)-1].health <= 0 or player_info.health <= 0:
#TALENTMOD GENOCIDE     
                if talent_list[0] == True:
                    player_info.attack += 0.5
#TALENTMOD GENOCIDE
                current_enemy_stats.despawned()
                current_enemy_stats.cooldown_refresh() 
                current_enemy_sprite.despawned()
                current_sprite_group.remove(current_enemy_sprite)
                player_info.gain_exp(current_enemy_stats.exp)
                e_atk = 0
                loop_start = False #only after u fight something can you progress to the next loop
                battle_event = False
            pygame.display.update()
            pygame.time.delay(battletime)
#SCUFFED COMBAT SYSTEM IS OVER 
        # if pla_sprite.tuple == walking_coords_list[1]:
        #     loopcount += 1 
            
    ##RENDER SPRITES
        #draws the equipment slots
        draw_equips()
        #draws various sprites
        drawSprite()
        #tooltip functionality
        tooltip_display()
        #equips item
        equip_item()
        #draws card, see: game_cardsystem
        card_functionality() 
        #draw grid lines
        # draw_grid()
        #duplicate monsters
        for x in trashmob_group.sprites():
            x.duplicate()
        ###
        if len(inventory_list) > 0:
            for x in inventory_list:
                x.draw_rarity_border()
            inventory_spr_group.draw(screen)
            
        pygame.display.update()
        pygame.time.delay(time)
    #END OF THE LOOP, GO AGANE
        
    #run game
main()








    #debugging
