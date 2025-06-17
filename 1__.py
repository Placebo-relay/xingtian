```
grid conway pygame quick test
```

import pygame
import time
import sys
from collections import deque

class GameOfLife:
    def __init__(self, width, height, cell_size=30):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.reset_game()
        
        # Colors
        self.bg_color = (0, 0, 0)
        self.grid_color = (50, 50, 50)
        self.cell_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        self.game_over_color = (255, 0, 0)
        
        # Pygame setup
        pygame.init()
        self.screen_width = width * cell_size + 40
        self.screen_height = height * cell_size + 80
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Conway's Game of Life")
        self.font = pygame.font.SysFont('Arial', 16)
        self.big_font = pygame.font.SysFont('Arial', 24)
        
        # Margins
        self.left = (self.screen_width - width * cell_size) // 2
        self.top = (self.screen_height - height * cell_size) // 2

    def reset_game(self):
        self.board = [[0] * self.width for _ in range(self.height)]
        self.paused = True
        self.generation = 0
        self.last_update = 0
        self.update_interval = 0.5
        self.game_over = False
        self.termination_reason = ""
        self.history = deque(maxlen=20)
        self.last_changes = 0

    def count_neighbors(self, x, y):
        count = 0
        for i in (-1, 0, 1):
            for j in (-1, 0, 1):
                if i == 0 and j == 0:
                    continue
                nx, ny = x + i, y + j
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    count += self.board[ny][nx]
        return count

    def update(self):
        if self.game_over:
            return 0
            
        new_board = [[0 for _ in range(self.width)] for _ in range(self.height)]
        changes = 0
        
        for y in range(self.height):
            for x in range(self.width):
                neighbors = self.count_neighbors(x, y)
                
                if self.board[y][x] == 1:  # Living cell
                    if neighbors < 2 or neighbors > 3:
                        new_board[y][x] = 0
                        changes += 1
                    else:
                        new_board[y][x] = 1
                else:  # Dead cell
                    if neighbors == 3:
                        new_board[y][x] = 1
                        changes += 1
        
        # Don't check termination on manual clear
        if not (self.last_changes == -1 and changes == 0):  # Skip check after clear
            if self.check_termination_conditions(new_board, changes):
                self.game_over = True
                return changes
                
        self.last_changes = changes
        self.history.append([row[:] for row in self.board])
        self.board = new_board
        self.generation += 1
        return changes

    def check_termination_conditions(self, new_board, changes):
        # Only check for all dead cells during simulation, not after clear
        if sum(sum(row) for row in new_board) == 0 and self.generation > 0:
            self.termination_reason = "Все клетки мертвы"
            return True
            
        # Stable configuration (no changes)
        if changes == 0 and self.generation > 0:
            self.termination_reason = "Стабильная конфигурация"
            return True
            
        # Periodic configuration
        for i, past_state in enumerate(self.history):
            if self.boards_equal(new_board, past_state):
                period = len(self.history) - i
                self.termination_reason = f"Повтор конфигурации (период {period})"
                return True
                
        return False

    def boards_equal(self, board1, board2):
        for y in range(self.height):
            for x in range(self.width):
                if board1[y][x] != board2[y][x]:
                    return False
        return True

    def draw(self):
        self.screen.fill(self.bg_color)
        
        # Draw cells
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] == 1:
                    pygame.draw.rect(
                        self.screen, 
                        self.cell_color, 
                        (
                            x * self.cell_size + self.left,
                            y * self.cell_size + self.top,
                            self.cell_size,
                            self.cell_size
                        )
                    )
        
        # Draw grid
        for x in range(self.width + 1):
            pygame.draw.line(
                self.screen,
                self.grid_color,
                (self.left + x * self.cell_size, self.top),
                (self.left + x * self.cell_size, self.top + self.height * self.cell_size)
            )
        for y in range(self.height + 1):
            pygame.draw.line(
                self.screen,
                self.grid_color,
                (self.left, self.top + y * self.cell_size),
                (self.left + self.width * self.cell_size, self.top + y * self.cell_size)
            )
        
        # Draw info
        status = "PAUSED" if self.paused else f"RUNNING (Gen: {self.generation})"
        if self.game_over:
            status = f"GAME OVER: {self.termination_reason}"
        
        status_text = self.font.render(status, True, self.text_color)
        controls_text = self.font.render("SPACE: Pause | N: Next | C: New Game | R: Random", True, self.text_color)
        
        self.screen.blit(status_text, (10, 10))
        self.screen.blit(controls_text, (10, self.screen_height - 25))
        
        if self.game_over:
            restart_text = self.big_font.render("Нажмите C для новой игры", True, self.game_over_color)
            text_rect = restart_text.get_rect(center=(self.screen_width//2, self.screen_height//2))
            self.screen.blit(restart_text, text_rect)

    def handle_click(self, pos):
        if self.game_over:
            return
            
        x = (pos[0] - self.left) // self.cell_size
        y = (pos[1] - self.top) // self.cell_size
        
        if 0 <= x < self.width and 0 <= y < self.height:
            self.board[y][x] = 1 if self.board[y][x] == 0 else 0

    def clear(self):
        self.reset_game()

    def randomize(self, density=0.2):
        import random
        self.board = [
            [1 if random.random() < density else 0 for _ in range(self.width)]
            for _ in range(self.height)
        ]
        self.generation = 0
        self.game_over = False
        self.history.clear()
        self.last_changes = -1  # Special flag to skip termination check after randomize

    def run(self):
        clock = pygame.time.Clock()
        
        while True:
            current_time = time.time()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click
                        self.handle_click(event.pos)
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and not self.game_over:
                        self.paused = not self.paused
                    elif event.key == pygame.K_n and (self.paused or self.game_over):
                        self.update()
                    elif event.key == pygame.K_c:
                        self.clear()
                    elif event.key == pygame.K_r and not self.game_over:
                        self.randomize()
                    elif event.key == pygame.K_UP and not self.game_over:
                        self.update_interval = max(0.1, self.update_interval - 0.1)
                    elif event.key == pygame.K_DOWN and not self.game_over:
                        self.update_interval += 0.1
            
            if not self.paused and not self.game_over and current_time - self.last_update >= self.update_interval:
                self.update()
                self.last_update = current_time
            
            self.draw()
            pygame.display.flip()
            clock.tick(30)

if __name__ == "__main__":
    game = GameOfLife(20, 20, 25)
    game.run()