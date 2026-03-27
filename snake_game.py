import pygame
import random

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
    def __init__(self, width=640, height=480):
        self.width = width
        self.height = height
        self.display = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Snake Game')
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
        self.clock.tick(FPS)
        return self.game_over

def main():
    pygame.init()
    game = SnakeGame()
    while not game.game_over:
        game.play_step()
    pygame.quit()

if __name__ == "__main__":
    main()