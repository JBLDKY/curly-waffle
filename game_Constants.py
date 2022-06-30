import pygame
from pygame.locals import *
import sys
import pygame.image
import pygame.key
import random
import math
pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((1600, 900))
img_talent_genocide = pygame.image.load("talent_genocide.png").convert_alpha()
img_talent_bigman = pygame.image.load("talent_bigman.png").convert_alpha()
img_talent_counterattack = pygame.image.load("talent_counterattack.png").convert_alpha()
img_talent_sweep = pygame.image.load("talent_sweep.png").convert_alpha()
img_talent_victoryrush = pygame.image.load("talent_victoryrush.png").convert_alpha()
img_talent_necromancer = pygame.image.load("talent_necromancer.png")
####talents arrays.convert_alpha()
img_talent_array = [img_talent_genocide, img_talent_bigman, img_talent_counterattack, img_talent_sweep, img_talent_victoryrush, img_talent_necromancer] # array of talent IMAGES
img_talent_array_id = [img_talent_genocide, img_talent_bigman, img_talent_counterattack, img_talent_sweep, img_talent_victoryrush, img_talent_necromancer] # array of talent IMAGES
img_talent_array_backup = [img_talent_genocide, img_talent_bigman, img_talent_counterattack, img_talent_sweep, img_talent_victoryrush, img_talent_necromancer] # array of talent IMAGES

###TIME/CLOCk
start_time = None
clock = pygame.time.Clock()
time_pass = pygame.time.Clock().get_time()
### END TIME/CLOCK




# ####PATHFINDING STUFF#######
pathfind_hor = pygame.image.load("J:\Python\Projects\game\pathstuff\pathfind_hor.png").convert_alpha()
pathfind_ver = pygame.image.load("J:\Python\Projects\game\pathstuff/pathfind_ver.png").convert_alpha()
pathfind_1 = pygame.image.load("J:\Python\Projects\game\pathstuff/pathfind1.png").convert_alpha()
pathfind_2 = pygame.image.load("J:\Python\Projects\game\pathstuff/pathfind2.png").convert_alpha()
pathfind_3 = pygame.image.load("J:\Python\Projects\game\pathstuff/pathfind3.png").convert_alpha()
pathfind_4 = pygame.image.load("J:\Python\Projects\game\pathstuff/pathfind4.png").convert_alpha()
img_path_list = [pathfind_1, pathfind_2, pathfind_3, pathfind_4, pathfind_hor, pathfind_ver]
# pathfind_ = pygame.img.load("J:\Python\Projects\game\Assets\pathstuff/pathfind_hor")
####END PATHFINDING STUFF#######

####CARDSYSTEM ASSETS#####
img_treescard = pygame.image.load("J:\Python\Projects\game\Assets\selfcards/trees.png").convert_alpha()
rect_treescard = img_treescard.get_rect()
img_trees_building = pygame.image.load("J:\Python\Projects\game/treesbuilding.png").convert_alpha()
img_rockscard = pygame.image.load("J:\Python\Projects\game\Assets\selfcards/rocks.png").convert_alpha()
rect_rockscard = img_rockscard.get_rect()
img_rocks_building = pygame.image.load("J:\Python\Projects\game/rocksbuilding.png").convert_alpha()
card_to_build = None
#####END CARDSYSTEM ASSETS####
####LOOTSYSTEM ASSETS ####
####t1 swords
img_sword1 = pygame.image.load("J:\Python\Projects\game\Loot\MyLoot\MeleeWeps\sword1.png").convert_alpha()
img_sword2 = pygame.image.load("J:\Python\Projects\game\Loot\MyLoot\MeleeWeps\sword2.png").convert_alpha()
img_sword3 = pygame.image.load("J:\Python\Projects\game\Loot\MyLoot\MeleeWeps\sword3.png").convert_alpha()
img_sword4 = pygame.image.load("J:\Python\Projects\game\Loot\MyLoot\MeleeWeps\sword4.png").convert_alpha()
img_sword_array = [img_sword1, img_sword2, img_sword3, img_sword4]
name_sword_array = ["Primitive Sword", "Broken Hilt", "Rusted Sword", "Chipped Sword"]
####t1 helms
img_helm1 = pygame.image.load("J:\Python\Projects\game\Loot\MyLoot\Helms/helm1.png").convert_alpha()
img_helm2 = pygame.image.load("J:\Python\Projects\game\Loot\MyLoot\Helms/helm2.png").convert_alpha()
img_helm3 = pygame.image.load("J:\Python\Projects\game\Loot\MyLoot\Helms/helm3.png").convert_alpha()
img_helm4 = pygame.image.load("J:\Python\Projects\game\Loot\MyLoot\Helms/helm4.png").convert_alpha()
img_helm_array = [img_helm1, img_helm2, img_helm3, img_helm4]
name_helm_array = ["Broken Helm", "Rusty Vizier", "Cracked Helm", "Cooking Pot"]
####t1 chests
img_chest1 = pygame.image.load("J:\Python\Projects\game\Loot\MyLoot\Chests/chest1.png").convert_alpha()
img_chest2 = pygame.image.load("J:\Python\Projects\game\Loot\MyLoot\Chests/chest2.png").convert_alpha()
img_chest3 = pygame.image.load("J:\Python\Projects\game\Loot\MyLoot\Chests/chest3.png").convert_alpha()
img_chest4 = pygame.image.load("J:\Python\Projects\game\Loot\MyLoot\Chests/chest4.png").convert_alpha()
img_chest_array = [img_chest1, img_chest2, img_chest3, img_chest4]
name_chest_array = ["Goblin Mail", "Broken Ringmail", "Leather Straps", "Rusted Cuirass"]
####t1 rings
img_ring1 = pygame.image.load("J:\Python\Projects\game\Loot\MyLoot\Rings/ring1.png").convert_alpha()
img_ring2 = pygame.image.load("J:\Python\Projects\game\Loot\MyLoot\Rings/ring2.png").convert_alpha()
img_ring3 = pygame.image.load("J:\Python\Projects\game\Loot\MyLoot\Rings/ring3.png").convert_alpha()
img_ring4 = pygame.image.load("J:\Python\Projects\game\Loot\MyLoot\Rings/ring4.png").convert_alpha()
img_ring_array = [img_ring1, img_ring2, img_ring3, img_ring4]
name_ring_array = ["Brass Ring", "Fractured Ring", "Tight Ring", "Dented Ring"]
####t1 shields
img_shield1 = pygame.image.load("J:\Python\Projects\game\Loot\MyLoot\Shields/shield1.png").convert_alpha()
img_shield2 = pygame.image.load("J:\Python\Projects\game\Loot\MyLoot\Shields/shield2.png").convert_alpha()
img_shield3 = pygame.image.load("J:\Python\Projects\game\Loot\MyLoot\Shields/shield3.png").convert_alpha()
img_shield4 = pygame.image.load("J:\Python\Projects\game\Loot\MyLoot\Shields/shield4.png").convert_alpha()
img_shield_array = [img_shield1, img_shield2, img_shield3, img_shield4]
name_shield_array = ["Wooden Buckler", "Kite Shield", "Square Plank", "Loose Fence"]
###LOOTSYSTEM ASSETS ###

###EQUIPSYSTEM ASSETS ###
weapon_slot_img = pygame.image.load("J:\Python\Projects\game\equips\swordequipslot.png").convert_alpha()
weapon_slot_rect = weapon_slot_img.get_rect(center = [1400, 150])
chest_slot_img = pygame.image.load("J:\Python\Projects\game\equips\chestequipslot.png").convert_alpha()
chest_slot_rect = chest_slot_img.get_rect(center = [1450, 150])
helm_slot_img = pygame.image.load("J:\Python\Projects\game\equips\helmequipslot.png").convert_alpha()
helm_slot_rect = helm_slot_img.get_rect(center = [1500, 150])
shield_slot_img = pygame.image.load("J:\Python\Projects\game\equips\shieldequipslot.png").convert_alpha()
shield_slot_rect = shield_slot_img.get_rect(center = [1400, 200])
ring1_slot_img = pygame.image.load("J:\Python\Projects\game\equips/ringequipslot.png").convert_alpha()
ring1_slot_rect = ring1_slot_img.get_rect(center = [1450, 200])
# ring2_slot_img = pygame.image.load("J:\Python\Projects\game\equips\ringequipslot.png")
ring2_slot_rect = ring1_slot_img.get_rect(center = [1500, 200])

# firstdimension = 3
# seconddimension = 4
    
    
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
dontspamequips = 0
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
    
##### GRID EXISTS #################################################################
grid_exists = False
grid_rect = pygame.draw.rect(screen, "white", (0,0, 64, 64))




####END GRID #################################################################################################
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
img_talent_genocide = pygame.image.load("talent_genocide.png").convert_alpha()
img_talent_bigman = pygame.image.load("talent_bigman.png").convert_alpha()
img_talent_counterattack = pygame.image.load("talent_counterattack.png").convert_alpha()
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
img_campfire1 = pygame.image.load("J:\Python\Projects\game\Assets\smolcampfire16x16\campfire_1_smol.png").convert_alpha()
img_campfire2 = pygame.image.load("J:\Python\Projects\game\Assets\smolcampfire16x16\campfire_2_smol.png").convert_alpha()
img_campfire3 = pygame.image.load("J:\Python\Projects\game\Assets\smolcampfire16x16\campfire_3_smol.png").convert_alpha()
img_campfire4 = pygame.image.load("J:\Python\Projects\game\Assets\smolcampfire16x16\campfire_4_smol.png").convert_alpha()
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


####SPRITE GROUPS #####
##SPRITE GROUPS OUTSIDE MAIN FUNC
testdummy_group = pygame.sprite.Group()
trashmob_group = pygame.sprite.Group()
boss_group = pygame.sprite.Group()
environment_group = pygame.sprite.GroupSingle()
attackanimations_group = pygame.sprite.Group()

def integer_coords(x):
    int_x_c = int(xCoords[x])
    int_y_c = int(yCoords[x])
    return int_x_c, int_y_c