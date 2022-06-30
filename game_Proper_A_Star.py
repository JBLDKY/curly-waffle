import pygame
import math
from queue import PriorityQueue
import numpy as np
from game_simplefunctions import *


WIDTH = 1600
HEIGHT = 900
# WIN = pygame.display.set_mode((1600, 900))
# pygame.display.set_caption("A* Path Finding Algorithm")
ROWS = 20
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)
class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows
        self.coords = [self.x, self.y]
    def get_pos(self):
        return self.row, self.col
    def is_closed(self):
        return self.color == RED
    def is_open(self):
        return self.color == GREEN
    def is_barrier(self):
        return self.color == BLACK
    def is_start(self):
        return self.color == ORANGE
    def is_end(self):
        return self.color == TURQUOISE
    def reset(self):
        self.color = WHITE
    def make_start(self):
        self.color = ORANGE
    def make_closed(self):
        self.color = RED
    def make_open(self):
        self.color = GREEN
    def make_barrier(self):
        self.color = BLACK
    def make_end(self):
        self.color = TURQUOISE
    def make_path(self):
        self.color = PURPLE
    
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))
    
    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # UP
            self.neighbors.append(grid[self.row - 1][self.col])
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False

def make_grid(rows, width):
	grid = []
	gap = width // rows
	for i in range(rows):
		grid.append([])
		for j in range(rows):
			spot = Spot(i, j, gap, rows)
			grid[i].append(spot)

	return grid

grid = make_grid(ROWS, WIDTH)

def h(p1, p2):
	x1, y1 = p1
	x2, y2 = p2
	return abs(x1 - x2) + abs(y1 - y2)

path_coords = []
def path_length_func(grid):
    for x in grid:
        if x.color == PURPLE:
            path_coords.append([x.x, x.y])
    
    
    
path_length = []
def reconstruct_path(came_from, current, grid):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        path_length.append(current)
        
def algorithm(grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos())
    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, grid)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        if current != start:
            current.make_closed()
    
    return False


def make_grid(rows):
    grid = [] #the grid
    gap =  64 #width of the squares
    for i in range(21): #20x10
        grid.append([])
        for j in range(20):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot) #enter the spot instance calls into the matrix

    return grid



#### BLACK SQUARE EXPANSION
    
def level_creation_preset_1(grid):              
    start = grid[18][5]
    start.make_start()
    end = grid[18][7]
    end.make_end()
    deadzone_coords = [[5, 18], [6, 18]]
    ####APPEND THE FIXED GRIDS TO generated_path_list WHEN DESIGNING A LEVEL
    # set_locs = [[grid[18][5].col, grid[18][5].row], [grid[18][6].col, grid[18][6].row], [grid[18][7].col, grid[18][7].row]]
    # generated_path_list.append(grid[18][5].row, grid[18][5].col)
    # generated_path_list.append(grid[18][6])
    # generated_path_list.append(grid[18][7])  # expansion_spot()

    ### SET AND DETECT BLACK BLOCKS
    for x in range(20): 
        grid[20][x].make_barrier()
        grid[x][10].make_barrier()
    
    grid[18][5].make_start()
    grid[18][7].make_end()
    
    
    for x in range(8):
        grid[x+12][6].make_barrier()
    for x in range(3):
        grid[x+12][5].make_barrier()
        grid[x+12][7].make_barrier()

    return start, end, deadzone_coords


black_grid = []
open_neighbors_list = []
lev_cre_open_neighbours = []
generated_path_list = []



def level_creation(grid):
    w = 20
    g = 3
    d = 1000
    for i in range(20): ### add blacks quares to the black grid list
        for x in grid[i]:
            # if x.color == BLACK and x not in black_grid:
            if x.color == BLACK and 1 < x.row < 17 and 1 < x.col < 8 and x not in black_grid:
                black_grid.append(x)
    ### EXPAND BLACK BLOCKS 
    
    lev_cre_open_neighbours = []
    for x in black_grid: #OLD CONDITIONS: if 1 < x.row < 17 and 1 < x.col < 8:
        if 1 < x.row < 17 and 1 < x.col < 8:
            x.update_neighbors(grid)
            if x.neighbors != []:
                lev_cre_open_neighbours.append(x.neighbors)
    
    
    
    open_neighbors_list = [] #new list that will be appended instance objects of possible new black squares
    
    if len(lev_cre_open_neighbours) > 0: #bugcatch
        open_neighbors_list = np.concatenate(lev_cre_open_neighbours) #2d list => 1d list

    if [] in open_neighbors_list: #if a square has no neghbours it appends []..
        open_neighbors_list.remove([]) #therefore, gotta remove the []s

    weight_list = [] #new list for calculating weights
    open_neighbors_list = sorted(open_neighbors_list, key=lambda x: x.row, reverse=False) #sort by ascending x coordinate
    
    for x in range(len(open_neighbors_list)): #creating a weight list of equal length to the available square list
        weight_list.append((w - open_neighbors_list[x].row) * (w - open_neighbors_list[x].row) * (w - open_neighbors_list[x].row) * (w - open_neighbors_list[x].row)) #the lower the x coordinate, the higher the weight
        #w is currently 20, since the list is sorted in ascending order, the weight of the lower x coordinates should be higher
    
    for x in range(g): #grow g black squares at a time (currently 5)
            winning_spots = random.choices(open_neighbors_list, weights = weight_list, k = 1) #list of winning neighbour
            expansion_spot =  winning_spots[0] #just taking the winner out of the list
            expansion_spot.make_barrier() #draw a black square on the winning location
            if expansion_spot not in black_grid: #if the square is not already in the list of black squares
                black_grid.append(expansion_spot) #add the new black square to the list of black squares

    #debugging..
    x_coord_list = []
    for x in range(len(open_neighbors_list)):
        x_coord_list.append(open_neighbors_list[x].row)
    
#### THIS I CALLED TO START THE PATHMAKING PROCESS   
def get_path():
    generated_path_list = [] 
    grid = make_grid(20)
    start, end, deadzone_coords = level_creation_preset_1(grid)
    
    # paff_to_the_norff = [deadzone_coords]

    while len(generated_path_list) < 34:
        level_creation(grid) 
        for row in grid:
            for spot in row:
                spot.update_neighbors(grid)

        algorithm(grid, start, end) 
        
        generated_path_list = []
        # generated_path_list.extend(deadzone_coords)
        
        # print(generated_path_list)
        for i in range(20):
            for x in grid[i]:
                if x.color == PURPLE or x.color == TURQUOISE or x.color == ORANGE:

                    generated_path_list.append([x.col, x.row])
        generated_path_list.extend(deadzone_coords)
        # generated_path_list.append(deadzone)
    return generated_path_list


#### END BLACK SQUARE EXPANSON













