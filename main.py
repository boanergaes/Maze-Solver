import pygame
from maze import Maze
from constants import ROWS,  COLS, FPS, WIDTH, HEIGHT

def main():
    pygame.init()
    
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Maze Solver")
    
    clock = pygame.time.Clock()
    
    maze = Maze(ROWS, COLS)
    
    # generate maze
    maze.generate(screen)
    
    maze.add_random_cycles()

    pygame.time.delay(1000)

    # solve maze
    maze.solve(screen)
    
    # keep window open
    while True:
        maze.handle_events()
        maze.draw(screen)
        clock.tick(FPS)
        
if __name__ == "__main__":
    main()
