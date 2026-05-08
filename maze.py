import pygame
import random
import sys
from constants import CELL_SIZE, WHITE, BLACK, RED, BLUE, GREEN, WIDTH, HEIGHT

class Maze:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.north_wall = [ [True]*cols for _ in range(rows) ]
        self.east_wall = [ [True]*cols for _ in range(rows) ]
        self.visited = [ [False]*cols for _ in range(rows) ]
        self.solution_visited = [ [False]*cols for _ in range(rows) ]
        self.dead_ends = set()
        self.solution_path = []
        self.start = (0, 0)
        self.end = (rows - 1, cols - 1)
        
    def draw(self, screen, current=None, solving=False):
        screen.fill(BLACK)
        
        # draw dead ends
        for r, c in self.dead_ends:
            pygame.draw.rect(
                screen,
                BLUE,
                (
                    c * CELL_SIZE + 4,
                    r * CELL_SIZE + 4, 
                    CELL_SIZE - 8,
                    CELL_SIZE - 8
                )
            )
        
        # draw solution path
        for r, c in self.solution_path:
            pygame.draw.rect(
                screen,
                GREEN,
                (
                    c * CELL_SIZE + 6,
                    r * CELL_SIZE + 6,
                    CELL_SIZE - 12,
                    CELL_SIZE - 12
                )
            )
        
        # draw current mouse position  
        if current:
            r, c = current
            
            pygame.draw.circle(
                screen,
                RED,
                (
                    c * CELL_SIZE + CELL_SIZE // 2,
                    r * CELL_SIZE + CELL_SIZE // 2
                ),
                CELL_SIZE // 4
            )
        
        # draw walls
        for r in range(self.rows):
            for c in range(self.cols):
                x = c * CELL_SIZE
                y = r * CELL_SIZE
                
                if self.north_wall[r][c]:
                    pygame.draw.line(
                        screen,
                        WHITE,
                        (x, y),
                        (x + CELL_SIZE, y),
                        2
                    )
                    
                if self.east_wall[r][c]:
                    pygame.draw.line(
                        screen,
                        WHITE,
                        (x + CELL_SIZE, y),
                        (x + CELL_SIZE, y + CELL_SIZE),
                        2
                    )
        
        # left border      
        pygame.draw.line(
            screen,
            WHITE,
            (0, 0),
            (0, HEIGHT),
            2
        )
        
        # bottom border
        pygame.draw.line(
            screen,
            WHITE,
            (0, HEIGHT),
            (WIDTH, HEIGHT),
            2
        )
        
        # openings
        sr, sc = self.start
        er, ec = self.end
        
        # start opening (left side)
        pygame.draw.line(
            screen,
            RED,
            (0, sr * CELL_SIZE + 2),
            (0, sr * CELL_SIZE + CELL_SIZE - 2),
            20
        )
        
        # end openings (right side)
        pygame.draw.line(
            screen,
            GREEN,
            (WIDTH, er * CELL_SIZE + 2),
            (WIDTH, er * CELL_SIZE + CELL_SIZE - 2),
            20
        )
        
        pygame.display.flip()
            
    def generate(self, screen):
        stack = []
        start_r = random.randint(0, self.rows - 1)
        start_c = random.randint(0, self.cols - 1)
        self.visited[start_r][start_c] = True
        stack.append((start_r, start_c))
        
        while stack:
            self.handle_events()
            
            current = stack[-1]
            r, c = current
            neighbors = self.get_unvisited_neighbors(r, c)
            
            if neighbors:
                nr, nc = random.choice(neighbors)
                self.remove_wall(r, c, nr, nc)
                self.visited[nr][nc] = True
                stack.append((nr, nc))
            else:
                stack.pop()
                
            self.draw(screen, current=current)
            pygame.time.delay(20)
         
        # create random start/end   
        self.start = ( random.randint(0, self.rows - 1), 0 )
        self.end = ( random.randint(0, self.rows - 1), self.cols - 1 )
        
    def solve(self, screen):
        stack = []
        sr, sc = self.start
        er, ec = self.end
        stack.append((sr, sc))
        self.solution_visited[sr][sc] = True
        
        while stack:
            self.handle_events()
            current = stack[-1]
            r, c = current
            self.solution_path = list(stack)
            self.draw(screen, current=current, solving=True)
            pygame.time.delay(40)
            
            if current == (er, ec):
                print("Maze Solved!")
                return True

            neighbors = self.get_reachable_neighbors(r, c)
            moved = False
            random.shuffle(neighbors)

            for nr, nc in neighbors:
                if not self.solution_visited[nr][nc]:
                    self.solution_visited[nr][nc] = True
                    stack.append((nr, nc))
                    moved = True
                    break
                
            if not moved:
                self.dead_ends.add(current)
                stack.pop()
                
        return False
    
    # helpers
    
    def get_unvisited_neighbors(self, r, c):
        neighbors = []
        
        # up
        if r > 0 and not self.visited[r - 1][c]:
            neighbors.append((r - 1, c))
        # down
        if r < self.rows - 1 and not self.visited[r + 1][c]:
            neighbors.append((r + 1, c))
        # left
        if c > 0 and not self.visited[r][c - 1]:
            neighbors.append((r, c - 1))
        # right
        if c < self.cols - 1 and not self.visited[r][c + 1]:
            neighbors.append((r, c + 1))
        
        return neighbors
    
    def remove_wall(self, r, c, nr, nc):
        # right
        if nr == r and nc == c + 1:
            self.east_wall[r][c] = False
        # left 
        elif nr == r and nc == c - 1:
            self.east_wall[r][c - 1] = False
        # up
        elif nr == r - 1 and nc == c:
            self.north_wall[r][c] = False
        # down
        elif nr == r + 1 and nc == c:
            self.north_wall[r + 1][c] = False
            
    def get_reachable_neighbors(self, r, c):
        neighbors = []
        
        # right
        if c < self.cols - 1 and not self.east_wall[r][c]:
                neighbors.append((r, c + 1))
        # left
        if c > 0 and not self.east_wall[r][c - 1]:
                neighbors.append((r, c - 1))
        # up
        if r > 0 and not self.north_wall[r][c]:
                neighbors.append((r - 1, c))
        # down
        if r < self.rows - 1 and not self.north_wall[r + 1][c]:
                neighbors.append((r + 1, c))
                
        return neighbors
                            
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
