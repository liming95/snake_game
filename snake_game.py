import pygame
import random
import sys

# 颜色定义
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

BLOCK_SIZE = 20

class SnakeGame:
    def __init__(self, display, fps=10):
        self.display = display
        self.width, self.height = display.get_size()
        self.fps = fps
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 35)
        self.big_font = pygame.font.SysFont(None, 50)
        self.reset()

    def reset(self):
        """重置游戏状态"""
        center_x = self.width // 2
        center_y = self.height // 2
        self.snake = [
            (center_x, center_y),
            (center_x, center_y + BLOCK_SIZE),
            (center_x, center_y + 2 * BLOCK_SIZE)
        ]
        self.direction = (0, -BLOCK_SIZE)
        self.next_direction = (0, -BLOCK_SIZE)
        self.food = self._place_food()
        self.score = 0
        self.game_over = False
        self.paused = False

    def _place_food(self):
        while True:
            x = random.randint(0, (self.width - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
            y = random.randint(0, (self.height - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
            if (x, y) not in self.snake:
                return (x, y)

    def _move(self):
        self.direction = self.next_direction
        head = self.snake[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])
        self.snake.insert(0, new_head)
        if new_head == self.food:
            self.score += 1
            self.food = self._place_food()
        else:
            self.snake.pop()

    def _check_collision(self):
        head = self.snake[0]
        if head[0] < 0 or head[0] >= self.width or head[1] < 0 or head[1] >= self.height:
            self.game_over = True
        if head in self.snake[1:]:
            self.game_over = True

    def _draw(self):
        self.display.fill(BLACK)
        for i, seg in enumerate(self.snake):
            color = BLUE if i == 0 else GREEN
            pygame.draw.rect(self.display, color, (seg[0], seg[1], BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(self.display, RED, (self.food[0], self.food[1], BLOCK_SIZE, BLOCK_SIZE))

        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.display.blit(score_text, (10, 10))
        speed_text = self.font.render(f"Speed: {self.fps}", True, WHITE)
        self.display.blit(speed_text, (10, 40))
        control_text = self.font.render("P: Pause | R: Restart | ESC: Quit", True, WHITE)
        self.display.blit(control_text, (10, self.height - 30))

        if self.paused:
            pause_text = self.big_font.render("PAUSED - Press P to continue", True, WHITE)
            self.display.blit(pause_text, (self.width//2 - pause_text.get_width()//2, self.height//2))

        if self.game_over:
            overlay = pygame.Surface((self.width, self.height))
            overlay.set_alpha(180)
            overlay.fill(BLACK)
            self.display.blit(overlay, (0, 0))
            game_over_text = self.big_font.render("GAME OVER", True, RED)
            self.display.blit(game_over_text, (self.width//2 - game_over_text.get_width()//2, self.height//2 - 60))
            final_score_text = self.font.render(f"Final Score: {self.score}", True, WHITE)
            self.display.blit(final_score_text, (self.width//2 - final_score_text.get_width()//2, self.height//2 - 10))
            restart_text = self.font.render("Press R to Restart or ESC to Quit", True, WHITE)
            self.display.blit(restart_text, (self.width//2 - restart_text.get_width()//2, self.height//2 + 40))

        pygame.display.update()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif self.game_over:
                        if event.key == pygame.K_r:
                            self.reset()
                        elif event.key == pygame.K_q:
                            running = False
                    else:
                        if event.key == pygame.K_p:
                            self.paused = not self.paused
                        elif event.key == pygame.K_r:
                            self.reset()
            keys = pygame.key.get_pressed()
            if not self.game_over and not self.paused:
                if keys[pygame.K_LEFT] and self.direction != (BLOCK_SIZE, 0):
                    self.next_direction = (-BLOCK_SIZE, 0)
                elif keys[pygame.K_RIGHT] and self.direction != (-BLOCK_SIZE, 0):
                    self.next_direction = (BLOCK_SIZE, 0)
                elif keys[pygame.K_UP] and self.direction != (0, BLOCK_SIZE):
                    self.next_direction = (0, -BLOCK_SIZE)
                elif keys[pygame.K_DOWN] and self.direction != (0, -BLOCK_SIZE):
                    self.next_direction = (0, BLOCK_SIZE)
            if not self.game_over and not self.paused:
                self._move()
                self._check_collision()
            self._draw()
            self.clock.tick(self.fps if not self.game_over else 30)
        return self.score

def show_menu():
    print("Snake Game")
    print("Select difficulty:")
    print("1. Easy (slow speed)")
    print("2. Medium (normal speed)")
    print("3. Hard (fast speed)")
    while True:
        choice = input("Enter 1, 2, or 3: ").strip()
        if choice == '1':
            return 5
        elif choice == '2':
            return 10
        elif choice == '3':
            return 15
        else:
            print("Invalid choice, please enter 1, 2, or 3.")

def main():
    difficulty = show_menu()
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Snake Game")
    # Bring window to front on Windows
    try:
        import ctypes
        hwnd = pygame.display.get_wm_info()['window']
        ctypes.windll.user32.SetForegroundWindow(hwnd)
    except:
        pass
    game = SnakeGame(display=screen, fps=difficulty)
    final_score = game.run()
    pygame.quit()
    print(f"Game Over! Final Score: {final_score}")

if __name__ == "__main__":
    main()