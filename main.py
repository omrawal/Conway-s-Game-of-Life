import pygame
import random

pygame.init()

BLACK = (0,0,0)
GREY = (128,128,128)
YELLOW = (255,255,0)

WIDTH , HEIGHT = 800,800
TILE_SIZE = 20
GRID_WIDTH = WIDTH // TILE_SIZE
GRID_HEIGHT = HEIGHT // TILE_SIZE
FPS = 60

screen = pygame.display.set_mode((WIDTH,HEIGHT))

clock = pygame.time.Clock()

def gen(num):
    # generate random positions
    return set([(random.randrange(0,GRID_HEIGHT), random.randrange(0,GRID_WIDTH)) for _ in range(num) ])

def adjust_grid(positions):
    # loop through live cells and check that and neighbours state not all cells
    all_neighbours = set() # only live and die cells can be the one who are direct neighbours of live cells
    new_positions = set() # new live cells at next step

    for position in positions:
        neighbours = get_neighbours(position)
        all_neighbours.update(neighbours)
    
        # get only live neighbours of all neighbours
        neighbours = list(filter(lambda x: x in positions, neighbours))

        # if current has 2 or 3 neighbours it servives for next round
        if(len(neighbours) in [2,3]):
            new_positions.add(position)

    # looping through neighbours of live cells     
    for position in all_neighbours:
        neighbours = get_neighbours(position)
        neighbours = list(filter(lambda x: x in positions, neighbours))
        
        # this dead cell becomes alive as it has exactly 3 live neighbours
        if len(neighbours) == 3:
            new_positions.add(position)

    return new_positions


def get_neighbours(pos):
    # get neighbour cells of current cell pos
    # 8 directions

    x,y = pos
    neighbours = []
    for dx in [-1, 0, 1]:
        if x + dx < 0 or x + dx > GRID_WIDTH:
            # out of grid
            continue
        for dy in [-1, 0 , 1]:
            if y + dy < 0 or y + dy > GRID_HEIGHT:
                # out of grid
                continue
            if dx == 0 and dy == 0 :
                # no displacement so this is current position
                continue
            neighbours.append((x + dx, y + dy))  

    return neighbours 

def draw_grid(positions):
    # positions are alive cells (col,row) 
    for position in positions:
        col,row = position
        # get top left coordinate to draw square
        top_left = (col * TILE_SIZE, row * TILE_SIZE)
        pygame.draw.rect(screen, YELLOW,(*top_left, TILE_SIZE, TILE_SIZE)) # * is projection tuple-> individual values, width , height


    for row in range(GRID_HEIGHT):
        # draw horizontal lines for grid
        pygame.draw.line(screen,BLACK,(0, row * TILE_SIZE),(WIDTH, row * TILE_SIZE))
    for col in range(GRID_WIDTH):
        # draw vertical lines for grid
        pygame.draw.line(screen,BLACK,(col * TILE_SIZE, 0),(col * TILE_SIZE, HEIGHT))




def main():
    running = True
    playing = False
    positions = set()
    # update screen frequency
    count = 0 
    update_freq = 120

    while(running):
        clock.tick(FPS)

        if playing:
            # max value is 60 as FPS = 60
            count += 1
        
        if count >= update_freq:
            # as 120 second is passed update the cells
            count = 0
            positions = adjust_grid(positions)

        pygame.display.set_caption("Playing" if playing else "Paused")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                x,y = pygame.mouse.get_pos()
                col = x // TILE_SIZE
                row = y // TILE_SIZE
                pos = (col,row)

                if pos in positions:
                    positions.remove(pos)
                else:
                    positions.add(pos)
            
            if event.type == pygame.KEYDOWN:
                # pause space
                if event.key == pygame.K_SPACE:
                    playing = not playing
                
                # clear
                if event.key == pygame.K_c:
                    positions = set()
                    playing = False
                    count = 0
                
                # generate random
                if event.key == pygame.K_g:
                    positions = gen(random.randrange(2, 5) * GRID_WIDTH)
                

        screen.fill(GREY)
        draw_grid(positions)
        pygame.display.update()        
    pygame.quit()

if __name__ == '__main__':
    main()