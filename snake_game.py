import pygame
import random
import ctypes

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Block size
BLOCK_SIZE = 20

# FPS
FPS = 10

class SnakeGame:
    def __init__(self, width=640, height=480, fps=10):
        self.width = width
        self.height = height
        self.fps = fps
        self.display = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Snake Game')
        # Bring window to front on Windows
        try:
            hwnd = pygame.display.get_wm_info()['window']
            ctypes.windll.user32.SetForegroundWindow(hwnd)
        except:
            pass  # Ignore if not on Windows or fails
        self.clock = pygame.time.Clock()
        self.reset()

    def reset(self):
        self.snake = [(self.width//2, self.height//2)]
        self.direction = (0, -BLOCK_SIZE)
        self.food = self._place_food()
        self.score = 0
        self.game_over = False

    def _place_food(self):
        x = random.randint(0, (self.width - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (self.height - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        return (x, y)

    def _move(self):
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
        for segment in self.snake:
            pygame.draw.rect(self.display, GREEN, (segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(self.display, RED, (self.food[0], self.food[1], BLOCK_SIZE, BLOCK_SIZE))
        font = pygame.font.SysFont(None, 35)
        text = font.render(f"Score: {self.score}", True, WHITE)
        self.display.blit(text, (10, 10))
        pygame.display.update()

    def play_step(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and self.direction != (BLOCK_SIZE, 0):
                    self.direction = (-BLOCK_SIZE, 0)
                elif event.key == pygame.K_RIGHT and self.direction != (-BLOCK_SIZE, 0):
                    self.direction = (BLOCK_SIZE, 0)
                elif event.key == pygame.K_UP and self.direction != (0, BLOCK_SIZE):
                    self.direction = (0, -BLOCK_SIZE)
                elif event.key == pygame.K_DOWN and self.direction != (0, -BLOCK_SIZE):
                    self.direction = (0, BLOCK_SIZE)

        self._move()
        self._check_collision()
        self._draw()
        self.clock.tick(self.fps)
        return self.game_over

def draw_menu(display, font):
    display.fill(BLACK)
    title = font.render("Snake Game", True, WHITE)
    display.blit(title, (320 - title.get_width()//2, 100))
    easy = font.render("1. Easy", True, GREEN)
    display.blit(easy, (320 - easy.get_width()//2, 200))
    medium = font.render("2. Medium", True, WHITE)
    display.blit(medium, (320 - medium.get_width()//2, 250))
    hard = font.render("3. Hard", True, RED)
    display.blit(hard, (320 - hard.get_width()//2, 300))
    pygame.display.update()

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
    game = SnakeGame(fps=difficulty)
    while not game.game_over:
        game.play_step()
    pygame.quit()

if __name__ == "__main__":
    main()