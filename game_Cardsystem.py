import pygame
from pygame.locals import *
import sys
import numpy as np
import pygame.image
import pygame.key
pygame.init()
import math
import random
import pygame.mouse
from game_Constants import *
# from mousefunctionality import lmb
from game_Proper_A_Star import *

def mousepos():# always get mouseposition
    return pygame.mouse.get_pos()


path_detect_list = []
path_detect_list_possible_start = []
build_grid = []
grid_exists = None
index = 0
index2 = 0
card_to_build = None
buildings = [ [ 0 for i in range(20)] for j in range (10)]
generated_path_list = get_path() #### THIS IS THE RAW PATH FROM A* // PAFF TO THE NORFF
grid_path_list_with_instances = []
# grid_path_list_with_instances_coords = []
start_point = None
class card():
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = image.get_rect()
        self.x_pos = 0 
        self.y_pos = 0
        self.rect.center = [self.x_pos, self.y_pos]
        self.mouseover = False
        self.index = 0
        self.index2 = 0
        self.width = self.rect[2]
        self.height = self.rect[3]
        self.currently_dragged = False
    def setloc(self, x, y):
        self.rect.center = [x, y]
        
        ####VELOCITY HOVER SYSTEM
    def hover(self):
        self.mouseover = True ##the mouseover stuff is to reset the velocity value upon re-hovering the same card
        if self.mouseover == True:
            self.index = 0
            
        speed = [-8, -8, -8, -7, -6, -5, -4, -4, -3] # velocity array
        if self.rect.center[1] == 880: #if card is in standard position
            self.index = 0 #set the velocity index to 0
            
        if self.rect.center[1] > 825: #if the card is between standard pos and 825x, start increasing the velocity
            if self.index < 8:
                self.index += 1
            x = math.floor(self.index) #this is onyl necessary if you want to increase with floated values

            velo = speed[x] #select from the array with an ever increasing index x
            self.rect.move_ip(0, velo) #move the card up 

    def unhover(self): ##see comments for def hover(self.)
        self.mouseover = False 
        if self.mouseover == False:
            self.index2 = 0
                
        speed = [6, 6, 6, 6, 6, 5, 4, 4, 3]
        if self.rect.center[1] <= 825:
            self.index2 = 0
            
        if self.rect.center[1] < 880:
            if self.index2 < 8:
                self.index2 += 1
            x = math.floor(self.index2)
            
            velo = speed[x]
            self.rect.move_ip(0, velo)
        
        if self.rect.center[1] > 880: #due to variable movement upon hovering, if the card reachesa stationary position that is not equal to the standard position, this will align it with the rest
            self.rect.center = [self.rect.center[0], 880]
            
            
    def drag(self):
        if self.currently_dragged == True:
            a = mousepos()[0]
            b = mousepos()[1]
            self.rect.center = [a, b]
            
    def reset_drag(self):
        i = player_card_hand.index(self)
        x_pos = cards_x_coords[i]
        if self.rect.center[1] <= 820 and self.currently_dragged != True:
            self.rect.center = [x_pos, 880]
            
        
            #array for images for cards
player_card_deck = [img_treescard, img_rockscard] 
            #array for card ID as a string
player_card_type = ["trees", "rocks"]
            #array for the cards that the player is holding in his hand
player_card_hand = []

def roll_cards_t1(i):
    cards_am = len(player_card_hand) #amount of cards the player has
    cards_sp = 15 - cards_am #space in the players" hand
    cards_drop = [] #temporary array for generating dropped cards

    #generate card drops, this might have to be moved somewhere else and add a weight system
    for x in range(i):  #loopyloop
        r = random.randint(0,len(player_card_deck) - 1) #random int that is used twice
        r_image = player_card_deck[r] #this has to do with randomizing drops, this needs work whne new cards are added
        r_type = player_card_type[r]
        cardt1 = card(r_image, r_type) #calls a class to create a card instance NOT A SPRITE INSTANCE
        cards_drop.append(cardt1) #array of the rolled cards

    #fixes player"s hands space
    if cards_sp < len(cards_drop):  #if free space is smaller than amoutn of cards dropped
        overflow = cards_sp - len(cards_drop) #new variable overflow = amount of cards to burn
        cards_out = (overflow)*-1 #make the amount of cards to be burned a positive integer
        for x in range(cards_out): #if there are cards to be burned, pop the oldest card (FIFO)
            player_card_hand.pop(0)

    player_card_hand.extend(cards_drop) #finally add the dropped cards to the player"s hand
    sort_cards() #sort the player"s hand (cards move to the left of the screen)

cards_x_coords = [50, 150, 250, 350, 450, 550, 650, 750, 850, 950, 1050, 1150, 1250, 1350, 1450, 1550]
cards_y_coords = [880]
def sort_cards():
    x_coords = []
    y_coords = []
    x_pos = 50
    y_pos = 880
    for x in player_card_hand: 
        x.setloc(x_pos, y_pos) #moves the cards over to the left of the screen
        x_pos += 100 #every th card is 100px to the right of the previous
    
        x_coords.append(x_pos) #calculated the x Coords of the cards for hovering purposes

def draw_cards():
    for x in player_card_hand: #every card
        screen.blit(x.image, x.rect) #draws the cards
        
def card_index():
    for x in range(len(player_card_hand)): #as many cards as the player has in his hand do:
        if player_card_hand[x].rect.collidepoint(mousepos()) == True: #if mouseover
            return int(x) #return the index of the hovered card
        else: player_card_hand[x].mouseover = False #else set mouseover to false
        
        
def mouseover_cards():
    x = card_index() #get the index of the hovered over card
    if x != None and x != str and player_card_hand[x].rect.collidepoint(mousepos()) == True: #if mouseovering card returns a value and mouseposition is on the card hitbox
        player_card_hand[x].hover() #trigger the function that shows what hard is covered
        
    for y in range(len(player_card_hand)):
        if y != x:
            player_card_hand[y].unhover() #if card is not hovered, trigger function that reset the card to the standard position
    
def general_card_things():
    for x in player_card_hand:
        x.reset_drag()

def drag_card():
    # left = pygame.mouse.get_pressed()[0] ### gonna just use the function to fix an erroer
    any_draggers = [] #array to index the card that is currently being dragged

    for x in player_card_hand: #loop thru hadn
        if pygame.mouse.get_pressed()[0] != True: #if no mousebutton is pressed
            x.currently_dragged = False #all cards are marked as not being dragged
        any_draggers.append(x.currently_dragged) #either way, append a bool to the list for indexing the card that is being dragged

    for x in player_card_hand:    #loop through hand again
        if any_draggers.count(True) > 0: #if a card is marked as being dragged in the list
            player_card_hand[any_draggers.index(True)].drag() #drag said card
            return #also stop the function because the following will select  anew card to be dragged

        if x.rect.collidepoint(mousepos()) == True and pygame.mouse.get_pressed()[0] == True:
            x.currently_dragged = True


def card_functionality():
    card_index()
    draw_cards()
    mouseover_cards()
    drag_card()
    general_card_things()
    highlight_grid()
    draw_buildings()
    # highlight_grid2()
    # draw_grid()
####BUILD GRID SECTION

# path = get_path()

class grid():
    path_list = get_path()
    
    def __init__(self, x_pos, y_pos, path_x, path_y):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.image = None
        self.rect = pygame.Rect(self.x_pos, self.y_pos, 64, 64)
        self.mouseover = False
        self.path = None 
        self.path_x = path_x
        self.path_y = path_y
        self.left = None
        self.right = None
        self.up = None
        self.down = None
        self.grid_type = None
        self.path_xy = []
        self.line = None
        self.start_point = None
        self.quarter = None
        self.coords_grabbed = None
        self.neighbours = []
        self.direction = None
        self.loc = [self.path_y, self.path_x]
        self.monster = None
        self.spawntype = "any"
    def orange_border(self):
        if self.coords_grabbed == True:
            pygame.draw.rect(screen, "orange", self.rect)
    def blue_border(self):
        if self.path == True:
            pygame.draw.rect(screen, "blue", self.rect)
    def green_border(self):
        if self.coords_grabbed == True:
            pygame.draw.rect(screen, "green", self.rect)

    def scan(self):
        if self.start_point == True:
            # print(self.loc)
            
            # grid_path_list_with_instances_coords.append(self)
            if  self.path_y < 5 and self.path_x < 10:
                self.quarter = "topleft"
                if self.grid_type == "ud":
                    next_block = build_grid[self.path_y + 1][self.path_x]
                if self.grid_type == "lr":
                    next_block = build_grid[self.path_y][self.path_x - 1]

            if  self.path_y >= 5 and self.path_x < 10:
                self.quarter = "bottomleft"
                if self.grid_type == "ud":
                    next_block = build_grid[self.path_y + 1][self.path_x]
                if self.grid_type == "lr":
                    next_block = build_grid[self.path_y][self.path_x + 1]

            if  self.path_y < 5 and self.path_x >= 10:
                self.quarter =  "topright"
                if self.grid_type == "ud":
                    next_block = build_grid[self.path_y - 1][self.path_x]
                if self.grid_type == "lr":
                    next_block = build_grid[self.path_y][self.path_x - 1]

            if  self.path_y >= 5 and self.path_x >= 10:
                self.quarter = "bottomright"
                if self.grid_type == "ud":
                    next_block = build_grid[self.path_y - 1][self.path_x]
                if self.grid_type == "lr":
                    next_block = build_grid[self.path_y][self.path_x + 1]

            grid_path_list_with_instances.append(self)
            # grid_path_list_with_instances.append(next_block)

        if self.start_point != True:   
            if self.path_y + 1 < 10 and build_grid[self.path_y + 1][self.path_x].path == True and build_grid[self.path_y + 1][self.path_x].coords_grabbed != True:
                next_block = build_grid[self.path_y + 1][self.path_x]

            if build_grid[self.path_y - 1][self.path_x].path == True and build_grid[self.path_y - 1][self.path_x].coords_grabbed != True:
                next_block = build_grid[self.path_y - 1][self.path_x]

            if build_grid[self.path_y][self.path_x + 1].path == True and build_grid[self.path_y][self.path_x + 1].coords_grabbed != True:
                next_block = build_grid[self.path_y][self.path_x +1]
                
            if build_grid[self.path_y][self.path_x - 1].path == True and build_grid[self.path_y][self.path_x - 1].coords_grabbed != True:
                next_block = build_grid[self.path_y][self.path_x -1]

        self.coords_grabbed = True
        
        grid_path_list_with_instances.append(next_block)
        
        if len(grid_path_list_with_instances) == len(path_detect_list):
            # print(len(grid_path_list_with_instances))
            # print(len(path_detect_list))
            walking_coords()
        else: next_block.scan()
        
    def am_i_a_path(self, generated_path_list):
        if self.loc in generated_path_list:
            self.path = True
            path_detect_list.append(self)
            
    def what_image_am_i(self):
        if self.up and self.down == True: #UP DOWN
            self.image = img_path_list[5]
            self.grid_type = "ud"
        if self.right and self.left == True: #LEFT RIGHT
            self.image = img_path_list[4]
            self.grid_type = "lr"
        if self.up == True and self.left == True: #UP LEFT
            self.image = img_path_list[2]
            self.grid_type = "ul"
        if self.up == True and self.right == True: #UP RIGHT
            self.image = img_path_list[3]
            self.grid_type = "ur"
        if self.down == True and self.left == True: #DOWN LEFT
            self.image =img_path_list[1]
            self.grid_type = "dl"
        if self.down == True and self.right == True: #DOWN RIGHT
            self.image =img_path_list[0]
            self.grid_type = "dr" 

    def what_path_am_i(self):
        if self.path == True:
            if self.path_y > 0 and self.path_y < 9 and build_grid[self.path_y - 1][self.path_x].path == True and build_grid[self.path_y + 1][self.path_x].path == True: #path beneath is true?
                self.up = True
                self.down = True
                self.left = False
                self.right = False
                # self.image = img_path_list[5]
            if self.path_y > 0 and self.path_x > 0 and build_grid[self.path_y - 1][self.path_x].path == True and self.path_y < 10 and build_grid[self.path_y][self.path_x - 1].path == True:
                #UP LEFT
                self.up = True
                self.down = False
                self.left = True
                self.right = False
                # self.image = img_path_list[1]
            if self.path_y > 0 and self.path_x < 19 and build_grid[self.path_y - 1][self.path_x].path and build_grid[self.path_y][self.path_x + 1].path == True:
                #UP RIGHT
                self.up = True
                self.down = False
                self.left = False
                self.right = True
                # self.image = img_path_list[0]

            if self.path_x < 19 and self.path_x > 0 and build_grid[self.path_y][self.path_x + 1].path and build_grid[self.path_y][self.path_x - 1].path == True:
                #RIGHT LEFT
                self.up = False
                self.down = False
                self.left = True
                self.right = True
                # self.image = img_path_list[5]

            if self.path_y < 9 and self.path_x > 0 and build_grid[self.path_y + 1][self.path_x].path and build_grid[self.path_y][self.path_x - 1].path == True:
            #DOWN LEFT
                self.up = False
                self.down = True
                self.left = True
                self.right = False
                # self.image = img_path_list[2]

            if self.path_y < 9 and self.path_x < 19 and build_grid[self.path_y + 1][self.path_x].path and build_grid[self.path_y][self.path_x + 1].path == True:
            #DOWN RIGHT
                self.up = False
                self.down = True
                self.left = False
                self.right = True
                
            self.rect = pygame.Rect(self.x_pos, self.y_pos, 64, 64)

            
        
        


grid_exists = None

def create_grid():
    global grid_exists
    d = 0
    c = 0 
    x_pos = 0
    y_pos = 96
    
    if len(build_grid) == 0: #prevents the function from triggering more than once
        for x in range(11): # adds a second dimension to the array
            build_grid.append([]) 
            
            
        for x in range(200): # adds 200 "grids"  to the grid array where u can build stuff
            griddy = grid(x_pos, y_pos, c, d)
            build_grid[d].append(griddy)
            # build_grid[d][c].update_rect(x_pos, y_pos)
            x_pos += 64
            
            c += 1  #increase c by 1 everytime a grid is added to the matrix
            
            if c == 20: #once 20 grids are added horizontally, go to the next row
                d += 1
                c = 0
                y_pos += 64
                x_pos = 0
            grid_exists = True   #prevents function from triggering again


def draw_grid():
    for i in range(10):
        for x in build_grid[i]:
            pygame.draw.rect(screen, "white", x.rect, 1)
            
def grid_index():
    for i in range(10):
        for x in build_grid[i]:
            if x.rect.collidepoint(mousepos()) == True:
                gii1 = build_grid[i].index(x)
                gii2 = i

                if gii1 != None and gii2 != None:
                    gi = [gii1, gii2]
                    return gi
                else: return [0, 0]
                    

def highlight_grid():
    if grid_index() != None:
        gi1 = grid_index()[0]
        gi2 = grid_index()[1]
        x = build_grid[gi2][gi1].rect.collidepoint(mousepos())
        y = build_grid[gi2][gi1].rect
        
        if x == True and pygame.mouse.get_pressed()[0]:
            pygame.draw.rect(screen, "yellow", y, 1)
    else: gi1, gi2 = 0, 0
    
# def highlight_grid2():
#     for i in range(len(build_grid)):
#         for x in range(len(build_grid[i])):
#             if build_grid[i][x].path == True:
#                 pygame.draw.rect(screen, "orange", build_grid[i][x].rect, 1)
        

def build_building():
    if grid_index() != None:
        bi1 = grid_index()[0]
        bi2 = grid_index()[1]
    else: bi1, bi2 = 0, 0
    card_to_build = 0
    
    for x in player_card_hand:
        if x.currently_dragged == True and grid_index() != None:
            card_to_build = x.type
            
            return [card_to_build, bi1, bi2, player_card_hand.index(x)]
                    
                
        
def builder_building(type, bi1, bi2, pop): 
    if type != 0:
        buildings[bi2][bi1] = type
        player_card_hand.pop(pop)
        sort_cards()
        

                    

# def grid_coords_func():
grid_coords = [[], [], [], [], [], [], [], [], [], [], []]
for k in range(10):
    for j in range(20): # adds a second dimension to the array
        a = str([j])+str([k])
        grid_coords[k].append(a) 
            
            
            
rocklist = []
def draw_buildings():
    for j in range(10):
        for x in buildings[j]:
            if x == "rocks":
                rocks = buildings[j].index(x)
                rocklist.append([img_rocks_building, (build_grid[j][rocks])])
                buildings[j][rocks] = "built"
            if x == "trees":
                trees = buildings[j].index(x)
                rocklist.append([img_trees_building, (build_grid[j][trees])])
                buildings[j][trees] = "built"
    screen.blits(rocklist)               
    


########## LETS GET THIS PATH BOI // THIS IS FOR FINDING THE GENERATED PATH

def path_detect():
    global start_point
    if len(path_detect_list) <= 0:
        for i in range(len(build_grid)):
            for x in build_grid[i]:
                x.am_i_a_path(generated_path_list) #appending to path_detect_list happens here
                
                # x.what_path_am_i()
                # x.what_image_am_i()
    print(path_detect_list)
    for x in path_detect_list:
        x.what_path_am_i()
        x.what_image_am_i()
        
        if x.grid_type == "ud" or x.grid_type == "lr":
            path_detect_list_possible_start.append(x)
    start_point = random.choice(path_detect_list_possible_start)
    start_point.start_point = True
    start_point.scan()
    print("path_detect is running!")
    #set_start
    # x = random.choice(path_detect_list_possible_start)           
    # x.start_point = True
# def set_start(x): #randomly generate a start point for the loop the character walks in
#     if x.start_point == None: #if no square in the game is marked as start point yet:
#         x = random.choice(path_detect_list) # x = a random square in the game that has a path
#         if x.grid_type == "lr" or x.grid_type == "ud": #if the path is also a straight line (lr" = left-right, ud" = up-down)
#             x.start_point = True #set the first random square object that is a straight path to be the start point
#             start_point = x
#             return x #return the instance of this square for possibly further processing
    
#         set_start(x) #if the path that was handed to the function is not "lr" or "ud", run this function again
#     else: return x

def draw_path():
    if len(path_detect_list) <= 0:
        path_detect()
    # for x in path_detect_list:
        # x.what_path_am_i()
        # x.what_image_am_i()
        # x.orange_border()
        # x.blue_border()
        # if x.image != None:
    for x in grid_path_list_with_instances:
        screen.blit(x.image, x.rect)
            
####BELOW IS FOR MAKING THE CHARACHTER WALK######
# def path_walk(start_point): 
#     start_line = pygame.draw.line(screen, "black", (start_point.rect.midright), (start_point.rect.midleft))
#     start_line_coords = start_point.rect.clipline(start_line)
# routed_grid = []

# def path_start(x): 
#     if x != None:
#         start_point = x #this is the instance object that is marked as the start point
#         start_point.scan()

    #up = index1 -1
    #down = index1 +1
#left = index2 -1
#right = index2 +1


walking_coords_list = []
def walking_coords():
    i = 0
    a = grid_path_list_with_instances
    paffs = len(grid_path_list_with_instances) - 1
    for x in range(len(a)):
        pos1 = a[x].rect.center
        if x == paffs:
            x = (0) 
        pos2 = a[x+1].rect.center
    
        if pos1[0] > pos2[0]:
            for x in range(65):
                walking_coords_list.append([pos1[0]-x, pos1[1]])
        if pos1[0] < pos2[0]:
            for x in range(65):
                walking_coords_list.append([pos1[0]+x, pos1[1]])
        if pos1[1] > pos2[1]:
            for x in range(65):
                walking_coords_list.append([pos1[0], pos1[1]-x])
        if pos1[1] < pos2[1]:
            for x in range(65):
                walking_coords_list.append([pos1[0], pos1[1]+x])

    # walking_coords_list.append(walking_coords_list[0])
    # print(walking_coords_list)
    # print(start_point.rect.center)
    # print(start_point.grid_type)
    
    
    # grid_path_list_with_instances.reverse()
    # grid_path_list_with_instances_coords.reverse()
    # for x in range(len(grid_path_list_with_instances)):
    #     cur_path = grid_path_list_with_instances[x-1]
    #     nex_path = grid_path_list_with_instances[x]


    #     print(cur_path.rect.center)
    #     print(cur_path.loc)
        # print(f"length of grid_path_list_with_instances: {len(grid_path_list_with_instances)}")
        # print(f"length of real path: {len(generated_path_list)}")
        # if cur_path[0] == nex_path[0]:
        #     for x in range
        
        
        
        
# def path_route(x):
#     start_point = x
#     start_point.scan()



# def path_route2(current_block, index1, index2, numpy_build_grid, prev_block):

#     if index1 < 5 and index2 < 10: #topleft
#         if current_block.left == True and prev_block != build_grid[current_block.path_y][current_block.path_x-1]:
#             next_block = build_grid[current_block.path_y][current_block.path_x-1]
            
#         if current_block.down == True and prev_block != build_grid[current_block.path_y+1][current_block.path_x]:
#             next_block = build_grid[current_block.path_y+1][current_block.path_x]
            
#         if current_block.right == True and prev_block != build_grid[current_block.path_y][current_block.path_x+1]:
#             next_block = build_grid[current_block.path_y][current_block.path_x+1]
            
#         if current_block.up == True and prev_block != build_grid[current_block.path_y-1][current_block.path_x]:
#             next_block = build_grid[current_block.path_y-1][current_block.path_x]
            

#     if index1 >= 5 and index2 < 10: #bottomleft
#         if current_block.down == True and prev_block != build_grid[current_block.path_y+1][current_block.path_x]:
#             next_block = build_grid[current_block.path_y+1][current_block.path_x]
            
#         if current_block.right == True and prev_block != build_grid[current_block.path_y][current_block.path_x+1]:
#             next_block = build_grid[current_block.path_y][current_block.path_x+1]
            
#         if current_block.up == True and prev_block != build_grid[current_block.path_y-1][current_block.path_x]:
#             next_block = build_grid[current_block.path_y-1][current_block.path_x]
            
#         if current_block.left == True and prev_block != build_grid[current_block.path_y][current_block.path_x-1]:
#             next_block = build_grid[current_block.path_y][current_block.path_x-1]

#     if index1 >= 5 and index2 >= 10: #bottomright
#         if current_block.right == True and prev_block != build_grid[current_block.path_y][current_block.path_x+1]:
#             next_block = build_grid[current_block.path_y][current_block.path_x+1]
            
#         if current_block.up == True and prev_block != build_grid[current_block.path_y-1][current_block.path_x]:
#             next_block = build_grid[current_block.path_y-1][current_block.path_x]
            
#         if current_block.left == True and prev_block != build_grid[current_block.path_y][current_block.path_x-1]:
#             next_block = build_grid[current_block.path_y][current_block.path_x-1]
            
#         if current_block.down == True and prev_block != build_grid[current_block.path_y+1][current_block.path_x]:
#             next_block = build_grid[current_block.path_y+1][current_block.path_x]
            

#     if index1 < 5 and index2 >= 10: #topright
#         if current_block.up == True and prev_block != build_grid[current_block.path_y-1][current_block.path_x]:
#             next_block = build_grid[current_block.path_y-1][current_block.path_x]
            
#         if current_block.left == True and prev_block != build_grid[current_block.path_y][current_block.path_x-1]:
#             next_block = build_grid[current_block.path_y][current_block.path_x-1]
            
#         if current_block.down == True and prev_block != build_grid[current_block.path_y+1][current_block.path_x]:
#             next_block = build_grid[current_block.path_y+1][current_block.path_x]
            
#         if current_block.right == True and prev_block != build_grid[current_block.path_y][current_block.path_x+1]:
#             next_block = build_grid[current_block.path_y][current_block.path_x+1]
            

#     prev_block = current_block
#     routed_grid.append(next_block)
#     print(routed_grid)
#     print(f"length: {len(routed_grid)}")
#     print(generated_path_list)
#     x = len(routed_grid) - 1
#     print(routed_grid[x].path_x)
#     print(routed_grid[x].path_y)
#     # indices = np.where(numpy_build_grid == next_block)
#     index1 = next_block.path_y
#     index2 = next_block.path_x

#     if len(routed_grid) != len(generated_path_list):
#         path_route(next_block, routed_grid[x].path_y, routed_grid[x].path_x, numpy_build_grid, prev_block)

#     return 
# #    if index1 < 5 and index2 < 10: #topleft
# #         if current_block.left == True and prev_block.left == True:
# #             next_block = build_grid[current_block.path_y][current_block.path_x-1]
# #         elif current_block.down == True and prev_block.down == True:
# #             next_block = build_grid[current_block.path_y+1][current_block.path_x]
# #         elif current_block.right == True and prev_block.right == True:
#             next_block = build_grid[current_block.path_y][current_block.path_x+1]
#         elif current_block.up == True and prev_block.up == True:
#             next_block = build_grid[current_block.path_y-1][current_block.path_x]

#     if index1 >= 5 and index2 < 10: #bottomleft
#         if current_block.down == True and prev_block.down == True:
#             next_block = build_grid[current_block.path_y+1][current_block.path_x]
#         elif current_block.right == True and prev_block.right == True:
#             next_block = build_grid[current_block.path_y][current_block.path_x+1]
#         elif current_block.up == True and prev_block.up == True:
#             next_block = build_grid[current_block.path_y-1][current_block.path_x]
#         elif current_block.left == True and prev_block.left == True:
#             next_block = build_grid[current_block.path_y][current_block.path_x-1]

#     if index1 >= 5 and index2 >= 10: #bottomright
#         if current_block.right == True and prev_block.right == True:
#             next_block = build_grid[current_block.path_y][current_block.path_x+1]
#         elif current_block.up == True and prev_block.up == True:
#             next_block = build_grid[current_block.path_y-1][current_block.path_x]
#         elif current_block.left == True and prev_block.left == True:
#             next_block = build_grid[current_block.path_y][current_block.path_x-1]
#         elif current_block.down == True and prev_block.down == True:
#             next_block = build_grid[current_block.path_y+1][current_block.path_x]

#     if index1 < 5 and index2 >= 10: #topright
#         if current_block.up == True and prev_block.up == True:
#             next_block = build_grid[current_block.path_y-1][current_block.path_x]
#         elif current_block.left == True and prev_block.left == True:
#             next_block = build_grid[current_block.path_y][current_block.path_x-1]
#         elif current_block.down == True and prev_block.down == True:
#             next_block = build_grid[current_block.path_y+1][current_block.path_x]
#         elif current_block.right == True and prev_block.right == True:
#             next_block = build_grid[current_block.path_y][current_block.path_x+1]
