import pygame
import random

# Initialize pygame
pygame.init()

# Game constants
WIDTH = 800
HEIGHT = 600
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
DOT_COLOR = (255, 165, 0)

# Define game classes

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((40, 40))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.speed_x = 0
        self.speed_y = 0
        self.score = 0

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Keep the player within the screen boundaries
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top < 0:
            self.rect.top = 0

# Dot class
class Dot(pygame.sprite.Sprite):
    def __init__(self, player):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 10))
        self.image.fill(DOT_COLOR)
        self.rect = self.image.get_rect()
        self.player = player
        self.reset()

    def reset(self):
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(HEIGHT - self.rect.height)

    def update(self):
        # Check collision with the player
        if pygame.sprite.collide_rect(self, self.player):
            self.player.score += 10
            self.reset()

# Ghost class
class Ghost(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((40, 40))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(HEIGHT - self.rect.height)
        self.speed_x = random.choice([-2, 2])
        self.speed_y = random.choice([-2, 2])

    def update(self):
        # Move randomly
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Keep the ghost within the screen boundaries
        if self.rect.right > WIDTH or self.rect.left < 0:
            self.speed_x *= -1
        if self.rect.bottom > HEIGHT or self.rect.top < 0:
            self.speed_y *= -1

# Initialize game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac-Man Game")
clock = pygame.time.Clock()

# Create sprite groups
all_sprites = pygame.sprite.Group()
dots_group = pygame.sprite.Group()
ghosts = pygame.sprite.Group()

# Create game objects
player = Player()
all_sprites.add(player)

for _ in range(5):
    ghost = Ghost()
    all_sprites.add(ghost)
    ghosts.add(ghost)

dot = Dot(player)
all_sprites.add(dot)
dots_group.add(dot)

# Game loop
running = True
while running:
    # Process events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.speed_x = -2
            elif event.key == pygame.K_RIGHT:
                player.speed_x = 2
            elif event.key == pygame.K_UP:
                player.speed_y = -2
            elif event.key == pygame.K_DOWN:
                player.speed_y = 2
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player.speed_x = 0
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                player.speed_y = 0

    # Update
    all_sprites.update()

    # Check collision with ghosts
    if pygame.sprite.spritecollide(player, ghosts, False):
        running = False  # Game over

    # Render
    screen.fill(BLACK)
    all_sprites.draw(screen)

    # Display score
    font = pygame.font.Font(None, 36)
    score_text = font.render("Score: " + str(player.score), True, WHITE)
    screen.blit(score_text, (10, 10))

    # Flip the display
    pygame.display.flip()

    # Control the game's FPS
    clock.tick(FPS)

# Quit the game
pygame.quit()
