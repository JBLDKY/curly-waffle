import pygame
from pygame.mixer import stop 
pygame.init()
import random
import sys
import pygame.image
from mousefunctionality import *
import math

screen = pygame.display.set_mode((1024, 680))

class talentcard(pygame.sprite.Sprite):
    def __init__(self, name, image, x, y):
        super(talentcard, self).__init__()
        self.name = name
        self.image = image
        self.x = x
        self.y = y
        self.rect = self.image.get_rect()
        self.rect.bottomleft = [x,y]
    def right(self, x, y):
        self.rect.bottomleft = [x, y]
    def left(self, x, y):
        self.rect.bottomleft = [x, y]
    def middle(self,x, y):
        self.rect.bottomleft = [x, y]


####IMAGES FOR STATIC 
img_topmenu = pygame.image.load("topmenubar.png").convert_alpha()
####END IMAGES FOR STATIC
###IMAGES FOR TALENTS
img_talent_genocide = pygame.image.load("talent_genocide.png")
img_talent_bigman = pygame.image.load("talent_bigman.png")
img_talent_counterattack = pygame.image.load("talent_counterattack.png")
img_talent_sweep = pygame.image.load("talent_sweep.png")
img_talent_victoryrush = pygame.image.load("talent_victoryrush.png")
img_talent_necromancer = pygame.image.load("talent_necromancer.png")
player_has_talent = [False, False, False, False, False, False]
# img_talent_array =  []
# img_talent_array_id = [img_talent_genocide, img_talent_bigman, img_talent_counterattack, img_talent_sweep, img_talent_victoryrush, img_talent_necromancer] # array of talent IMAGES
# img_talent_array_backup = [img_talent_genocide, img_talent_bigman, img_talent_counterattack, img_talent_sweep, img_talent_victoryrush, img_talent_necromancer] # array of talent IMAGES
img_talent_array_name_backup = ["genocide", "bigman", "counterattack", "sweep",  "victoryrush", "necromancer"]
dynamic_select_group = ["genocide", "bigman","counterattack",  "sweep",  "victoryrush", "necromancer"]
# img_talent_array_bool = []
# talent_choices_on_screen = []

##SPRITEINITIALIZATION##
# talentcard_sprite_group_total = pygame.sprite.Group()
# talentcard_sprite_group_selected = pygame.sprite.Group()
talent_card_left_group = pygame.sprite.GroupSingle()
talent_card_middle_group = pygame.sprite.GroupSingle()
talent_card_right_group = pygame.sprite.GroupSingle()
genocide_sprite = talentcard("genocide", img_talent_genocide, 0, 0)
bigman_sprite = talentcard("bigman", img_talent_bigman, 0, 0)
counterattack_sprite = talentcard("counterattack", img_talent_counterattack, 0, 0)
sweep_sprite = talentcard("sweep", img_talent_sweep, 0,0)
victoryrush_sprite = talentcard("victoryrush",img_talent_victoryrush, 0,0)
necromancer_sprite = talentcard("necromancer", img_talent_necromancer, 0,0)
##SPRITEGROUPTOTAL
talent_card_sprite_array = [genocide_sprite, bigman_sprite, counterattack_sprite, sweep_sprite, victoryrush_sprite, necromancer_sprite]

#
###DICTIONARY
Name = {
"genocide" : {
"name" : "genocide",
"sprite" : genocide_sprite,
"image" : genocide_sprite.image,
"rect" : genocide_sprite.rect,
"index" : img_talent_array_name_backup.index(genocide_sprite.name),
"hardindex" : 0
},
"bigman" : {
"name" : "bigman",
"sprite" : bigman_sprite, 
"image" : bigman_sprite.image,
"rect" : bigman_sprite.rect,
"index" : img_talent_array_name_backup.index(bigman_sprite.name),
"hardindex" : 1
},
"counterattack" : {
"name" : "counterattack",
"sprite" : counterattack_sprite, 
"image" :  counterattack_sprite.image,
"rect" : counterattack_sprite.rect,
"index" : img_talent_array_name_backup.index(counterattack_sprite.name),
"hardindex" : 2
},
"sweep" : {
"name" : "sweep",
"sprite" : sweep_sprite, 
"image" :  sweep_sprite.image,
"rect" : sweep_sprite.image,
"index" : img_talent_array_name_backup.index(sweep_sprite.name),
"hardindex" : 3
},
"victoryrush"  : {
"name" : "victoryrush",
"sprite" : victoryrush_sprite, 
"image" : victoryrush_sprite.image, 
"rect" : victoryrush_sprite.rect,
"index" : img_talent_array_name_backup.index(victoryrush_sprite.name),
"hardindex" : 4
},
"necromancer" : {
"name" : "necromancer",
"sprite" : necromancer_sprite,
"image" :  necromancer_sprite.image,
"rect" : necromancer_sprite.rect,
"index" : img_talent_array_name_backup.index(necromancer_sprite.name),
"hardindex" : 5
}
}
###END DICTIONARY ###



def talent_selected():
    print(player_choice)
    return player_choice #[player_choice] ##talent name corresponding with the number that is generated

def talent_select():
    global player_choice
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
        # global sample_selected
    talents_generated = False ##so that the selection menu doesnt open immediately
    sample_range = [] # sample_selected = []
    temp_list = [] 
    
    for x in range(len(talent_card_sprite_array)): #add the possible range to a list
        sample_range.append(x)
    print(sample_range)    
    sample_selected = random.sample(sample_range, 3) #get 3 random unique numbers from the list
    print(sample_selected)
    left_card = dynamic_select_group[sample_selected[0]] ##assign a string
    talent_card_left_group.add(Name[left_card]["sprite"]) ##add to group
    left = Name[left_card]["sprite"] #sprite
    left.left(0, 640) ##position
    temp_list.append(left.name)

    middle_card = dynamic_select_group[sample_selected[1]]
    talent_card_middle_group.add(Name[middle_card]["sprite"])
    middle = Name[middle_card]["sprite"]
    middle.middle(350, 640)
    temp_list.append(middle.name)
        
    right_card = dynamic_select_group[sample_selected[2]]
    talent_card_right_group.add(Name[right_card]["sprite"])
    right = Name[right_card]["sprite"]
    right.right(700, 640)
    temp_list.append(right.name)
    print(temp_list)
    print(right_card)
    print(talent_card_right_group)
    print(right) 
    
    talents_generated = True #start loop
    
    while talents_generated:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()    
        talent_card_right_group.draw(screen)
        talent_card_left_group.draw(screen)
        talent_card_middle_group.draw(screen)
        
        if  left.rect.collidepoint(mousepos()) and lmb() == True:
            player_choice = temp_list[0]
            talent_card_sprite_array.remove(left)
            dynamic_select_group.remove(left.name)
            talents_generated = False
            talent_selected()
            break
        if  middle.rect.collidepoint(mousepos()) and lmb() == True:
            player_choice = temp_list[1]
            talent_card_sprite_array.remove(middle)
            dynamic_select_group.remove(middle.name)
            talents_generated = False
            talent_selected()
            break
        if  right.rect.collidepoint(mousepos()) and lmb() == True:
            player_choice = temp_list[2]
            talent_card_sprite_array.remove(right)
            dynamic_select_group.remove(right.name)
            talents_generated = False
            talent_selected()
            break
        
        
        pygame.display.update()
        pygame.time.delay(50)

# def time_for_player_to_take_damage():
    

