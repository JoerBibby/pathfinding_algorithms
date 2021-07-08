import operator
import time
import pygame
from tkinter import *
from tkinter import ttk

# constants
blue = (0, 0, 255)
white = (255, 255, 255)
gray = (152, 152, 152)
green = (0, 255, 0)
black = (0, 0, 0)
yellow = (255, 255, 0)
first_node_x = 150
first_node_y = 150
second_node_x = 450
second_node_y = 450
display_width = 600
display_height = 600
block_size = 10

cols = 60
rows = 60

# pygame.display.init()
# dis = pygame.display.set_mode((display_height, display_width))
pygame.display.init()
dis = pygame.display.set_mode((display_height, display_width))

# define cell
class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.adjacent = []
        self.visited = False
        self.previous = None
        self.path_length = 10000
        self.current = False
        self.walled = False
        self.color = None

    def unvisited_render(self):
        if self.visited == False:
            # draw square at position * 10, becasue the row and column size is 10 display units
            pygame.draw.rect(dis, gray, [self.x * block_size, self.y * block_size, block_size, block_size])

    def fill(self, color):
        pygame.draw.rect(dis, color, [self.x * block_size, self.y * block_size, block_size, block_size])
        self.color = color

    def add_adjacents(self):
        x = self.x
        y = self.y
        if x < cols - 1 and grid[x + 1][y].walled == False:
            self.adjacent.append(grid[x + 1][y])
        if x > 0 and grid[x -1][y].walled == False:
            self.adjacent.append(grid[x - 1][y])
        if y < rows - 1 and grid[x][y + 1].walled == False:
            self.adjacent.append(grid[x][y + 1])
        if y > 0 and grid[x][y - 1].walled == False:
            self.adjacent.append(grid[x][y - 1])


# create 60 * 60 matrix filled with 0s, then fill it with instances of Cell
grid = [0 for i in range(cols)]

for i in range(cols):
    grid[i] = [0 for i in range(rows)]

for i in range(cols):
    for j in range(rows):
        grid[i][j] = Cell(i, j)

for i in range(cols):
    for j in range(rows):
        grid[i][j].fill(gray)
pygame.display.update()

starting_node = None
finishing_node = None



def djikstra(current, target):
    # start at current node
    # work out adjacent path lengths and add adjacent cells to unvisited
    # mark current node as visited
    # choose new current node - node in unvisited with shortest path length
    # repeat
    # NEED TO SET CURRENT PATH LENGTH TO 0 AT THE START OF THIS
    # others dont need an arbitrarily large path length because they are only added to unvisited when thier actual path
    # lengths are computed
    start_node = current
    end_node = target
    #render



    current.fill(blue)
    target.fill(blue)
    current.color = blue
    target.color = blue
    pygame.display.update()
    #render
    found = False
    unvisited = []
    visited = []
    current.path_length = 0

    while found is not True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                found = True

        # add adjacent cells
        current.add_adjacents()


        # compute adjacent cells and add to unvisited
        for i in current.adjacent:
            i.path_length = current.path_length + 1
            if i.previous == None:
                i.previous = current
            if i.visited is False:
                unvisited.append(i)

        # sort univisted and set lowest path as current
        #unvisited.sort(key=lambda cell: cell.path_length)

        # remove all visited items from unvisited so we don't get repeat current nodes
        visited.append(current)
        current.visited = True
        current.fill(green)
        # if len(unvisited) > 1:
        #     unvisited.remove(current)
        # probably shouldnt be looping through all univisted every display update
        for i in unvisited:
            if i.visited == True:
                unvisited.remove(i)
        # for i in visited:
        #     if i in unvisited:
        #         unvisited.remove(i)
        # possibly dont need to draw every single visited cell every display update?
        for i in visited:
            # if rect is not start or end node or already coloured green
            if i.color is not green and not blue:
                i.fill(green)
                i.color = green
        start_node.fill(blue)
        end_node.fill(blue)

        pygame.display.update()
        current = unvisited[0]

        if current == target:
            found_node = current
            for i in range(0, current.path_length):
                if current.color is not blue:
                    current.fill(yellow)
                pygame.display.update()

                current = current.previous

            found = True

            print('found target node at : ', found_node.x, found_node.y)



def djikstra_start():
    try:

        start = starting_node
        end = finishing_node

    except ValueError:
        pass
    # pass tk window entries as arguments
    djikstra(start, end)


def draw_walls():
    fin = False
    while fin is False:
        for event in pygame.event.get():
            if pygame.mouse.get_pressed()[0]:
                try:

                    x = round(event.pos[0]/block_size)
                    y = round(event.pos[1]/block_size)
                    grid[x][y].fill(black)
                    grid[x][y].walled = True
                    pygame.display.update()
                except AttributeError:
                    pass
            elif event.type == pygame.KEYDOWN:
                try:
                    fin = True
                except AttributeError:
                    pass
    return





def place_nodes():
    nodes = []
    fin = False
    while fin == False:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                try:
                    x = round(event.pos[0]/block_size)
                    y = round(event.pos[1]/block_size)
                    grid[x][y].fill(blue)
                    nodes.append(grid[x][y])
                    pygame.display.update()
                except AttributeError:
                    pass
            if event.type == pygame.KEYDOWN:
                try:
                    fin = True
                except AttributeError:
                    pass
    global starting_node
    starting_node = nodes[0]
    global finishing_node
    finishing_node = nodes[1]
    if starting_node is not None:
        print(starting_node)
    if finishing_node is not None:
        print(finishing_node)





root = Tk()
root.geometry('350x200')
root.title('Algorithm Viualizer')
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
ttk.Button(mainframe, text="start", command=djikstra_start).grid(column=1, row=5, sticky=W)
ttk.Label(mainframe, text="Note: click on pygame window to select it after pressing button,").grid(column=1, row=1, sticky=W)
ttk.Label(mainframe, text="press any key to exit draw mode after placing nodes/walls").grid(column=1, row=2, sticky=W)
# start_x = IntVar()
# start_x_entry = ttk.Entry(mainframe, width=5, textvariable=start_x)
# start_x_entry.grid(column=2, row=1)
# start_y = IntVar()
# start_y_entry = ttk.Entry(mainframe, width=5, textvariable=start_y)
# start_y_entry.grid(column=3, row=1)
# end_x = IntVar()
# end_x_entry = ttk.Entry(mainframe, width=5, textvariable=end_x)
# end_x_entry.grid(column=2, row=2)
# end_y = IntVar()
# end_y_entry = ttk.Entry(mainframe, width=5, textvariable=end_y)
# end_y_entry.grid(column=3, row=2)
# ttk.Label(mainframe, text="start x, start y").grid(column=1, row=1)
# ttk.Label(mainframe, text="end x, end y").grid(column=1, row=2)
ttk.Button(mainframe, text="draw walls", command=draw_walls).grid(column=1, row=4, sticky=W)
ttk.Button(mainframe, text="place nodes", command=place_nodes).grid(column=1, row=3, sticky=W)

root.mainloop()

time.sleep(5)




# djikstra(start_node)
pygame.quit()
# quit()


# -- more detailed pseudocode --
# take node1 - apply length 1 to all adjacent nodes
# place node1 in visited []
# choose next current node from smallest length in univisted []
# apply length = length + 1 to all adjacent nodes
# place node in visited
# reorder unvisited and pick new current node








# loop()
# pygame.quit()
# quit()