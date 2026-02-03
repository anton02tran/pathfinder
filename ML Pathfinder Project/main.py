# CODE TO DISPLAY THE WINDOW

import pygame # type: ignore
import sys
from player import get_neighbors
from player import bfs

# VALUES
# DIMENSIONS
WIDTH = 1800
HEIGHT = 920
GRID_SIZE = 40 # square sizes.

# COLOURS
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
PURPLE = (160, 32, 240) 
ORANGE = (255, 165, 0)
LIGHT_BLUE = (173, 216, 230)
LIGHTER_GRAY = (158, 158, 158)
GRAY = (128, 128, 128)
BLACK = (0, 0, 0)

# POSITIONS
PLAYER_POS = [6, 5]
AI_POS = [6, 5]
MOVED = False

# ALGORITHM CHECKS
PATHFINDING_ON = -1
AI_ON = -1

# EXTRA
AI_PATH = [] # LIST FOR BFS PATH 
FRAMES_RAN = 0 
DEATHS = 0
WINS = 0
GEN = 0 
STEPS = 0
time_alive = 0

# MEMORY BANK

ROWS = HEIGHT // GRID_SIZE  
COLS = WIDTH // GRID_SIZE   

grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]

grid[6][5] = 2 # START VALUE
grid[ROWS-5][COLS-5] = 3 # END VALUE

# INTEGRATE PATHFINDERS 

from pathfinder import QAgent
agent = QAgent(ROWS, COLS)

def run_ai_step():
    global AI_POS
    global DEATHS
    global GEN
    global WINS
    global STEPS
    global time_alive

    state = (AI_POS[0], AI_POS[1])
    action = agent.get_action(state)
    
    # Calculate new position, UP, DOWN, LEFT, RIGHT
    new_r, new_c = state
   
    if action == 0: # UP
        new_r -= 1 
        STEPS += 1
    if action == 1: # DOWN
        new_r += 1 
        STEPS += 1
    if action == 2: # LEFT
        new_c -= 1 
        STEPS += 1
    if action == 3: # RIGHT
        new_c += 1 
        STEPS += 1
    
# PATHFINDER PARAMETERS

    # Boundaries and Walls
    if not (0 <= new_r < ROWS and 0 <= new_c < COLS) or grid[new_r][new_c] == 1:
        reward = -5
        new_r, new_c = state # Don't move
        time_alive += 1
        done = False
    
    # Obstacles
    elif grid[new_r][new_c] == 4:
        reward = -500
        new_r, new_c = (6, 5) # Reset to hardcoded start
        done = True # "Die" and start over
        time_alive = 0
        DEATHS += 1
        GEN += 1

    # Goal
    elif grid[new_r][new_c] == 3:
        reward = 888
        new_r, new_c = (6, 5) # Reset for next training round
        done = True
        time_alive = 0
        WINS += 1
        GEN += 1
        
    # Path
    elif grid[new_r][new_c] == 5:
        reward = 0 # Walking on the Path does not cost the AI
        time_alive += 1
        done = False

    # Check if time_alive is more than set time. (removed feature, made robot take wayyyy to long to start finding the exit)

    # elif time_alive > 300:
        # reward = -100 # Dying by time loses less than obstacle
        # new_r, new_c = (6, 5) # Reset to hardcoded start
        # done = True # "Die" and start over
        # time_alive = 0
        # DEATHS += 1
        # GEN += 1

    # Normal Path
    else:
        reward = -1 # Small penalty for every step to encourage speed
        time_alive += 1
        done = False

    # Tell the brain what happened
    agent.update(state, action, reward, (new_r, new_c))
    
    # Update actual position
    AI_POS = [new_r, new_c]
    
    # Slowly stop being random
    if done:
        agent.epsilon = max(0.01, agent.epsilon * agent.decay)

# START PROGRAM

print("Starting")

pygame.init()
pygame.font.init()

# DISPLAY SCREEN (COLOURS, AND DIMENSIONS)

font = pygame.font.SysFont("Arial", 18) # Font type and size

# DRAW TEXT FUNCTION

def draw_text(text, x, y):

    text_surface = font.render(text, True, (255, 255, 255)) # Font detailings
    screen.blit(text_surface, (x, y)) # Location

# SCREEN DIMENSIONS + CAPTION

screen = pygame.display.set_mode((WIDTH, HEIGHT)) # Dimensions

pygame.display.set_caption("PATHFINDER")

# ----------------------------------------------------------------------------------- START MAIN LOOP -------------------------------------------------------------------------------------

while True:
    for event in pygame.event.get():
        MOVED = False

    # FRAMES RAN

        FRAMES_RAN += 1
        print(f"frame: {FRAMES_RAN}")

# END GAME WITH CLOSE BUTTON

        if event.type == pygame.QUIT:
            print("Exiting")
            pygame.quit()
            sys.exit()

# CONFIG DURING GAME (RESET: PLAYER/MAP) (OBSTACLE CHECK)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # RESET MAP TO 0
                grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]

                grid[6][5] = 2 # START VALUE, RESET!
                grid[ROWS-5][COLS-5] = 3 # END VALUE, RESET!
            
            # RESET PLAYER POSITION WITH "r"
            if event.key == pygame.K_r: 
                PLAYER_POS = [6, 5]
                print("reset PLAYER")

            # RESET AI POSITION WITH "t"
            if event.key == pygame.K_t: 
                AI_POS = [6, 5]
                print("reset AI")

            # CHECK IF ON OBSTACLE, IF YES, RESET
            new_row, new_col = PLAYER_POS[0], PLAYER_POS[1]
            if grid[new_row][new_col] == 4:
                PLAYER_POS = [6, 5]
                print("died")

# PLAYER MOVEMENT

        if event.type == pygame.KEYDOWN:

            # Create a new potential position
            new_row, new_col = PLAYER_POS[0], PLAYER_POS[1]

            # UP/DOWN MOVEMENT
            if event.key == pygame.K_UP:    
                new_row -= 1
            if event.key == pygame.K_DOWN:  
                new_row += 1
            # LEFT/RIGHT MOVEMENT
            if event.key == pygame.K_LEFT:  
                new_col -= 1
            if event.key == pygame.K_RIGHT: 
                new_col += 1

            # BOUNDARY CHECK + WALL CHECK BEFORE UPDATE
            if 0 <= new_row < ROWS and 0 <= new_col < COLS: # CHECK IF INSIDE BOUNDS
                if grid[new_row][new_col] != 1: # CHECK IF THE BLOCK IS A WALL, IF NOT, PASS,
                    PLAYER_POS[0] = new_row
                    PLAYER_POS[1] = new_col 

                    # CHECK IF NEW POSITION IS AN OBSTACLE
                    if grid[new_row][new_col] == 4:
                        PLAYER_POS = [6, 5]
                        MOVED = True

                    new_col, new_row = PLAYER_POS[0], PLAYER_POS[1] # UPDATE POSITION
                    MOVED = True

# START BFS PATHFINDING

        # TOGGLE PATHFINDING WITH "enter"

        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_RETURN:
                PATHFINDING_ON *= -1

        # IF PATHFINDING IS ON, RUN CODE

        if PATHFINDING_ON == 1:    
            start_node = (PLAYER_POS[0], PLAYER_POS[1])
            end_node = (ROWS-5, COLS-5)
            
            AI_PATH = bfs(start_node, end_node, grid, ROWS, COLS)
            if AI_PATH:
                print(f"Path found, Length: {len(AI_PATH)}")
            else:
                print("No path possible")

# START ML PATHFINDER 

    # TOGGLE AI WITH "g"

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_g:
                AI_ON *= -1

        if AI_ON == 1:
            run_ai_step()

# MEMORY UDPATE FROM MOUSE CLICKS

        # LEFT CLICK = WALL
        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos() # Get (x, y) of mouse
            col = pos[0] // GRID_SIZE    # Convert pixel to grid index
            row = pos[1] // GRID_SIZE    # Convert pixel to grid index
            
            # BOUNDARY CHECK
            if 0 <= row < ROWS and 0 <= col < COLS:
                grid[row][col] = 1 # Mark this spot as a wall in memory

        # RIGHT CLICK = OBSTACLE
        if pygame.mouse.get_pressed()[2]:
            pos = pygame.mouse.get_pos() # Get (x, y) of mouse
            col = pos[0] // GRID_SIZE    # Convert pixel to grid index
            row = pos[1] // GRID_SIZE    # Convert pixel to grid index
            
            # BOUNDARY CHECK
            if 0 <= row < ROWS and 0 <= col < COLS:
                grid[row][col] = 4 # Mark this spot as an obstacle in memory

        # MIDDLE CLICK = PATH
        if pygame.mouse.get_pressed()[1]:
            pos = pygame.mouse.get_pos() # Get (x, y) of mouse
            col = pos[0] // GRID_SIZE    # Convert pixel to grid index
            row = pos[1] // GRID_SIZE    # Convert pixel to grid index
            
            # BOUNDARY CHECK
            if 0 <= row < ROWS and 0 <= col < COLS:
                grid[row][col] = 5 # Mark this spot as an path in memory

# START DRAWINGS
# FILL SCREEN WITH LIGHT GRAY

        screen.fill((LIGHTER_GRAY)) 

# DRAW GRID ON SCREEN

        for x in range(0, WIDTH, GRID_SIZE):
            pygame.draw.line(screen, (GRAY), (x, 0), (x, HEIGHT))

        for y in range(0, HEIGHT, GRID_SIZE):
            pygame.draw.line(screen, (GRAY), (0, y), (WIDTH, y))

# DRAW PATH FOR BFS

        if PATHFINDING_ON == 1: 
            if AI_PATH:
                for node in AI_PATH:
                    pygame.draw.rect(screen, (LIGHT_BLUE), # LIGHT BLUE COLOUR
                                    (node[1] * GRID_SIZE + 8, node[0] * GRID_SIZE + 8, # CHANGE PATH SIZE
                                    GRID_SIZE - 16, GRID_SIZE - 16))
                    
# DRAW START AND END SQUARES

        pygame.draw.rect(screen, (GREEN), (5*GRID_SIZE+1, 6*GRID_SIZE+1, GRID_SIZE-1, GRID_SIZE-1)) # Draw START

        pygame.draw.rect(screen, (RED), ((COLS-5)*GRID_SIZE+1, (ROWS-5)*GRID_SIZE+1, GRID_SIZE-1, GRID_SIZE-1)) # Draw END

# DRAW PLAYER

        pygame.draw.rect(screen, (BLUE), (PLAYER_POS[1] * GRID_SIZE, PLAYER_POS[0] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

# WALL BUILDER, PAINTING NEW VALUES FROM MEMORY

        # BUILD NORMAL WALLS
        for r in range(ROWS):
            for c in range(COLS):
                if grid[r][c] == 1:
                    # Draw a square at this grid position
                    pygame.draw.rect(screen, (BLACK), (c * GRID_SIZE, r * GRID_SIZE, GRID_SIZE, GRID_SIZE))

        # BUILD OBSTACLES
        for r in range(ROWS):
            for c in range(COLS):
                if grid[r][c] == 4:
                    # Draw a square at this grid position
                    pygame.draw.rect(screen, (ORANGE), (c * GRID_SIZE, r * GRID_SIZE, GRID_SIZE, GRID_SIZE))

        # BUILD PATH
        for r in range(ROWS):
            for c in range(COLS):
                if grid[r][c] == 5:
                    # Draw a square at this grid position
                    pygame.draw.rect(screen, (WHITE), (c * GRID_SIZE, r * GRID_SIZE, GRID_SIZE, GRID_SIZE))

# DRAW AI RUNNER

        if AI_ON == 1:
            pygame.draw.rect(screen, (PURPLE), (AI_POS[1] * GRID_SIZE, AI_POS[0] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

# DISPLAY TEXT

        draw_text(f"L-Click: Wall", 10, 10) 
        draw_text(f"R-Click: Lava", 10, 30) 
        draw_text(f"Reset Player: r", 150, 10)
        draw_text(f"Reset Map: SPACE", 150, 30)
        draw_text(f"Pathfinding toggle: enter", 1590, 10)
        draw_text(f"AI toggle: g", 1590, 30)
        draw_text(f"WINS: {WINS}", 1590, 70)
        draw_text(f"DEATHS: {DEATHS}", 1590, 90)
        draw_text(f"GENERATION: {GEN}", 1590, 110)
        draw_text(f"STEPS: {STEPS}", 1590, 130)
        # draw_text(f"TIME_ALIVE: {time_alive}", 1590, 150) # removed feature

# UPDATE DISPLAY

        pygame.display.flip()


